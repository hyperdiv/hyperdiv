from ..prop_types import OneOf, String, CSSField, Size
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.styled import Styled
from ..component_mixins.interactive import Interactive
from ..style_part import StylePart, BasePart


class avatar(Component, Styled, Interactive):
    """
    A component useful for rendering a user avatar. By default it
    renders a user icon.

    ```py
    with hd.box(gap=1):
        hd.avatar()
        hd.avatar(image="/assets/kitten.jpg")
        hd.avatar(initials="MP", size=5)
        hd.avatar(initials="AD", shape="rounded")
    ```

    """

    _tag = "sl-avatar"

    # The path or URL of an image to render in the avatar.
    image = Prop(String)
    # An invisible label useful for accessibility.
    assistive_label = Prop(String, ui_name="label")
    # A string of two initials. Typically, these are the user's
    # initials when an image is not available.
    initials = Prop(String, "")
    loading = Prop(OneOf("eager", "lazy"), "eager")
    # The shape of the avatar.
    shape = Prop(OneOf("circle", "square", "rounded"), "circle")
    # The size of the avatar.
    size = Prop(CSSField("--size", Size))

    base_style = Prop(BasePart())
    icon_style = Prop(StylePart("icon"))
    initials_style = Prop(StylePart("initials"))
    image_style = Prop(StylePart("image"))
