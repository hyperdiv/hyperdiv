import asyncio
from ..prop_types import Int, BoolEvent
from ..prop import Prop
from ..frame import AppRunnerFrame
from ..debug import logger
from .async_command import async_command


def run_asynchronously(result_callback, fn, *args, **kwargs):
    frame = AppRunnerFrame.current()

    if asyncio.iscoroutinefunction(fn):
        # If task is an async function, run it on the ioloop
        async def run_async_task():
            try:
                with frame.task_frame():
                    try:
                        result = await fn(*args, **kwargs)
                        result_callback(result)
                    except Exception as e:
                        logger.exception("Task Failure")
                        result_callback(error=str(e))
            except Exception as e:
                logger.exception(f"Internal Error: {e}")

        frame.run_task_on_ioloop(run_async_task())

    else:
        # If task is a regular function, run it in the threadpool
        def run_task():
            try:
                with frame.task_frame():
                    try:
                        result = fn(*args, **kwargs)
                        result_callback(result=result)
                    except Exception as e:
                        logger.exception("Task Failure")
                        result_callback(error=str(e))
            except Exception as e:
                logger.exception(f"Internal Error: {e}")

        frame.run_task_in_threadpool(run_task)


class task(async_command):
    """
    `task` enables running user functions asynchronously, without
    occupying the main UI thread. Functions doing significant work
    or waiting on I/O may be good candidates to run with `task`.

    The task function runs concurrently with the main app
    function. While a task function is running, the main app function
    can run and update the UI independently.

    The main app function can inspect the state of the running task
    using the props `running`, `done`, `error`, `result` and
    `finished`.

    The task function cannot instantiate UI components like
    @component(button) -- it cannot create UIs. However, it can update
    state. You can pass a UI or state component into the task function
    and the task can read and update its props. The updates propagate
    immediately and can cause the main app function to re-run, and
    update the UI, while the task function is still running.

    Tasks can also instantiate global state -- components defined with
    @component(global_state) -- and inspect/update the global state.

    ## Result Caching

    When running a function with `task`, the return value of the
    function will be cached in the task's `result` prop. Subsequent
    calls to `task.run` will not re-run the function, unless you call
    `rerun` or `clear`. Clearing a task will cause a subsequent call
    to `run()` to run the function again.

    In this example, when we click `Update`, the app-reruns, and since
    the task is cleared, `task.run(get_timestamp)` will run the
    `get_timestamp` function again.

    ```py
    def get_timestamp():
        import time
        return time.time()

    task = hd.task()
    task.run(get_timestamp)

    hd.text("Last timestamp:", task.result)

    if hd.button("Update").clicked:
        task.clear()
    ```

    ## Using `rerun`

    As an alternative to using `run` and `clear`, you can use `rerun`,
    which clears the task and reruns the task function. `rerun` should
    be run only in response to an event, like a click or a change
    event.

    ```py
    def increment(state):
        state.count += 1

    state = hd.state(count=0)

    task = hd.task()

    hd.text("Count:", state.count)

    if hd.button("Increment").clicked:
        task.rerun(increment, state)
    ```

    ## Async Functions

    `task` supports both normal functions and `async def`
    functions. Normal functions are run in a threadpool, and `async
    def` functions are run on an ioloop which runs on a separate
    "ioloop thread".

    ```py
    async def my_function(state):
        import asyncio
        await asyncio.sleep(1)
        state.count += 1

    state = hd.state(count=0)

    task = hd.task()

    hd.text("Count:", state.count)

    if hd.button(
        "Increment",
        disabled=task.running
    ).clicked:
        task.rerun(my_function, state)
    ```

    Whenever you click the button, a task is launched that increments
    the count one second later. This example also shows how to use the
    task state to display different UI states. In this case, the
    button is disabled while the task is running.

    ## Displaying Interstitials

    The task state can be used to display "Loading" interstitials
    while the task is running.

    ```py
    async def get_users():
        import asyncio
        await asyncio.sleep(1)
        return ["Billy", "Molly"]

    users_task = hd.task()
    users_task.run(get_users)

    if hd.button("Load").clicked:
        users_task.clear()

    if not users_task.done:
        hd.spinner()
    else:
        hd.text(users_task.result)
    ```

    ## Concurrency

    Tasks run concurrently with each other and the app function. Prop
    reads and writes are automatically protected by a lock, but you
    may need to use your own locks if you need coarser-granularity
    locking. You can store a lock in state and pass that state to tasks.

    """

    _run_number = Prop(Int, 0)
    finished = Prop(BoolEvent, False)

    def __init__(self, *, key=None):
        super().__init__(key=key)

    def run(self, fn, *args, **kwargs):
        """
        Run `fn(*args, **kwargs)` on a separate thread (or ioloop if the
        function is `async`).
        """

        run_number = self._run_number

        def result_callback(result=None, error=None):
            if self._run_number != run_number:
                logger.warn(
                    f"The task {fn}({args}, {kwargs}) was cleared/restarted "
                    "before the previous run could finish."
                )
                return
            self.result = result
            self.error = error
            self.done = True
            self.running = False
            self.trigger_event("finished", True)

        if not self.running and not self.done:
            self.running = True
            run_asynchronously(result_callback, fn, *args, **kwargs)

    def rerun(self, fn, *args, **kwargs):
        """Just like `run` but calls `self.clear()` before running."""

        self.clear()
        self.run(fn, *args, **kwargs)

    def clear(self):
        """
        Resets the props of the task to initial values. If the task is
        `done`, clearing it will allow it to run again. Note that if
        an instance of the task is running at the time `clear()` is
        called, that instance will be ignored, but it will still run
        to completion.

        Note that the `result` prop is not cleared, allowing the app
        to keep rendering the previous result until the `result` prop
        is updated with the data of the new run.
        """

        if self.running:
            logger.warn("Clearing running task.")
        self._run_number += 1
        super().clear()
