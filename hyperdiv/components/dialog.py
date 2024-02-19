from ..prop import Prop
from ..slot import Slot
from ..component_mixins.togglable import Togglable
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent


class dialog(LabelComponent, Togglable):
    """
    A dialog is an overlay that opens in the middle of the viewport. A
    dialog can contain arbitrary hyperdiv components.

    ```py
    dialog = hd.dialog("My Dialog")
    with dialog:
        hd.text("Dialog Contents")
    if hd.button("Open Dialog").clicked:
        dialog.opened = True
    ```

    """

    _tag = "sl-dialog"

    label_slot = Slot(ui_name="label")
    header_actions = Slot()
    footer = Slot()

    base_style = Prop(BasePart())
    overlay_style = Prop(StylePart("overlay"))
    panel_style = Prop(StylePart("panel"))
    header_style = Prop(StylePart("header"))
    header_actions_style = Prop(StylePart("header-actions"))
    title_style = Prop(StylePart("title"))
    close_button_style = Prop(StylePart("close-button"))
    close_button_base_style = Prop(StylePart("close-button__base"))
    body_style = Prop(StylePart("body"))
    footer_style = Prop(StylePart("footer"))

    def _get_label_slot(self):
        return self.label_slot
