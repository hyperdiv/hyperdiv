from ..prop_types import String, Optional, Bool
from ..prop import Prop
from ..slot import Slot
from ..style_part import BasePart, StylePart
from .common.text_utils import concat_text
from .common.label_component import LabelComponent
from .common.shoelace_types import ShoelaceSize


class radio_button(LabelComponent):
    """
    A radio button component to be used with
    @component(radio_group). Similar to @component(radio), but
    rendered as a button.

    This component isn't useful by itself and should only be used when
    nested in a @component(radio_group).

    ```py
    hd.radio_button("My Button")
    ```
    """

    _tag = "sl-radio-button"

    # The value of the radio button. By default, if `value` isn't
    # provided, it is set to be equal to the label.
    value = Prop(Optional(String))
    # The size of the radio button.
    size = Prop(ShoelaceSize, "medium")
    # Whether this radio button can be selected.
    disabled = Prop(Bool, False)
    # Whether to render the radio button as a pill.
    pill = Prop(Bool, False)

    prefix = Slot()
    suffix = Slot()

    base_style = Prop(BasePart())
    button_style = Prop(StylePart("button"))
    button_checked_style = Prop(StylePart("button--checked"))
    prefix_style = Prop(StylePart("prefix"))
    label_style = Prop(StylePart("label"))
    suffix_style = Prop(StylePart("suffix"))

    def __init__(self, *label, value=None, width="fit-content", **kwargs):
        if value is None:
            value = concat_text(label)

        super().__init__(*label, value=value, width=width, **kwargs)
