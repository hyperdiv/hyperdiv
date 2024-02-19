import pytest
from ..border import Border


def test_border():
    assert repr(Border) == "Border"

    assert Border.parse(None) is Border.render(None) is None
    assert Border.parse("none") == "none"
    assert Border.render("none") == {"border": "none"}

    assert Border.parse("1px solid red") == (((1, "px"), "solid", "red"),) * 4
    assert Border.render((((1, "px"), "solid", "red"),) * 4) == {
        "border": "1px solid var(--sl-color-red-600)"
    }

    assert Border.parse(
        (
            "1px solid red",
            "10px solid green",
            "3em dashed blue",
            "50% dotted fuchsia-100",
        )
    ) == (
        ((1, "px"), "solid", "red"),
        ((10, "px"), "solid", "green"),
        ((3, "em"), "dashed", "blue"),
        ((50, "%"), "dotted", "fuchsia-100"),
    )

    assert Border.render(
        (
            ((1, "px"), "solid", "red"),
            ((10, "vh"), "solid", "green"),
            ((3, "em"), "dashed", "blue"),
            ((50, "%"), "dotted", "fuchsia-100"),
        )
    ) == {
        "border-top": "1px solid var(--sl-color-red-600)",
        "border-right": "10vh solid var(--sl-color-green-600)",
        "border-bottom": "3em dashed var(--sl-color-blue-600)",
        "border-left": "50% dotted var(--sl-color-fuchsia-100)",
    }

    assert Border.parse(("1px solid red", "10vh solid green", "3em dashed blue")) == (
        ((1, "px"), "solid", "red"),
        ((10, "vh"), "solid", "green"),
        ((3, "em"), "dashed", "blue"),
        None,
    )

    assert Border.parse(("1px solid red", "10vh solid green")) == (
        ((1, "px"), "solid", "red"),
        ((10, "vh"), "solid", "green"),
        None,
        None,
    )

    assert Border.parse(("1px solid red",)) == (
        ((1, "px"), "solid", "red"),
        None,
        None,
        None,
    )

    assert Border.render(
        (
            ((1, "px"), "solid", "red"),
            None,
            None,
            None,
        )
    ) == {"border-top": "1px solid var(--sl-color-red-600)"}

    assert Border.render(
        Border.parse(
            (
                "1px solid red",
                "1px solid red",
                "1px solid red",
                "1px solid red",
            )
        )
    ) == {"border": "1px solid var(--sl-color-red-600)"}

    with pytest.raises(ValueError):
        Border.parse(
            (
                "1px solid red",
                "10px solid green",
                "3em dashed blue",
                "50% dotted fuchsia-100",
                "50% dotted fuchsia-100",
            )
        )

    with pytest.raises(ValueError):
        Border.parse(())
