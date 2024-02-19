import pytest
from ..base_size import parse_number, BaseSize


def test_base_size():
    assert repr(BaseSize) == "BaseSize"

    assert BaseSize.parse(None) is BaseSize.render(None) is None

    assert BaseSize.parse(1) == (1, "rem")
    assert BaseSize.parse((1, "rem")) == (1, "rem")
    assert BaseSize.parse("1rem") == (1, "rem")
    assert BaseSize.render((1, "rem")) == "1rem"

    assert BaseSize.parse("1") == (1, "rem")
    assert BaseSize.parse("1.234") == (1.234, "rem")

    assert BaseSize.parse("50%") == (50, "%")
    assert BaseSize.render((50, "%")) == "50%"

    for unit in ("em", "px", "vh", "vw", "rem"):
        assert BaseSize.parse(f"20{unit}")
        assert BaseSize.render((20, unit)) == f"20{unit}"

    assert (
        BaseSize.parse("fit-content") == BaseSize.render("fit-content") == "fit-content"
    )

    assert BaseSize.parse(("1", "px")) == (1, "px")

    with pytest.raises(ValueError):
        BaseSize.parse(("bunnies", "px"))

    with pytest.raises(Exception):
        BaseSize.parse("-20%")

    with pytest.raises(Exception):
        BaseSize.parse("em")

    with pytest.raises(Exception):
        BaseSize.parse("100blem")

    with pytest.raises(ValueError):
        BaseSize.parse({"x": 1})

    with pytest.raises(ValueError):
        BaseSize.parse([])


def test_parse_number():
    assert parse_number("10") == 10
    assert parse_number("1.234") == 1.234
    assert parse_number("-1.234") == -1.234

    with pytest.raises(ValueError):
        parse_number("10", low=11)

    with pytest.raises(ValueError):
        parse_number("10", high=9)
