import pytest
from ..native import Native


def test_native():
    nat = Native(int, coercible_types=[str])

    assert nat.parse("1") == 1
    assert nat.parse("0") == 0
    assert nat.parse(10) == 10

    with pytest.raises(ValueError):
        nat.parse("Hello")

    with pytest.raises(TypeError):
        nat.parse(dict())

    assert repr(nat) == "Int"
