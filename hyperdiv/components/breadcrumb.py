from ..prop_types import String
from ..prop import Prop
from ..component_base import Component
from ..slot import Slot
from ..component_mixins.styled import Styled
from ..style_part import BasePart


class breadcrumb(Component, Styled):
    """
    This component renders a breadcrumb trail useful in building
    navigations. It accepts @component(breadcrumb_item) components
    as its children.

    ```py
    with hd.breadcrumb():
        hd.breadcrumb_item(
            "Grandparent",
            href="/grandparent"
        )
        hd.breadcrumb_item(
            "Parent",
            href="/grandparent/parent"
        )
        hd.breadcrumb_item("Child", href="#")
    ```

    """

    _tag = "sl-breadcrumb"

    # An invisible label that helps voice navigation.
    assistive_label = Prop(String, "", ui_name="label")

    # TODO: separator slot strips styles from the element in the slot
    separator = Slot()

    base_style = Prop(BasePart())
