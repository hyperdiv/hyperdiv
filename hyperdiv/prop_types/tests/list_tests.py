import pytest
from ..list_type import List
from ..native import Int, PureString


def test_list():
    l = List(Int)
    assert repr(l) == "List[Int]"

    assert l.parse((1, 2, 3)) == (1, 2, 3)
    assert l.render((1, 2, 3)) == (1, 2, 3)

    with pytest.raises(TypeError):
        l.parse((1.2, 1.3))

    l = List(PureString)

    assert l.parse(["A", "B"]) == ("A", "B")
    assert l.render(("A", "B")) == ("A", "B")

    with pytest.raises(TypeError):
        l.parse((1, 2))

    with pytest.raises(ValueError):
        l.parse(1)
