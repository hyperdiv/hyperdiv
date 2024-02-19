from ..prop_types import String, Optional, Bool
from ..prop import Prop
from ..style_part import BasePart, StylePart
from .common.text_utils import concat_text
from .common.label_component import LabelComponent
from .common.shoelace_types import ShoelaceSize


class radio(LabelComponent):
    """
    A radio input component to be used with @component(radio_group).
    It isn't useful by itself.

    ```py
    r = hd.radio("A radio button")
    ```
    """

    _tag = "sl-radio"

    # The value of the radio button. By default, the value is set to
    # be equal to the label, if the value prop is not given.
    value = Prop(Optional(String))
    # The size of the radio button.
    size = Prop(ShoelaceSize, "medium")
    # Whether the radio button can be selected.
    disabled = Prop(Bool, False)

    base_style = Prop(BasePart())
    control_style = Prop(StylePart("control"))
    control_checked_style = Prop(StylePart("control--checked"))
    checked_icon_style = Prop(StylePart("checked-icon"))
    label_style = Prop(StylePart("label"))

    def __init__(self, *label, value=None, **kwargs):
        if value is None:
            value = concat_text(label)

        super().__init__(*label, value=value, **kwargs)
