from ..prop_types import Bool, CSSField, Color, Size
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.styled import Styled


class divider(Component, Styled):
    """
    A horizontal or vertical divider used to add visual separation
    between components.

    ```py
    with hd.box():
        hd.text("Item One")
        hd.divider(spacing=0.5)
        hd.text("Item Two")
    ```

    To use a divider in a horizontal box, pass `vertical=True` to
    render a vertical divider.

    ```py
    with hd.hbox():
        hd.text("Item One")
        hd.divider(vertical=True, spacing=1)
        hd.text("Item Two")
    ```

    """

    _tag = "sl-divider"
    _has_direct_children = False

    # Whether the divider should be rendered vertically.
    vertical = Prop(Bool, False)
    # The color of the divider.
    color = Prop(CSSField("--color", Color))
    # The thickness of the divider.
    thickness = Prop(CSSField("--width", Size))
    # The spacing around the divider.
    spacing = Prop(CSSField("--spacing", Size), 0)
