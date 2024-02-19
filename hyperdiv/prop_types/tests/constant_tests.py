import pytest
from ..constant import Constant


def test_constant():
    c = Constant(10)

    assert repr(c) == "Constant[10]"

    assert c.parse(10) == c.render(10) == 10

    with pytest.raises(ValueError):
        c.parse(20)
