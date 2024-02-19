import pytest
from ..time_value import TimeValue


def test_time_value():
    assert repr(TimeValue) == "TimeValue"

    assert TimeValue.parse("12ms") == (12, "ms")
    assert TimeValue.parse("+12ms") == (12, "ms")
    assert TimeValue.parse("-12ms") == (-12, "ms")

    assert TimeValue.parse("12s") == (12, "s")
    assert TimeValue.parse("+12s") == (12, "s")
    assert TimeValue.parse("-12s") == (-12, "s")

    assert TimeValue.parse((12, "s")) == (12, "s")
    assert TimeValue.parse((-12, "s")) == (-12, "s")

    with pytest.raises(ValueError):
        TimeValue.parse((1, "s", 2))

    with pytest.raises(ValueError):
        TimeValue.parse((1, "m"))

    with pytest.raises(ValueError):
        TimeValue.parse(("1", "s"))

    assert TimeValue.render((12, "ms")) == "12ms"
    assert TimeValue.render((-12, "ms")) == "-12ms"
    assert TimeValue.render((12, "s")) == "12s"
    assert TimeValue.render((-12, "s")) == "-12s"
