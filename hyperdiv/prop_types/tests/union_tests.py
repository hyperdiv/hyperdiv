import pytest
from ..union import Union
from ..native import Int, PureString


def test_union():
    u = Union(Int, PureString)

    assert repr(u) == "Union[Int, PureString]"

    assert u.parse(1) == 1
    assert u.parse("Hello") == "Hello"

    with pytest.raises(TypeError):
        u.parse(dict())

    with pytest.raises(TypeError):
        u.parse(b"123")
