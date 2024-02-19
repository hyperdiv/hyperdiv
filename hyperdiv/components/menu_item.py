from ..prop_types import OneOf, Bool, String
from ..prop import Prop
from ..slot import Slot
from ..component_mixins.interactive import Interactive
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .icon import icon


class menu_item(LabelComponent, Interactive):
    """
    A menu item component to be used within the @component(menu) component.

    This component exports the `prefix` and `suffix` slots that are
    typically used for prefix and suffix icons. The `prefix_icon` and
    `suffix_icon` args in the constructor can be used to quickly add
    icons into these slots.

    ```py
    with hd.menu():
        hd.menu_item(
            "Settings",
            prefix_icon="gear",
            suffix_icon="bell-slash"
        )
    ```

    """

    _tag = "sl-menu-item"

    # When the value of this prop is `"checkbox"`, the manu item is
    # checkable and a check mark indicator is rendered next to it.
    item_type = Prop(OneOf("normal", "checkbox"), "normal", ui_name="type")
    # Whether the item is checked. Only relevant when `item_type` is
    # set to `"checkbox"`.
    checked = Prop(Bool, False)
    # A hidden value, like an identifier, that can be assigned to this
    # item. You can use this to identify the selected item in a menu.
    value = Prop(String, "")
    # Whether the item can be selected.
    disabled = Prop(Bool, False)

    # Prefix slot
    prefix = Slot()
    # Suffix slot
    suffix = Slot()

    base_style = Prop(BasePart())
    checked_icon_style = Prop(StylePart("checked-icon"))
    prefix_style = Prop(StylePart("prefix"))
    label_style = Prop(StylePart("label"))
    suffix_style = Prop(StylePart("suffix"))
    submenu_icon_style = Prop(StylePart("submenu-icon"))

    def __init__(self, *label, prefix_icon=None, suffix_icon=None, **kwargs):
        super().__init__(*label, **kwargs)
        if prefix_icon or suffix_icon:
            with self:
                if prefix_icon:
                    icon(prefix_icon, slot=self.prefix)
                if suffix_icon:
                    icon(suffix_icon, slot=self.suffix)
