import pytest
from ..event import Event
from ..native import Bool, Int
from ..border import Border


def test_event():
    e = Event(Bool)
    assert repr(e) == "Event[Bool]"

    assert e.parse(True) is True
    assert e.render(True) is True

    e = Event(Int)
    assert repr(e) == "Event[Int]"

    assert e.parse(10) == 10
    assert e.render(-50) == -50
