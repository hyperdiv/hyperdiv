from ...test_utils import mock_frame
from ..markdown import markdown


@mock_frame
def test_markdown():
    m = markdown("# Hello")
    assert m.render()["props"]["content"] == "<h1>Hello</h1>"


@mock_frame
def test_code():
    m = markdown(
        """
        ```py
        def add(x, y):
            return x + y
        ```
        """
    )
    assert m.render()["props"]["content"].startswith('<div class="codehilite"')


@mock_frame
def test_unknown_lexer():
    m = markdown(
        """
        ```unknown
        def add(x, y):
            return x + y
        ```
        """
    )
    assert m.render()["props"]["content"].startswith('<div class="codehilite"')


@mock_frame
def test_no_lexer():
    m = markdown(
        """
        ```
        def add(x, y):
            return x + y
        ```
        """
    )
    assert m.render()["props"]["content"].startswith('<div class="codehilite"')
