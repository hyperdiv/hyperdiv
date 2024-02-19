from ..prop_types import CSSField, OneOf
from ..prop import Prop
from .common.list_base import list_base


class ordered_list(list_base):
    """
    Renders an ordered (numbered) list of @component(list_item)s.

    ```py
    hd.text("Here is a list:")
    with hd.ordered_list():
        hd.list_item("One")
        hd.list_item("Two")
        hd.list_item("Three")
        hd.list_item("Four")
    ```

    ### Custom item numbers

    The number formatting can be controlled via the `style_type` prop.

    ```py
    hd.text("Here is a list:")
    with hd.ordered_list(style_type="lower-roman"):
        hd.list_item("One")
        hd.list_item("Two")
        hd.list_item("Three")
        hd.list_item("Four")
    ```
    """

    _tag = "ol"

    style_type = Prop(
        CSSField(
            "list-style-type",
            OneOf(
                "none",
                "decimal",
                "lower-latin",
                "lower-roman",
                "upper-latin",
                "upper-roman",
            ),
        ),
        "decimal",
    )
