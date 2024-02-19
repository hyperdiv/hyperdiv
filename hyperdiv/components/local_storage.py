from ..frame import AppRunnerFrame
from ..ui_command import UICommand
from .async_command import async_command


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


class local_storage:
    """
    A Hyperdiv interface to browser localStorage. Using this interface,
    you can read and write data into the user's browser, and this data
    persists across app visits. `local_storage` can be used to
    implement authentication and store various user settings.

    Each `local_storage` function returns an @component(async_command)
    component. The `async_command` can be used to inspect whether the
    function is still running, and its return value if it is done
    running.

    `local_storage` maintains an internal cache of
    @component(async_command) objects that have been returned by reads
    (`get_item` and `has_item`). The cache is keyed by the local
    storage key. When a write (`set_item`, `remove_item`) is invoked
    at that key, the related `async_command` objects will be reset. This
    will trigger corresponding reads to re-run and get the new values.

    When `clear()` is called, all keys are removed from localStorage
    and the cache, and all reads re-run.

    ```py
    command = hd.local_storage.get_item("test_key")

    hd.markdown("`test_key` value:", command.result)

    if hd.button("Set key").clicked:
        hd.local_storage.set_item("test_key", "Bunnies")

    if hd.button("Remove key").clicked:
        hd.local_storage.remove_item("test_key")
    ```

    """

    # A cache that remembers results from previous local storage reads
    # (`get_item` and `has_item` calls). When a write is invoked on a
    # key that has been read before, those results are cleared,
    # triggering a re-read.

    _storage_key = "local_storage_result_cache"

    def __init__(self):
        """
        Unlike typical Hyperdiv components, `local_storage` cannot be
        instantiated. All methods are static.
        """
        raise Exception("local_storage cannot be instantiated.")

    @staticmethod
    def _cache_result(key, result):
        storage = AppRunnerFrame.current().get_storage(local_storage._storage_key)

        storage.setdefault(key, [])
        storage[key].append(result)

    @staticmethod
    def _clear_cache_at_key(key):
        storage = AppRunnerFrame.current().get_storage(local_storage._storage_key)

        read_results = storage.get(key, [])
        for read_result in read_results:
            read_result.clear()

    @staticmethod
    def _clear_cache():
        storage = AppRunnerFrame.current().get_storage(local_storage._storage_key)

        for read_results in storage.values():
            for read_result in read_results:
                read_result.clear()

    #
    # Local storage reads.
    #

    @staticmethod
    def get_item(key):
        """
        Calls the browser's `window.localStorage.getItem(key)`.
        """
        result, sent = ui_read("localStorage", "getItem", [key])
        if sent:
            local_storage._cache_result(key, result)
        return result

    @staticmethod
    def has_item(key):
        """
        Tests if a key exists in the browser's localStorage. The returned
        @component(async_command)'s `result` prop is set to `True` if the
        given key exists in the browser's localStorage, or `False`
        otherwise.
        """
        result, sent = ui_read("localStorage", "hasItem", [key])
        if sent:
            local_storage._cache_result(key, result)
        return result

    #
    # Local storage writes.
    #

    @staticmethod
    def set_item(key, value):
        """
        Calls the browser's `window.localStorage.setItem(key, value)`.
        """

        if not isinstance(value, str):
            raise ValueError("local_storage.set_item can only store strings.")

        result = ui_write("localStorage", "setItem", [key, value])

        local_storage._clear_cache_at_key(key)

        return result

    @staticmethod
    def remove_item(key):
        """
        Calls the browser's `window.localStorage.removeItem(key)`.
        """
        result = ui_write("localStorage", "removeItem", [key])

        local_storage._clear_cache_at_key(key)

        return result

    @staticmethod
    def clear():
        """
        Calls the browser's `window.localStorage.clear()`, removing all the
        keys from localStorage.
        """
        result = ui_write("localStorage", "clear", [])

        local_storage._clear_cache()

        return result
