import pytest
from ..border_edge import BorderEdge


def test_border_edge():
    assert repr(BorderEdge) == "BorderEdge"

    assert BorderEdge.parse(None) is BorderEdge.render(None) is None
    assert BorderEdge.parse("none") == BorderEdge.render("none") == "none"

    assert (
        BorderEdge.parse("1 solid red")
        == BorderEdge.parse((1, "solid", "red"))
        == BorderEdge.parse(((1, "rem"), "solid", "red"))
        == ((1, "rem"), "solid", "red")
    )
    assert BorderEdge.parse("1 dotted red") == ((1, "rem"), "dotted", "red")
    assert BorderEdge.parse("20% dashed green-200") == (
        (20, "%"),
        "dashed",
        "green-200",
    )

    assert (
        BorderEdge.render(((1, "rem"), "solid", "red"))
        == "1rem solid var(--sl-color-red-600)"
    )

    with pytest.raises(ValueError):
        BorderEdge.parse("1 hello red")

    with pytest.raises(ValueError):
        BorderEdge.parse("1 solid red green")

    with pytest.raises(ValueError):
        BorderEdge.parse("1 solid")
