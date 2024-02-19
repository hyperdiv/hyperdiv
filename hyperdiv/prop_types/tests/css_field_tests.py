import pytest
from ..css_field import CSSField
from ..native import Int
from ..base_size import BaseSize


def test_css_field():
    f = CSSField("hello", Int)
    assert repr(f) == 'CSSField["hello":Int]'
    assert f.parse(10) == 10
    assert f.render(10) == {"hello": 10}

    f = CSSField("border", BaseSize)
    assert f.parse(10) == (10, "rem")
    assert f.render((10, "rem")) == {"border": "10rem"}
