from ..prop_types import OneOf, String
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.styled import Styled
from ..icons import icon_names
from ..style_part import StylePart

Icon = OneOf(*icon_names)


class icon(Component, Styled):
    """
    A component that renders one of the built-in icons. See
    @prop_type(Icon) for the available icons. Icons can be styled
    using style props, much like you style text.

    Also see the related @component(icon_button).

    ```py
    with hd.box(gap=1):
        hd.icon()
        hd.icon("apple", font_size=3)
        hd.icon(
            "activity",
            font_color="red",
            font_size=2,
            border="1px solid neutral-200",
            border_radius="large",
            padding=0.5
        )
    ```

    """

    _tag = "sl-icon"

    # The name of the icon.
    name = Prop(Icon, "emoji-laughing-fill")
    # An invisible label useful for accessibility.
    assistive_label = Prop(String, "", ui_name="label")

    svg_style = Prop(StylePart("svg"))
    use_style = Prop(StylePart("use"))

    def __init__(self, name="emoji-laughing-fill", **kwargs):
        super().__init__(name=name, **kwargs)
