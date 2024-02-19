from ...test_utils import MockRunner, mock_frame
from ..local_storage import local_storage
from ..plaintext import plaintext
from ..button import button


def test_get_item():
    cmd_key = None
    text_key = None

    def app():
        nonlocal cmd_key, text_key

        cmd = local_storage.get_item("items")
        cmd_key = cmd._key

        text = plaintext(cmd.result)
        text_key = text._key

    with MockRunner(app) as mr:
        msg = mr.connection.msgs[-1]
        child = msg["dom"]["children"][0]
        assert child["key"] == text_key
        assert child["props"]["content"] == "None"

        mr.process_updates(
            [
                (cmd_key, "done", True),
                (cmd_key, "running", False),
                (cmd_key, "result", "Bunnies"),
            ]
        )

        msg = mr.connection.msgs[-1]
        assert text_key in msg["diff"]
        assert msg["diff"][text_key]["props"]["content"] == "Bunnies"


def test_has_item():
    cmd_key = None
    text_key = None

    def app():
        nonlocal cmd_key, text_key

        cmd = local_storage.has_item("items")
        cmd_key = cmd._key

        text = plaintext(cmd.result)
        text_key = text._key

    with MockRunner(app) as mr:
        msg = mr.connection.msgs[-1]
        child = msg["dom"]["children"][0]
        assert child["key"] == text_key
        assert child["props"]["content"] == "None"

        mr.process_updates(
            [
                (cmd_key, "done", True),
                (cmd_key, "running", False),
                (cmd_key, "result", True),
            ]
        )

        msg = mr.connection.msgs[-1]
        assert text_key in msg["diff"]
        assert msg["diff"][text_key]["props"]["content"] == "True"


def test_set_item():
    def app():
        local_storage.set_item("foo", "bar")

    with MockRunner(app) as mr:
        msg = mr.connection.msgs[-1]
        cmd = msg["commands"][0]
        assert cmd["command"] == "setItem"
        assert cmd["args"] == ["foo", "bar"]


def test_remove_item():
    def app():
        local_storage.remove_item("foo")

    with MockRunner(app) as mr:
        msg = mr.connection.msgs[-1]
        cmd = msg["commands"][0]
        assert cmd["command"] == "removeItem"
        assert cmd["args"] == ["foo"]


def test_clear():
    def app():
        local_storage.clear()

    with MockRunner(app) as mr:
        msg = mr.connection.msgs[-1]
        cmd = msg["commands"][0]
        assert cmd["command"] == "clear"
        assert cmd["args"] == []
