import time
from queue import Queue, Empty
import traceback
import threading
import json
from textwrap import dedent
from termcolor import colored
from .diff import diff, diff_mutations
from .frame import (
    AppRunnerFrame,
    StateAccessFrame,
    ResetUIEventsFrame,
    RenderFrame,
    UIUpdatesFrame,
)
from .ui_prop_state import UIPropState
from .debug import (
    PROFILE_RENDER,
    PROFILE_DIFF,
    PROFILE_RUN,
    PRINT_OUTPUT,
    timing,
    logger,
)
from .cache import Cache, cached_app
from .exceptions import Stop
from .application_state import ApplicationState
from .components.box import vbox
from .components.lifecycle import lifecycle
from .ui_singleton import SingletonCollector


class AppRunner:
    """
    Manages the repeated running of the application, and holds on to
    the global prop state, for a user session. Corresponds 1 to 1 with
    a websocket connection.
    """

    def __init__(
        self,
        connection,
        task_runtime,
        app_function,
        initial_ui_updates,
    ):
        # The websocket connection
        self.connection = connection
        # A hyperdiv.task_runtime.TaskRuntime instance
        self.task_runtime = task_runtime
        # The user app
        self.app_function = cached_app(app_function)

        # The cache managing @cached and @cached_app functions
        self.cache = Cache()

        # The root container computed on the previous run, used when
        # calculating the diff of the most recent run
        self.previous_root_container = None

        # A list of hyperdiv.ui_command.UICommand to send to the
        # browser in the next reply.
        self.pending_commands = []

        # Generic key-value in-memory storage that components can
        # use. For example local_storage uses it for its internal
        # cache.
        self.storage = dict()

        # The global state holding all component props.
        self.state = ApplicationState()
        # A data structure that remembers the prop values that were
        # last sent to the browser. Used to determine which changed
        # prop values need to be sent to the browser.
        self.ui_prop_state = UIPropState(self.state)

        # The queue receiving prop updates from the browser (or
        # internally from simulated events), or mutations from tasks.
        self.input_queue = Queue()

        # An internal cache of updates previously taken off
        # `input_queue` but not yet ready to be processed. Will be
        # processed on the next run.
        self.ui_updates = []

        # The run number of the current run. Increments by 1 with
        # every run.
        self.run_id = -1

        # The initial updates to be added to the input
        # queue. `initial_ui_updates` are sent by the browser on
        # connect.
        self.initial_ui_updates = initial_ui_updates + [
            (lifecycle._key, "app_started", True)
        ]

        # The core thread processing the input queue and running the
        # application.
        self.thread = threading.Thread(target=self.run_loop_wrapper)

    def start(self):
        """
        Start the internal thread, which starts processing the queue.
        """
        self.thread.start()
        self.enqueue_ui_updates(self.initial_ui_updates)

    def process_queue(self, timeout=1):
        """
        Called only by the internal thread.

        Takes updates from the input queue and returns them. If
        updates clash on (key, prop_name), only the first is returned,
        and the rest are saved in `self.ui_updates` to be processed on
        subsequent runs.
        """
        task_mutations = []
        stop = False

        def process(elem):
            nonlocal stop

            if elem[0] == "task_mutations":
                task_mutations.extend(elem[1])
            elif elem[0] in "ui_updates":
                self.ui_updates.extend(elem[1])
            elif elem[0] == "stop":
                stop = True
            else:
                raise Exception(f"Malformed update: {elem}")

        try:
            # Block on an empty queue only if we don't have any
            # previous updates saved in `self.ui_updates`.
            if not self.ui_updates:
                process(self.input_queue.get(timeout=timeout))
            while True:
                try:
                    process(self.input_queue.get_nowait())
                except Empty:
                    break
        except Empty:
            pass

        if not self.ui_updates:
            return stop, [], task_mutations

        # We apply updates in batches disjoint on (key, prop_name). We
        # assume it's ok to apply multiple updates in the same frame
        # as long as we're not updating the same prop multiple times.

        check_set = set()
        ui_updates = []

        for (key, prop_name, value) in list(self.ui_updates):
            if (key, prop_name) not in check_set:
                check_set.add((key, prop_name))
                ui_updates.append((key, prop_name, value))
                self.ui_updates.remove((key, prop_name, value))

        return stop, ui_updates, task_mutations

    def get_storage(self, key, default=None):
        """
        Creates/returns a storage dict at `key`.
        """
        self.storage.setdefault(key, dict() if default is None else default)
        return self.storage[key]

    def run_user_app(self, frame):
        """
        Called only by the internal thread.

        Runs the user app function in the context of `frame` and
        returns the resulting root container.
        """

        if frame.prev_frame_mutations:
            self.cache.eject_entries_for_mutated_props(frame.prev_frame_mutations)

        root_container = vbox(collect=False)

        with root_container:
            with timing("App", profile=PROFILE_RUN):
                self.app_function()

        logger.debug(f"Component count: {AppRunnerFrame.current().component_count}")
        return root_container

    def apply_ui_updates(self, ui_updates):
        """
        Called only by the internal thread.

        Applies the given `ui_updates` to the application state, and
        returns the mutations caused by these updates, separating
        normal mutations from event mutations.
        """

        with UIUpdatesFrame(self) as ui_update_frame:
            logger.debug(f"UI Updates: {ui_updates}")

            for key, prop_name, value in ui_updates:
                if value == "$reset":
                    ui_update_frame.reset_state(key, prop_name)
                else:
                    ui_update_frame.update_state(key, prop_name, value)

        return ui_update_frame.mutations, ui_update_frame.event_mutations

    def reset_event_mutations(self, frame, event_mutations):
        """
        Called only by the internal thread.

        Resets the props described by the given `event_mutations` to their
        default values.
        """
        for key, prop_name in event_mutations:
            frame.reset_state(key, prop_name)

    def render_and_reply(self, frame, root_container=None, diff=None):
        """
        Called only by the internal thread.

        Given a root container or a diff, render that root container
        or diff and send a reply on the websocket. The reply will
        contain any pending commands and changed singletons.

        Even if there is no relevant container or diff to send, but
        there are commands or singletons, a reply will be sent.
        """
        # frame.set_phase(FramePhase.Rendering)

        output = dict()

        # Render the container or diff

        with timing("Set UI Prop Values"):
            if root_container:
                self.ui_prop_state.set_prop_values_from_component(root_container)
            elif diff:
                self.ui_prop_state.set_prop_values_from_diff(diff)

        with timing("Render", profile=PROFILE_RENDER):
            if root_container:
                output["dom"] = root_container.render()
            elif diff:
                output["diff"] = diff.render()

        # Render changed singletons

        singletons = SingletonCollector.create_ui_singletons()

        for singleton in singletons:
            if self.ui_prop_state.component_changed(singleton):
                self.ui_prop_state.set_prop_values_from_component(singleton)
                output.setdefault("singletons", dict())
                output["singletons"][singleton._name] = singleton.render()

        # Render commands

        if len(self.pending_commands) > 0:
            output["commands"] = [command.render() for command in self.pending_commands]

        self.pending_commands.clear()

        # If anything changed, send it to the UI

        if len(output) > 0:
            if PRINT_OUTPUT:
                logger.debug(json.dumps(output, indent=2))
            self.connection.send(output)

    def diff_and_reply(self, frame, root_container):
        """
        Called only by the internal thread.

        Sends a reply with the given root container (or a diff if a
        previous container exists to diff against).
        """
        dom = None
        dom_diff = None

        if self.previous_root_container:
            with timing("Diff", profile=PROFILE_DIFF):
                dom_diff = diff(self.previous_root_container, root_container)
        else:
            dom = root_container

        self.previous_root_container = root_container

        self.render_and_reply(frame, root_container=dom, diff=dom_diff)

    def diff_mutations_and_reply(self, frame, mutations):
        """
        Called only by the internal thread.

        Given `mutations`, which is a list of (key, prop_name) tuples, it
        creates a diff with those mutated props' new values, and sends
        a reply to the browser.
        """
        self.render_and_reply(frame, diff=diff_mutations(mutations))

    def run(self, mutations, event_mutations=None):
        """
        Called only by the internal thread.

        Runs the user app if necessary, and sends a reply to the browser
        if necessary.

        `mutations` is a set of mutations from a prior frame. Using
        these `mutations`, we determine if the user function is
        "dirty" and needs to run again.

        If `event_mutations` are given, we reset those event props to
        default values after running the user function.
        """
        root_container = None

        # We run the user app in the context of the given mutations.
        with AppRunnerFrame(self, prev_frame_mutations=mutations) as frame:
            run_function = self.app_function.is_dirty()
            if run_function:
                logger.debug(f"Dirty deps: {self.app_function.get_dirty_deps()}")
                root_container = self.run_user_app(frame)

        if event_mutations:
            with ResetUIEventsFrame(self) as reset_frame:
                self.reset_event_mutations(reset_frame, event_mutations)

        if not run_function:
            with RenderFrame(self) as render_frame:
                self.diff_mutations_and_reply(render_frame, mutations)
                return 0

        # We keep running the user app until there are no more
        # dirty mutations, or hit the run limit.
        num_frames = 1
        while True:
            with AppRunnerFrame(self, prev_frame_mutations=frame.mutations) as frame:
                run_function = self.app_function.is_dirty()
                if run_function:
                    logger.debug(f"Dirty deps: {self.app_function.get_dirty_deps()}")
                    root_container = self.run_user_app(frame)
            if not run_function:
                with RenderFrame(self) as render_frame:
                    self.diff_and_reply(render_frame, root_container)
                    break

            num_frames += 1
            if num_frames >= 20:
                raise RuntimeError(
                    "Possible infinite loop detected. Stopped after 20 runs."
                )
        return num_frames

    def run_loop(self):
        """
        Called only by the internal thread.

        The long-running thread that runs the application function in
        response to state updates. This thread is alive if and only if
        the corresponding websocket is connected. When the websocket
        closes, it calls `AppRunner.stop()`, causing the run loop to
        exit.
        """

        # 1st frame
        with StateAccessFrame(self):
            # Add these 'singletons' to the state, because the
            # UI will update them immediately, and their props
            # need to be added to state in order to be
            # updated.
            SingletonCollector.create_singletons()

        # This loop runs indefinitely, until stop() is called, or it
        # exits due to an uncaught exception in user code.
        while True:
            # Grab updates from the queue.
            stop, ui_updates, task_mutations = self.process_queue(timeout=1)

            if ui_updates or task_mutations:
                self.run_id += 1

                logger.debug(
                    colored(
                        f"######## Run {self.run_id} ########",
                        "magenta",
                        attrs=["bold"],
                    )
                )
                with timing(f"Run {self.run_id}"):
                    # Run the app in the context of ui updates
                    if ui_updates:
                        # First apply the UI updates
                        (
                            ui_mutations,
                            ui_event_mutations,
                        ) = self.apply_ui_updates(ui_updates)
                        # Then run the app in the context of those
                        # mutations
                        num_frames = self.run(
                            ui_mutations, event_mutations=ui_event_mutations
                        )
                        logger.debug(f"{num_frames} frames ran the app.")
                    # Run the app in the context of task mutations
                    if task_mutations:
                        self.run(task_mutations)
            # Exit the thread
            if stop:
                break

    def run_loop_wrapper(self):
        """
        The entrypoint to the main loop thread. Whereas `run_loop` raises
        unhandled exceptions, `run_loop_wrapper` catches those
        exceptions, prints a stacktrace, and gracefully exits the
        thread.
        """
        try:
            self.run_loop()
        except Stop:
            pass
        except Exception as e:
            message = (
                "INTERNAL ERROR!\n"
                + dedent("".join(traceback.format_tb(e.__traceback__)))
                + f"{e.__class__.__name__}: {e}"
            )
            print(colored(message, "red"))

    def _internal_sync(self):
        """
        Only used in tests.

        Blocks until the app runner becomes idle -- input queue is empty
        and the task runner is idle.

        This method is only used in tests and assumes that while this
        method is running, no other user threads are adding items to
        the input queue. While flushing, the app runner may internally
        continue adding items to the input queue, like scheduling
        tasks or simulating ui events.
        """
        while True:
            if self.input_queue.qsize() == 0 and self.task_runtime.is_empty():
                return
            time.sleep(0.01)

    #
    # Public methods; thread-safe
    #

    def stop(self):
        """
        Enqueue a stop message, which will cause the internal thread to exit.
        """
        self.enqueue_ui_updates([(lifecycle._key, "app_stopped", True)])
        self.input_queue.put(("stop",))

    def wait(self):
        """
        Wait on the internal thread to exit.
        """
        self.thread.join()

    def enqueue_ui_updates(self, ui_updates):
        """
        Enqueue a batch of "ui updates". These are typically events
        generated by users in the browser and enqueued by
        `hyperdiv.connection.Connection`.

        They can also be simulated UI events, triggered by user code
        via `self.trigger_event`.
        """
        self.input_queue.put(
            (
                "ui_updates",
                [
                    (
                        key,
                        prop_name,
                        tuple(value) if isinstance(value, list) else value,
                    )
                    for key, prop_name, value in ui_updates
                ],
            )
        )

    def enqueue_task_mutations(self, mutations):
        """
        An async task can mutate application state. When a mutation
        happens, it is added to `input_queue`. This gives the internal
        thread the opportunity to re-run the application function in
        case the task mutated any props that the application function
        depends on.
        """
        self.input_queue.put(("task_mutations", mutations))

    def trigger_event(self, prop, value):
        """
        Simulates a UI event. Usually called by `Component.trigger_event
        """
        if not prop.is_event_prop:
            raise Exception(f"Cannot trigger event for non event prop {prop.name}")
        self.enqueue_ui_updates([(prop.key, prop.name, value)])
