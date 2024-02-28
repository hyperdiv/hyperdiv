import pytest
from ...slot import Slot
from ...test_utils import mock_frame
from ...component_base import Component
from ..boxy import Scroll, Direction, Boxy
from ..interactive import Interactive
from ..slottable import Slottable, SlotType
from ..styled import Styled, BackgroundGradient, TextGradient
from ..togglable import Togglable


def test_scroll():
    assert repr(Scroll) == "Scroll"

    assert Scroll.parse(None) is None
    assert Scroll.parse(True) is True
    assert Scroll.parse(False) is False

    assert Scroll.render(None) is None
    assert Scroll.render(True) == "auto"
    assert Scroll.render(False) == "hidden"

    with pytest.raises(Exception):
        Scroll.parse("foo")


def test_direction():
    assert repr(Direction) == "Direction"

    for v in (None, "horizontal", "vertical", "horizontal-reverse", "vertical-reverse"):
        assert Direction.parse(v) == v

    assert Direction.render(None) is None
    assert Direction.render("horizontal") == {"flex-direction": "row"}
    assert Direction.render("vertical") == {"flex-direction": "column"}
    assert Direction.render("horizontal-reverse") == {"flex-direction": "row-reverse"}
    assert Direction.render("vertical-reverse") == {"flex-direction": "column-reverse"}

    with pytest.raises(Exception):
        Direction.parse("foo")


def test_slot_type():
    assert repr(SlotType) == "SlotType"

    s = Slot(ui_name="ui-slot")
    assert SlotType.parse(None) is None
    assert SlotType.parse(s) == s

    assert SlotType.render(None) is None
    assert SlotType.render(s) == "ui-slot"

    with pytest.raises(Exception):
        SlotType.parse("my-slot")


def test_background_gradient():
    assert repr(BackgroundGradient) == "BackgroundGradient"

    assert BackgroundGradient.parse(None) is None
    assert BackgroundGradient.render(None) is None

    assert BackgroundGradient.parse((60, "red", "blue")) == (60, "red", "blue")
    assert BackgroundGradient.render((60, "red", "blue")) == {
        "background-image": "linear-gradient(60deg, var(--sl-color-red-600), var(--sl-color-blue-600))"
    }

    with pytest.raises(Exception):
        BackgroundGradient.parse((60, "red"))


def test_text_gradient():
    assert repr(TextGradient) == "TextGradient"

    assert TextGradient.parse(None) is None
    assert TextGradient.render(None) is None

    assert TextGradient.parse((60, "red", "blue")) == (60, "red", "blue")
    assert TextGradient.render((60, "red", "blue")) == {
        "background-image": "linear-gradient(60deg, var(--sl-color-red-600), var(--sl-color-blue-600))",
        "background-clip": "text",
        "-webkit-background-clip": "text",
        "color": "transparent",
    }

    with pytest.raises(Exception):
        TextGradient.parse((60, "red"))


def test_instantiation():
    for klass in (Interactive, Slottable, Styled, Boxy, Togglable):
        with pytest.raises(Exception):
            klass()


@mock_frame
def test_togglable():
    class T(Component, Togglable):
        pass

    t = T()
    assert t.opened is False
    assert t.visibility_changed is False
    assert t.was_opened is False
    assert t.was_closed is False
