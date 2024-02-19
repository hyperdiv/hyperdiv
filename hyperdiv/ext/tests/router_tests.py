from ...test_utils import MockRunner
from ...components.plaintext import plaintext
from ..router import router

r = router()


@r.route("/foo", redirect_from="/")
def foo_route():
    plaintext("Foo")


@r.route("/bar")
def bar_route():
    plaintext("Bar")


@r.route("/baz")
def baz_route():
    r.render_not_found()


@r.not_found
def not_found():
    plaintext("Not Found")


def my_app():
    r.run()


def test_router():
    with MockRunner(my_app) as mr:
        # Initially it renders not found
        last_msg = mr.connection.msgs[-1]
        assert last_msg["dom"]["children"][0]["props"]["content"] == "Foo"

        # Update the path to /foo
        mr.process_updates([("location", "path", "/foo")])

        # Nothing happened, because redirect_from already redirected to '/foo'
        assert len(mr.connection.msgs) == 1

        mr.process_updates([("location", "path", "/bar")])

        last_msg = mr.connection.msgs[-1]
        chunks = list(last_msg["diff"].values())[0]["children"]
        # The diff removes the "Foo" text
        assert chunks[0] == ("delete", 0, 1)
        # And replaces it with "Bar"
        assert chunks[1][2][0]["props"]["content"] == "Bar"

        mr.process_updates([("location", "path", "/baz")])

        last_msg = mr.connection.msgs[-1]
        chunks = list(last_msg["diff"].values())[0]["children"]
        # The diff removes the "Foo" text
        assert chunks[0] == ("delete", 0, 1)
        # And replaces it with "Bar"
        assert chunks[1][2][0]["props"]["content"] == "Not Found"
