from .frame import AppRunnerFrame


class UICommand:
    """
    Just an in-memory representation of a command. `result_key` is the
    Hyperdiv key of the `async_command` object returned by the
    command. The UI will update the done/running/result props at this
    key when the command is done executing.
    """

    def __init__(self, result_key, target, command, args):
        self.result_key = result_key
        self.target = target
        self.command = command
        self.args = args

    def render(self):
        return dict(
            resultKey=self.result_key,
            target=self.target,
            command=self.command,
            args=self.args,
        )

    @staticmethod
    def send(result_key, target, command, args):
        """Sends a command to the UI at the end of the current frame."""
        AppRunnerFrame.current().add_command(UICommand(result_key, target, command, args))
