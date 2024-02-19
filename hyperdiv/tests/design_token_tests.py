import pytest
from ..design_tokens import (
    TokenEnum,
    Spacing,
    Shadow,
    BorderRadius,
    FontFamily,
    FontSize,
    FontWeight,
    LetterSpacing,
    LineHeight,
    Color,
)


class MyToken(TokenEnum):
    foo = "foo"
    bar = "bar"


def test_design_tokens():
    assert MyToken.values() == ["foo", "bar"]

    with pytest.raises(Exception):
        MyToken.foo.render()

    assert Spacing.three_x_small.render() == "var(--sl-spacing-3x-small)"
    assert Shadow.x_large.render() == "var(--sl-shadow-x-large)"
    assert BorderRadius.circle.render() == "var(--sl-border-radius-circle)"
    assert FontFamily.sans_serif.render() == "var(--sl-font-sans)"
    assert FontFamily.mono.render() == "var(--sl-font-mono)"
    assert FontSize.three_x_large.render() == "var(--sl-font-size-3x-large)"
    assert FontWeight.bold.render() == "var(--sl-font-weight-bold)"
    assert LetterSpacing.looser.render() == "var(--sl-letter-spacing-looser)"
    assert LineHeight.looser.render() == "var(--sl-line-height-looser)"
    assert Color.red.render() == "var(--sl-color-red-600)"
    assert Color.red_600.render() == "var(--sl-color-red-600)"
