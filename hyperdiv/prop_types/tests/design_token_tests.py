import pytest
from ..design_token import DesignToken
from ...design_tokens import Color


def test_design_token():
    d = DesignToken(Color)
    assert repr(d) == f"DesignToken[{Color}]"

    assert d.parse("red") == "red"
    assert d.render("red") == "var(--sl-color-red-600)"

    assert d.parse(Color.red) == "red"
    assert d.parse(Color.red_600) == "red-600"

    with pytest.raises(ValueError):
        d.parse("bunnies")

    with pytest.raises(ValueError):
        DesignToken(int)
