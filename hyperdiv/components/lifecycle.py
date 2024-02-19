from ..prop import Prop
from ..prop_types import BoolEvent
from ..ui_singleton import Singleton


class lifecycle(Singleton):
    """
    The `lifecycle` component gives you the opportunity to execute
    one-time actions when the app starts or stops.

    For example you can allocate resources on app start, and
    de-allocate them before the app exits.

    Or if you have long-running @component(task)s you can signal those
    tasks to exit. The app won't cleanly shut down if there are
    lingering tasks still executing.

    ```py-nodemo

    def my_task(state):
        state.running = True

        while state.running:
            do_something()

    def app():
        state = hd.state(running=False)

        task = hd.task()
        task.run(my_task, state)

        lifecycle = hd.lifecycle()
        if lifecycle.app_stopped:
            state.running = False
    ```

    Note that if the app function crashes, the code that is supposed
    to execute on `app_stopped` may not be executed.
    """

    _key = "lifecycle"

    # True for one frame when the app just started.
    app_started = Prop(BoolEvent, False)
    # True for one frame when the app is about to exit.
    app_stopped = Prop(BoolEvent, False)
