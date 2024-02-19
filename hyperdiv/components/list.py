from ..prop_types import CSSField, OneOf
from ..prop import Prop
from .common.list_base import list_base


class list(list_base):
    """
    Renders an unordered (bullet-point) list of @component(list_item)s.

    ```py
    hd.text("Here is a list:")
    with hd.list():
        hd.list_item("One")
        hd.list_item("Two")
        hd.list_item("Three")
        hd.list_item("Four")
    ```

    ### Custom item numbers

    The bullet formatting can be controlled via the `style_type` prop.

    ```py
    hd.text("Here is a list:")
    with hd.list(style_type="square"):
        hd.list_item("One")
        hd.list_item("Two")
        hd.list_item("Three")
        hd.list_item("Four")
    ```
    """

    _tag = "ul"

    style_type = Prop(
        CSSField(
            "list-style-type",
            OneOf(
                "none",
                "circle",
                "square",
                "disc",
            ),
        ),
        "disc",
    )
