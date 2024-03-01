import pytest
from ...test_utils import mock_frame
from ..button import button
from ..popup import popup, Anchor
from ..text import text


@mock_frame
def test_anchor_type():
    b = button("Click Me")
    assert Anchor.parse(b) == b
    assert Anchor.render(b) == b._key

    with pytest.raises(Exception):
        Anchor.parse("Hello")


@mock_frame
def test_popup():
    b = button("Click Me")
    with popup(b) as p:
        text("Hello")

    assert p.anchor == b
