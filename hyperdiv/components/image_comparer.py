from ..prop_types import CSSField, ClampedFloat, Size
from ..prop import Prop
from ..component_base import Component
from ..slot import Slot
from ..component_mixins.styled import Styled
from ..style_part import BasePart, StylePart


class image_comparer(Component, Styled):
    """
    A component that allows visually comparing two images by sliding a divider.

    ```py
    with hd.image_comparer() as ic:
        hd.image(
            "/assets/kitten-bw.jpg",
            slot=ic.before
        )
        hd.image(
            "/assets/kitten.jpg",
            slot=ic.after
        )
    ```
    """

    _tag = "sl-image-comparer"
    _has_direct_children = False

    # The divider position, as a percentage.
    position = Prop(ClampedFloat(0, 100), 50)
    # The divider width.
    divider_width = Prop(CSSField("--divider-width", Size))
    # The size of the divider handle.
    handle_size = Prop(CSSField("--handle-size", Size))

    before = Slot()
    after = Slot()
    handle = Slot()

    base_style = Prop(BasePart())
    before_style = Prop(StylePart("before"))
    after_style = Prop(StylePart("after"))
    divider_style = Prop(StylePart("divider"))
    handle_style = Prop(StylePart("handle"))
