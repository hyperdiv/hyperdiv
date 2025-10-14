from .frame import AppRunnerFrame
from .components.async_command import async_command


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
        AppRunnerFrame.current().add_command(
            UICommand(result_key, target, command, args)
        )


def ui_read(target, command, args):
    """Invoke a UI read command. A read will send the command to the UI
    and return a result object in `running` state. Calling this read
    again on subsequent frames will *not* re-send the read call to the
    UI. It will remain in `done` state and return the same value over
    and over.

    To trigger a re-read, you can call `clear()` on the returned
    `async_command` object, which resets the running/done props and causes
    the read to be sent again on the next frame.
    """

    result = async_command()

    sent = False

    if not result.running and not result.done:
        UICommand.send(result._key, target, command, args)
        result.running = True
        sent = True

    return result, sent


def ui_write(target, command, args):
    """Invoke a UI write command. Unlike a read, a write call will send
    the command to the UI on every call. Intuitively, writes should
    not be called on every frame, but rather only in response to
    events like `clicked`.

    Writes still return a `async_command` object that can be inspected to
    determine the status of the write. However, note that if you
    immediately invoke the same write again, before the previous has
    finished, the `async_command` object will likely be updated by the 1st
    (unfinished) call, and then again by the 2nd.
    """
    result = async_command()
    result.clear()

    UICommand.send(result._key, target, command, args)

    result.running = True

    return result


class UICommandCache:
    """
    A generic cache that stores UI command objects in Hyperdiv
    session storage.
    """

    def __init__(self, storage_key):
        self.storage_key = storage_key

    def cache_result(self, key, result):
        storage = AppRunnerFrame.current().get_storage(self.storage_key)

        storage.setdefault(key, [])
        storage[key].append(result)

    def clear_cache_at_key(self, key):
        storage = AppRunnerFrame.current().get_storage(self.storage_key)

        read_results = storage.get(key, [])
        for read_result in read_results:
            read_result.clear()

    def clear_cache(self):
        storage = AppRunnerFrame.current().get_storage(self.storage_key)

        for read_results in storage.values():
            for read_result in read_results:
                read_result.clear()
