from .box import box
from .box_list_item import box_list_item


class box_list(box):
    """
    Renders a list of @component(box_list_item)s.

    By contrast to @component(list) and @component(ordered_list),
    `box_list` does not render a bullet point or number on its
    children, and subclasses @component(box), giving you a greater
    amount of control over how the children are rendered within
    the list.

    This type of list is convenient, for example, when building
    navigation menus. Accessibility tools will recognize this
    component as a list, even though it effectively works like a box.

    ```py
    with hd.box_list():
        hd.box_list_item("One")
        hd.box_list_item("Two")
    ```

    ### Custom alignment

    ```py
    with hd.box_list(
        direction="horizontal",
        gap=1
    ):
        hd.box_list_item(
            "One",
            border="1px solid green",
            padding=1
        )
        hd.box_list_item(
            "Two",
            border="1px solid green",
            padding=1
        )
    ```

    """

    _tag = "ul"
    _classes = box._classes + ["box-list"]

    def _collect_child(self, child):
        if not isinstance(child, box_list_item):
            raise Exception("A `box_list` can only contain `box_list_item` children.")
        super()._collect_child(child)
