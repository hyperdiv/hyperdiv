from ..prop_types import Int
from ..prop import Prop
from ..component_base import Component
from ..slot import Slot
from ..component_mixins.styled import Styled
from ..component_mixins.togglable import Togglable
from ..style_part import BasePart, StylePart
from .common.shoelace_types import ShoelacePlacement
from .button import button


class dropdown(Component, Styled, Togglable):
    """
    A dropdown is an overlay component that opens near a "trigger"
    component. Normally the trigger is a button, and clicking the
    button will open the dropdown overlay.

    The dropdown component is a container that has a `trigger` slot.
    The trigger component should be placed in the `trigger` slot.

    The body of the dropdown is the content that will open when the
    `opened` prop is set to `True`.

    Typical dropdown usage:

    ```py
    with hd.dropdown("Open"):
        hd.text("The content")
    ```

    To customize the click target, don't pass a label, use the
    `target` slot, and toggle the dropdown's `opened` prop when the
    target is clicked:

    ```py
    with hd.dropdown() as dropdown:
        # The trigger:
        trigger = hd.button(
            "Open",
            variant='primary',
            caret=True,
            slot=dropdown.trigger
        )
        # When the trigger is clicked,
        # the dropdown is toggled:
        if trigger.clicked:
            dropdown.opened = not dropdown.opened
        # The content:
        hd.text("The content")
    ```

    In the following example, you can explore the behavior of the
    dropdown's props, which can be used to control where, relative to
    the trigger, the dropdown opens.

    ```py
    placement_values = (
        "top",
        "top-start",
        "top-end",
        "bottom",
        "bottom-start",
        "bottom-end",
        "right",
        "right-start",
        "right-end",
        "left",
        "left-start",
        "left-end"
    )

    with hd.box(gap=1):
        placement = hd.select(
            "Placement:",
            options=placement_values,
            value="bottom-start"
        )
        skidding = hd.slider("Skidding")
        distance = hd.slider("Distance")

        with hd.dropdown(
            "Open Me",
            placement=placement.value,
            skidding=int(skidding.value),
            distance=int(distance.value)
        ) as dropdown:
            with hd.box(
                border="1px solid green",
                padding=1,
                background_color="neutral-50"
            ):
                hd.text("Dropdown Contents")
    ```

    """

    _tag = "sl-dropdown"

    placement = Prop(ShoelacePlacement, "bottom-start")
    distance = Prop(Int, 0)
    skidding = Prop(Int, 0)

    trigger = Slot()

    base_style = Prop(BasePart())
    trigger_style = Prop(StylePart("trigger"))
    panel_style = Prop(StylePart("panel"))

    def __init__(self, *button_label, **kwargs):
        super().__init__(**kwargs)
        if button_label:
            with self:
                if button(*button_label, caret=True, slot=self.trigger).clicked:
                    self.opened = not self.opened
