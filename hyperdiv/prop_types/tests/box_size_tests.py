import pytest
from ..box_size import BoxSize


def test_box_size():
    assert repr(BoxSize) == "BoxSize"

    assert BoxSize.parse(None) is BoxSize.render(None) is None

    assert BoxSize.parse((1, 2, 3, 4)) == (
        (1, "rem"),
        (2, "rem"),
        (3, "rem"),
        (4, "rem"),
    )

    assert (
        BoxSize.render(
            (
                (1, "rem"),
                (2, "rem"),
                (3, "rem"),
                (4, "rem"),
            )
        )
        == "1rem 2rem 3rem 4rem"
    )

    assert BoxSize.parse(1) == ((1, "rem"),) * 4
    assert BoxSize.parse("1px") == ((1, "px"),) * 4
    assert BoxSize.parse((20, "%")) == ((20, "%"),) * 4

    assert BoxSize.parse((1, 2)) == ((1, "rem"), (2, "rem"), (0, "rem"), (0, "rem"))

    assert BoxSize.render(BoxSize.parse(1)) == "1rem"
    assert (
        BoxSize.render(BoxSize.parse((1, (1, "rem"), "1rem", ("1", "rem")))) == "1rem"
    )

    with pytest.raises(ValueError):
        assert BoxSize.parse((1, 2, 3, 4, 5))

    with pytest.raises(ValueError):
        assert BoxSize.parse(())
