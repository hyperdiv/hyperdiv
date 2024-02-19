import pytest
from ..color_constant import ColorConstant


def test_color_constant():
    assert repr(ColorConstant) == "ColorConstant"

    # hex
    for c in ("#123", "#aabb44", "#aab", "#aabc", "#aabbccdd"):
        assert ColorConstant.parse(c) == c
        assert ColorConstant.render(c) == c

    with pytest.raises(ValueError):
        ColorConstant.parse("123")

    with pytest.raises(ValueError):
        ColorConstant.parse("#aa55zz")

    with pytest.raises(ValueError):
        ColorConstant.parse("#a")

    with pytest.raises(ValueError):
        ColorConstant.parse("#ab")

    with pytest.raises(ValueError):
        ColorConstant.parse("#abcde")

    with pytest.raises(ValueError):
        ColorConstant.parse("#abcdef0")

    with pytest.raises(ValueError):
        ColorConstant.parse("#abcdef012")

    # rgb/rgba
    assert ColorConstant.parse((255, 255, 255)) == (255, 255, 255)
    assert ColorConstant.render((255, 255, 255)) == "rgb(255, 255, 255)"

    with pytest.raises(ValueError):
        ColorConstant.parse((128, 300, 111))

    with pytest.raises(ValueError):
        ColorConstant.parse((128, -20, 111))

    assert ColorConstant.parse((255, 255, 255, 0.7)) == (255, 255, 255, 0.7)
    assert ColorConstant.render((255, 255, 255, 0.7)) == "rgba(255, 255, 255, 0.7)"

    with pytest.raises(ValueError):
        ColorConstant.parse((128, 129, 111, 2))

    with pytest.raises(ValueError):
        ColorConstant.parse((128, 129, 111, -0.4))

    with pytest.raises(ValueError):
        ColorConstant.parse((128, 129))

    with pytest.raises(ValueError):
        ColorConstant.parse((128, 129, 111, 123, 123))

    with pytest.raises(ValueError):
        ColorConstant.parse("red")

    with pytest.raises(ValueError):
        ColorConstant.parse(123)
