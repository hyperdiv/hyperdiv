import threading
from functools import wraps
from .app_runner import AppRunner
from .task_runtime import TaskRuntime
from .frame import Frame


class MockFrame(Frame):
    def get_state(self, key, prop_name):
        return self._app_runner.state._get(key, prop_name)

    def update_state(self, key, prop_name, value):
        return self._app_runner.state._update(key, prop_name, value)


class MockTaskRuntime:
    def __init__(self):
        self.ioloop_fns = []
        self.threadpool_fns = []

    def run_on_ioloop(self, fn):
        self.ioloop_fns.append(fn)

    def run_in_threadpool(self, fn):
        self.threadpool_fns.append(fn)


class MockConnection:
    def __init__(self):
        self.msgs = []
        self.has_message = threading.Event()

    def send(self, msg):
        self.msgs.append(msg)
        self.has_message.set()


mock_initial_updates = [
    ("location", "path", "/"),
    ("location", "query_args", ""),
    ("location", "hash_arg", ""),
    ("theme", "mode", "dark"),
    ("theme", "system_mode", "dark"),
    ("window", "width", 840),
    ("window", "height", 998),
]


class MockRunner:
    """
    This mock runner starts the AppRunner thread.

    When you call `process_updates()`, the updates are enqueued, which
    triggers the thread to start processing them. The call blocks
    until the updates are fully processed.
    """

    def __init__(self, fn, initial_updates=None):
        self.initial_updates = initial_updates or mock_initial_updates
        self.fn = fn
        self.app_runner = None
        self.task_runtime = None
        self.connection = None

    def __enter__(self):
        self.connection = MockConnection()
        self.task_runtime = TaskRuntime(10)
        self.app_runner = AppRunner(
            self.connection, self.task_runtime, self.fn, self.initial_updates
        )
        self.app_runner.start()
        self.app_runner._internal_sync()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.app_runner.stop()
        self.app_runner.wait()
        self.task_runtime.shutdown()

    def process_updates(self, updates):
        self.app_runner.enqueue_ui_updates(updates)
        self.app_runner._internal_sync()

    def get_state(self, key, prop_name):
        with MockFrame(self.app_runner) as frame:
            return frame.get_state(key, prop_name)


class MockManualRunner:
    """
    This mock runner does not start the AppRunner thread. You can call
    advance() to manually do one run a time. The run runs
    synchronously on the caller thread.
    """

    def __init__(self, fn=None, initial_updates=None):
        self.task_runtime = MockTaskRuntime()
        self.connection = MockConnection()
        self.app_runner = AppRunner(
            self.connection,
            self.task_runtime,
            fn or (lambda: None),
            initial_updates if initial_updates is not None else mock_initial_updates,
        )
        self.app_runner.enqueue_ui_updates(self.app_runner.initial_ui_updates)

    def process_updates(self, updates):
        self.app_runner.enqueue_ui_updates(updates)
        self.advance()

    def process_task_mutations(self, mutations):
        self.app_runner.enqueue_task_mutations(mutations)
        self.advance()

    def update_state(self, key, prop_name, value):
        with MockFrame(self.app_runner) as frame:
            frame.update_state(key, prop_name, value)

    def get_state(self, key, prop_name):
        with MockFrame(self.app_runner) as frame:
            return frame.get_state(key, prop_name)

    def advance(self):
        self.app_runner.stop()
        self.app_runner.run_loop()


def mock_frame(fn):
    @wraps(fn)
    def wrapper():
        mr = MockManualRunner(fn)
        mr.advance()

    return wrapper
