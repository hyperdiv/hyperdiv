import re
from ..prop_types import HyperdivType, ClampedFloat, Bool, OneOf, CSSField, Size, Int
from ..prop import Prop
from ..component_base import Component
from ..slot import Slot
from ..component_mixins.styled import Styled
from ..style_part import StylePart


class SnapDef(HyperdivType):
    """
    This type defines a sequence of snap points for use in
    @component(split_panel).

    It accepts either a tuple of @prop_type(Size) values or a string
    concatenating size values by spaces. If a string is given, the
    string will be parsed into a tuple of @prop_type(Size) values.

    Examples of accepted values:

    ```py
    "50px 50% 300px"
    ("50px", "50%", "300px")
    ```

    """

    def parse(self, values):
        if values is None:
            return None
        if isinstance(values, str):
            values = re.split(r"\s+", values)
        return tuple([Size.parse(v) for v in values])

    def render(self, values):
        if values is None:
            return None
        return " ".join(Size.render(v) for v in values)


Snap = SnapDef()


class split_panel(Component, Styled):
    """
    A container that renders side by side components with a draggable
    divider between them. The divider can be dragged to increase the
    width of one component while decreasing the width of the other.

    The split panel provides the slots `start` and `end` into which
    the two components can be slotted.

    ```py
    with hd.split_panel(height=5) as sp:
        with hd.box(
            align="center",
            justify="center",
            horizontal_scroll=False,
            background_color="neutral-50",
            slot=sp.start,
        ):
            hd.text("One")
        with hd.box(
            align="center",
            justify="center",
            horizontal_scroll=False,
            background_color="neutral-50",
            slot=sp.end,
        ):
            hd.text("Two")
    ```

    ### Custom Divider

    The divider box can be customized using the `divider_style` style
    part, and custom components can be slotted into the "grip" area of
    the divider using the `divider` slot.

    ```py
    with hd.split_panel(
        height=5,
        divider_width="1px",
        divider_style=hd.style(
            background_color="green"
        )
    ) as sp:
        with hd.box(
            align="center",
            justify="center",
            horizontal_scroll=False,
            background_color="neutral-50",
            slot=sp.start,
        ):
            hd.text("One")
        with hd.box(
            align="center",
            justify="center",
            horizontal_scroll=False,
            background_color="neutral-50",
            slot=sp.end,
        ):
            hd.text("Two")
        with hd.box(slot=sp.divider):
            hd.icon("circle-fill", font_color="green")
    ```

    """

    _tag = "sl-split-panel"
    _has_direct_children = False

    # The position of the draggable divider expressed as a percentage.
    position = Prop(ClampedFloat(0, 100), 50)
    # Whether the split panel is rendered vertically. In this case,
    # the draggable divider is a horizontal divider and can be dragged
    # up and down.
    vertical = Prop(Bool, False)
    # Whether the divider can be dragged.
    disabled = Prop(Bool, False)
    # Which panel is considered the primary panel.
    primary = Prop(OneOf(None, "start", "end"))
    # The minimum size of the primary panel.
    primary_min_size = Prop(CSSField("--min", Size))
    # The maximum size of the primary panel.
    primary_max_size = Prop(CSSField("--max", Size))
    # The points to which the divider snaps while dragged.
    snap = Prop(Snap)
    # When the divider is within a certain distance from a snapping
    # point, it immediately snaps into place. This prop sets that
    # distance in pixels.
    snap_threshold = Prop(Int, 12)
    # The width of the divider.
    divider_width = Prop(CSSField("--divider-width", Size))
    # The space/area around the divider from which the divider can be
    # dragged.
    divider_hit_area = Prop(CSSField("--divider-hit-area", Size))

    start = Slot()
    end = Slot()
    divider = Slot()

    start_style = Prop(StylePart("start"))
    end_style = Prop(StylePart("end"))
    panel_style = Prop(StylePart("panel"))
    divider_style = Prop(StylePart("divider"))
