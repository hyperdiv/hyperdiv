from ..prop_types import StringEvent
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.styled import Styled
from .menu_item import menu_item


class menu(Component, Styled):
    """
    A non-navigational menu component. You can build menus out using
    @component(menu_item), @component(menu_label) and
    @component(divider).

    ```py
    with hd.menu() as menu:
        hd.menu_item("One")
        hd.menu_item("Two")
        hd.menu_item("Three")
        hd.divider(spacing=0.5)
        hd.menu_label("Other options")
        hd.menu_item(
            "Settings",
            prefix_icon="gear"
        )
        hd.menu_item(
            "Home",
            prefix_icon="house"
        )
    ```

    The menu's `selected_item` attribute can be used to do stuff when
    an item was selected.

    ```py
    state = hd.state(last_selected=None)

    with hd.box(gap=1):
        with hd.menu() as menu:
            hd.menu_item("One")
            hd.menu_item("Two")
            hd.menu_item("Three")
            hd.divider(spacing=0.5)
            hd.menu_label("Other options")
            hd.menu_item(
                "Settings",
                prefix_icon="gear"
            )
            hd.menu_item(
                "Home",
                prefix_icon="house"
            )

        if menu.selected_item:
            state.last_selected = menu.selected_item.label

        hd.text("Last selected:", state.last_selected)
    ```

    ### Checkable items

    Menu items can act like checkboxes when you set `item_type` to `"checkbox"`.

    ```py
    with hd.menu():
        hd.menu_item("One", item_type="checkbox")
        hd.menu_item("Two", item_type="checkbox")
    ```

    You can get the checked items out of the menu using the `checked_items` property.

    ```py
    with hd.box(gap=1):
        with hd.menu() as menu:
            hd.menu_item("One", item_type="checkbox")
            hd.menu_item("Two", item_type="checkbox")

        hd.text("Checked items:", [
            item.label
            for item in menu.checked_items
        ])
    ```

    ### Dropdown menus

    A typical use of menus is to put them in @component(dropdown)s:

    ```py
    with hd.dropdown() as dd:
        trigger = hd.button(
            "Open Me",
            caret=True,
            slot=dd.trigger
        )
        with hd.menu() as menu:
            hd.menu_item("One")
            hd.menu_item("Two")
            hd.divider(spacing=0.5)
            hd.menu_item("Three")
            hd.menu_item("Four")
        if trigger.clicked or menu.selected_item:
            dd.opened = not dd.opened
    ```
    """

    _tag = "sl-menu"

    _selected_item_key = Prop(StringEvent, "")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_item = None

    def _collect_child(self, child):
        super()._collect_child(child)
        if child._key == self._selected_item_key:
            self.selected_item = child

    def item(self, *args, **kwargs):
        return menu_item(*args, **kwargs)

    @property
    def items(self):
        return [child for child in self.children if isinstance(child, menu_item)]

    @property
    def checked_items(self):
        return [
            item for item in self.items if item.item_type == "checkbox" and item.checked
        ]
