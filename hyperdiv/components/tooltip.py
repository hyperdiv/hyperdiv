from ..prop_types import String, Bool, Int, OneOrMoreOf
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.styled import Styled
from ..component_mixins.togglable import Togglable
from .common.text_utils import concat_text
from .common.shoelace_types import ShoelacePlacement
from ..style_part import BasePart, StylePart


class TooltipTriggerDef(OneOrMoreOf):
    """
    Used in @component(tooltip) to define the interaction by which a
    tooltip becomes visible.
    """

    def __init__(self):
        super().__init__("hover", "focus", "click", "manual")

    def render(self, value):
        return " ".join(value)

    def __repr__(self):
        return "TooltipTrigger"


TooltipTrigger = TooltipTriggerDef()


class tooltip(Component, Styled, Togglable):
    """
    Wraps a target component in a tooltip.

    ```py
    with hd.tooltip("Settings"):
        hd.icon("gear")
    ```
    """

    _tag = "sl-tooltip"

    # The text rendered in the tooltip.
    content = Prop(String, "")
    # Placement of the tooltip relative to the wrapped component.
    placement = Prop(ShoelacePlacement, "top")
    # When `disabled` is set to `True`, the tooltip stays hidden.
    disabled = Prop(Bool, False)
    # How far the tooltip is from the target.
    distance = Prop(Int, 8)
    # How far the tooltip is displaced along the target.
    skidding = Prop(Int, 0)
    # The set of actions on which the tooltip becomes visible. When
    # the action is `"manual"`, the tooltip does not become visible
    # unless the `opened` prop is programmatically set to `True`.
    trigger = Prop(TooltipTrigger, ("hover", "focus"))

    base_style = Prop(BasePart())
    body_style = Prop(StylePart("body"))
    base_popup_style = Prop(StylePart("base__popup"))
    base_arrow_style = Prop(StylePart("base__arrow"))

    def __init__(self, *content, **kwargs):
        """
        If `*content` is passed, it will be joined by `" "` and used to
        initialize the `content` prop.
        """
        if content:
            kwargs["content"] = concat_text(content)

        super().__init__(**kwargs)
