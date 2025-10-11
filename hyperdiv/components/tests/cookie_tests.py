from ...test_utils import MockRunner
from ..cookies import cookies
from ..plaintext import plaintext


def test_get_cookie():
    cmd_key = None
    text_key = None

    def app():
        nonlocal cmd_key, text_key

        cmd = cookies.get_cookie("items")
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


def test_set_cookie():
    def app():
        cookies.set_cookie("foo", "bar")

    with MockRunner(app) as mr:
        msg = mr.connection.msgs[-1]
        cmd = msg["commands"][0]
        assert cmd["command"] == "setCookie"
        assert cmd["args"][:2] == ["foo", "bar"]
        assert cmd["args"][2] == dict(max_age=None, secure=False, same_site="lax")


def test_set_cookie_args():
    def app():
        cookies.set_cookie("foo", "bar", max_age=20, secure=True, same_site="strict")

    with MockRunner(app) as mr:
        msg = mr.connection.msgs[-1]
        cmd = msg["commands"][0]
        assert cmd["command"] == "setCookie"
        args = cmd["args"]
        assert args[0] == "foo"
        assert args[1] == "bar"
        assert args[2] == dict(max_age=20, secure=True, same_site="strict")


def test_remove_cookie():
    def app():
        cookies.remove_cookie("foo")

    with MockRunner(app) as mr:
        msg = mr.connection.msgs[-1]
        cmd = msg["commands"][0]
        assert cmd["command"] == "removeCookie"
        assert cmd["args"][:1] == ["foo"]
