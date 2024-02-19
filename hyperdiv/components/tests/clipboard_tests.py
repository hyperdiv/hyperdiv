from ...test_utils import mock_frame
from ..clipboard import clipboard


@mock_frame
def test_clipboard():
    c = clipboard()

    assert c._key == "clipboard"

    c.write("Hello")
    assert c._value == "Hello"
