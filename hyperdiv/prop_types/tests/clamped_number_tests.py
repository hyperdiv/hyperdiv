import pytest
from ..clamped_number import ClampedNumber


def test_clamped_number():
    c = ClampedNumber(int, low=0, high=10)
    assert c.parse(5) == c.render(5) == 5

    with pytest.raises(ValueError):
        c.parse(-1)
    with pytest.raises(ValueError):
        c.parse(11)

    assert repr(c) == "ClampedNumber[Int, 0, 10]"

    c = ClampedNumber(float)
    assert repr(c) == "ClampedNumber[Float, -inf, +inf]"

    with pytest.raises(ValueError):
        ClampedNumber(str)
