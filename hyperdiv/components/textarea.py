from ..prop_types import String, Bool, OneOf, Int, Optional, BoolEvent
from ..prop import Prop
from ..slot import Slot
from .common.shoelace_types import (
    ShoelaceSize,
    InputAutoCapitalize,
    InputAutoCorrect,
    InputEnterKeyHint,
    InputMode,
)
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text


class textarea(LabelComponent):
    """
    A text area component.

    ```py
    hd.textarea(placeholder="Type here")
    ```
    """

    _tag = "sl-textarea"

    value = Prop(String, "")
    name = Prop(String, "")
    size = Prop(ShoelaceSize, "medium")
    filled = Prop(Bool, False)
    help_text = Prop(String, "")
    placeholder = Prop(String, "")
    rows = Prop(Int, 4)
    resize = Prop(OneOf("none", "vertical", "auto"), "vertical")
    disabled = Prop(Bool, False)
    readonly = Prop(Bool, False)
    minlength = Prop(Optional(Int))
    maxlength = Prop(Optional(Int))
    autocapitalize = Prop(InputAutoCapitalize)
    autocorrect = Prop(InputAutoCorrect)
    autocomplete = Prop(Optional(String))
    autofocus = Prop(Bool, False)
    enterkeyhint = Prop(InputEnterKeyHint)
    spellcheck = Prop(Bool, False)
    inputmode = Prop(InputMode)
    changed = Prop(BoolEvent, False)

    label_slot = Slot(ui_name="label")

    base_style = Prop(BasePart("form-control"))
    input_wrapper_style = Prop(StylePart("form-control-input"))
    input_base_style = Prop(StylePart("base"))
    input_style = Prop(StylePart("textarea"))
    label_style = Prop(StylePart("form-control-label"))
    help_text_style = Prop(StylePart("form-control-help-text"))

    def __init__(self, *label, name=None, **kwargs):
        if name is None:
            name = concat_text(label)

        super().__init__(*label, name=name, **kwargs)

    def reset(self):
        self.reset_prop("value")

    def _get_label_slot(self):
        return self.label_slot
