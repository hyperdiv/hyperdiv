from ..component_base import BaseState
from ..prop import Prop
from ..prop_types import Bool, Optional, String, Any


class async_command(BaseState):
    """
    This component represents the result of calling an asynchronous
    command. This component is not usable directly, so there is no
    user-facing need to ever instantiate it.

    It is used by @component(local_storage) and @component(task). When
    calling a @component(local_storage) function, it returns an
    `async_command` instance. @component(task) inherits
    `async_command`.

    This component can be used to inspect the status of calling an
    asynchronous command, whether it is using @component(task) to call
    a user-defined asynchronous function, or calling a built-in
    @component(local_storage) function.

    ```py
    command = hd.local_storage.get_item("test_key")
    if command.running:
        hd.spinner()
    elif command.done:
        hd.text(command.result)
    ```

    """

    # Whether the asynchronous command is currently running and has
    # not yet finished.
    running = Prop(Bool, False)
    # Whether the asynchronous command has run and finished.
    done = Prop(Bool, False)
    # Whether the asynchronous command has run and finished with an error.
    error = Prop(Optional(String))
    # The return value of the asynchronous command, if it has finished
    # without an error.
    result = Prop(Any)

    def clear(self):
        """
        Resets the `done`, `running`, and `error` props, bringing the
        command to initial state allowing it to re-run.
        """
        self.reset_prop("done")
        self.reset_prop("running")
        self.reset_prop("error")
