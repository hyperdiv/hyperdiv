from ..component_base import Component
from ..prop import Prop
from ..prop_types import Bool, OneOf, Int, CSSField, Color, HyperdivType, Size
from ..slot import Slot
from ..style_part import StylePart
from .common.shoelace_types import ShoelacePlacement


class AnchorDef(HyperdivType):
    """
    The type of a @component(popup) anchor. This type accepts Hyperdiv
    UI components.
    """

    def parse(self, value):
        if value is None:
            return None
        if not isinstance(value, Component):
            raise ValueError(f"Expected a Hyperdiv component but got {type(value)}")
        return value

    def render(self, value):
        return value._key


Anchor = AnchorDef()


class popup(Component):
    """
    A popup is an overlay that is anchored to an existing Hyperdiv component.

    Note that in most cases you probably want a @component(tooltip) or
    a @component(dropdown).

    ```py
    button = hd.button("Click Me")

    with hd.popup(
        button,
        distance=10,
        arrow=True,
        arrow_color="pink",
    ) as popup:
        with hd.box(padding=1, background_color="pink"):
            hd.text("Hello")

    if button.clicked:
        popup.opened = not popup.opened
    ```

    This example uses a popup to attach a menu to a text box,
    simulating search suggestions:

    ```py
    text_input = hd.text_input(prefix_icon="search")

    state = hd.state(suggestions=())

    with hd.popup(text_input, placement="bottom") as popup:
        with hd.menu() as menu:
            for suggestion in state.suggestions:
                with hd.scope(suggestion):
                    mi = hd.menu_item(suggestion)
                    if menu.selected_item == mi:
                        text_input.value = suggestion
                        popup.opened = False

    if text_input.changed:
        state.suggestions = (
            text_input.value + "foo",
            text_input.value + "baz"
        )
        if text_input.value:
            popup.opened = True
        else:
            popup.opened = False

    hd.button("Search")
    ```

    """

    _tag = "sl-popup"

    # The visibility of the popup.
    opened = Prop(Bool, False, ui_name="active")
    # The Hyperdiv component to which the popup is attached.
    anchor = Prop(Anchor)
    # Where, relative to the anchor, the popup is displayed.
    placement = Prop(ShoelacePlacement, "top")
    # The distance from the anchor on the placement axis, in pixels.
    distance = Prop(Int, 0)
    # The skidding perpendicular to the placement axis, in pixels.
    skidding = Prop(Int, 0)
    # Whether to display a tooltip arrow.
    arrow = Prop(Bool, False)
    arrow_placement = Prop(OneOf("start", "end", "center", "anchor"), "anchor")
    arrow_padding = Prop(Int, 10)
    # The size of the arrow.
    arrow_size = Prop(CSSField("--arrow-size", Size))
    # The color of the arrow.
    arrow_color = Prop(CSSField("--arrow-color", Color))
    # Whether to flip the popup to the other side of the anchor, to
    # remain visible for longer while scrolling out of the viewport.
    flip = Prop(Bool, False)
    flip_padding = Prop(Int, 0)
    # Whether to shift the popup, to remain visible for longer while
    # scrolling out of the viewport.
    shift = Prop(Bool, False)
    shift_padding = Prop(Int, 0)
    # Sync the popup's dimensions to those of the anchor.
    sync = Prop(OneOf("width", "height", "both"), "width")
    strategy = Prop(OneOf("absolute", "fixed"), "absolute")

    anchor_slot = Slot("anchor")

    arrow_style = Prop(StylePart("arrow"))
    popup_style = Prop(StylePart("popup"))
    hover_bridge = Prop(StylePart("hover-bridge"))

    def __init__(self, anchor, **kwargs):
        super().__init__(anchor=anchor, **kwargs)
