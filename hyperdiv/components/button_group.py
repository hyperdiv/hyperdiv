from ..prop_types import String
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.styled import Styled
from ..style_part import BasePart


class button_group(Component, Styled):
    """
    A container that visually groups together a set of related
    @component(button)s.

    ```py
    with hd.button_group():
        hd.button("One")
        hd.button("Two")
        hd.button("Three")
    ```

    """

    _tag = "sl-button-group"

    # An invisible label that helps with accessibility.
    assistive_label = Prop(String, "")

    base_style = Prop(BasePart())
