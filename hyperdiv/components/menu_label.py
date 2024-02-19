from ..prop import Prop
from .common.label_component import LabelComponent
from ..style_part import BasePart


class menu_label(LabelComponent):
    """
    A menu component that can be used to give titles to sections
    within a @component(menu).

    ```py
    with hd.menu():
        hd.menu_label("First section")
        hd.menu_item("One")
        hd.menu_item("Two")
        hd.divider(spacing=0.5)
        hd.menu_label("Second section")
        hd.menu_item("Three")
        hd.menu_item("Four")
    ```
    """

    _tag = "sl-menu-label"

    base_style = Prop(BasePart())
