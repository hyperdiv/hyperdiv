import pytest
from ..test_utils import mock_frame
from ..components.style import style
from ..components.button import button
from ..style_part import StylePart


@mock_frame
def test_style_part():
    # None case
    b = button(label_style=None)
    assert b.label_style is None

    # Non-style case
    with pytest.raises(Exception):
        button(label_style=10)

    # Basic case, does not add `display:flex` or direction.
    b = button(label_style=style(width=10))

    rendered = b.render()
    assert rendered["style"][f"#{b._key}::part(label)"] == "width:10rem"

    # Test that 'display:flex' and 'direction' are automatically added:
    b = button(label_style=style(width=10, align="center"))

    rendered = b.render()

    style_items = set(rendered["style"][f"#{b._key}::part(label)"].split(";"))

    assert style_items == set(
        [
            "display:flex",
            "width:10rem",
            "align-items:center",
            "flex-direction:column",
        ]
    )

    # Test that direction is correctly taken into account:
    b = button(label_style=style(width=10, align="center", direction="horizontal"))

    rendered = b.render()

    style_items = set(rendered["style"][f"#{b._key}::part(label)"].split(";"))

    assert style_items == set(
        [
            "display:flex",
            "width:10rem",
            "align-items:center",
            "flex-direction:row",
        ]
    )
