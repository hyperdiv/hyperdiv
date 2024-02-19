import pytest
from ..optional import Optional
from ..native import Int
from ..base_size import BaseSize


def test_optional():
    o = Optional(Int)

    assert repr(o) == "Optional[Int]"

    assert o.parse(None) is None
    assert o.parse(1) == 1

    with pytest.raises(TypeError):
        o.parse("Hello")

    o = Optional(BaseSize)
    assert o.parse(None) is None
    assert o.render(None) is None
    assert o.parse("12rem") == BaseSize.parse("12rem")
    assert o.render(o.parse("12rem")) == BaseSize.render(BaseSize.parse("12rem"))
