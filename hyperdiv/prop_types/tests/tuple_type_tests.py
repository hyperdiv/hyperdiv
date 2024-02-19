import pytest
from ..tuple_type import Tuple
from ..native import Int, PureString


def test_tuple():
    t = Tuple(Int, PureString)

    assert repr(t) == "Tuple[Int, PureString]"

    assert t.parse((1, "Hello")) == (1, "Hello")
    assert t.parse((-10, "Hello")) == (-10, "Hello")

    assert t.render((-10, "Hello")) == (-10, "Hello")

    with pytest.raises(TypeError):
        t.parse((1, 1))

    with pytest.raises(TypeError):
        t.parse(("Hello", 1))

    with pytest.raises(ValueError):
        t.parse((1, "Hello", 2))

    with pytest.raises(ValueError):
        t.parse("Hello")
