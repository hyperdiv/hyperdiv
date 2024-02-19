from ..prop_types import Bool, OneOf
from ..prop import Prop
from ..slot import Slot
from ..component_mixins.togglable import Togglable
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text
from .text import text


class drawer(LabelComponent, Togglable):
    """
    A drawer is an overlay container that slides in from the sides of
    the viewport. A drawer has a title and a body, and the body can
    contain arbitrary hyperdiv components.

    ```py
    with hd.box(gap=1):
        placement = hd.radio_buttons(
            "start",
            "top",
            "end",
            "bottom",
            value="start"
        )

        with hd.drawer(
            "My Drawer",
            placement=placement.value,
        ) as drawer:
            hd.text("Drawer contents")

        if hd.button("Open Drawer").clicked:
            drawer.opened = True
    ```

    ## Contained Drawers

    Drawers can be contained within a @component(box) if you set the
    `contained` prop to `True`.

    ```py
    with hd.box(height=10, border="1px solid neutral-100"):
        with hd.drawer(
            "My Drawer",
            contained=True
        ) as drawer:
            hd.text("Drawer Contents")

    if hd.button("Open Drawer").clicked:
        drawer.opened = True
    ```

    ## Header Actions

    Drawers can have additional components (such as icon buttons or
    links) placed in a `header_actions` slot, which is rendered to the
    left of the drawer close button.

    ```py
    with hd.drawer("My Drawer") as drawer:
        hd.text("Drawer Contents")

        with hd.hbox(
            slot=drawer.header_actions,
            align="center",
            gap=0.8
        ):
            hd.icon_button("gear")
            hd.icon_button("people")

    if hd.button("Open Drawer").clicked:
        drawer.opened = True
    ```

    In this example, we place a horizontal @component(box) in the
    drawer's `header_actions` slot and put two side-by-side
    @component(icon_button)s in that box.
    """

    _tag = "sl-drawer"

    # Where the drawer opens from:
    # * `top` - opens downward from the top.
    # * `start` - opens rightward from the left.
    # * `bottom` - opens upward from the bottom.
    # * `end` - opens leftward from the right.
    placement = Prop(OneOf("top", "start", "bottom", "end"), "start")
    # Whether the drawer should be contained within its parent
    # component. By default, the drawer is contained within the
    # top-level viewport.
    contained = Prop(Bool, False)
    # Removes the header and the close button. Since this removes the
    # default way to close the drawer, users should be provided with an
    # alternative way to close the drawer.
    no_header = Prop(Bool, False)

    label_slot = Slot(ui_name="label")
    header_actions = Slot()
    footer = Slot()

    # The style part controlling the panel.
    panel_style = Prop(BasePart("panel", has_root=False))
    # The style part controlling the base.
    base_style = Prop(StylePart("base"))
    overlay_style = Prop(StylePart("overlay"))
    header_style = Prop(StylePart("header"))
    header_actions_style = Prop(StylePart("header-actions"))
    title_style = Prop(StylePart("title"))
    close_button_style = Prop(StylePart("close-button"))
    close_button_base_style = Prop(StylePart("close-button__base"))
    body_style = Prop(StylePart("body"))
    footer_style = Prop(StylePart("footer"))

    def _get_label_slot(self):
        return self.label_slot
