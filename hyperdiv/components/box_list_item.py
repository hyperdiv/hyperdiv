from .box import box
from .list_item import list_item


class box_list_item(list_item, box):
    """
    A list item component that can be nested in a @component(box_list).

    By contrast to @component(list_item), `box_list_item` subclasses
    @component(box), giving flexible control over how its
    children are aligned.

    ```py
    with hd.box_list(gap=0.5):
        with hd.box_list_item(
            direction="horizontal",
            align="center",
            gap=0.5
        ):
            hd.icon("arrow-right")
            hd.link("An item", href="#")

        with hd.box_list_item(
            direction="horizontal",
            align="center",
            gap=0.5
        ):
            hd.icon("chevron-right")
            hd.link("Another item", href="#")
    ```

    """

    pass
