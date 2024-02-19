from ..prop_types import Bool, String, BoolEvent
from ..prop import Prop
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.shoelace_types import ShoelaceSize
from .common.text_utils import concat_text


class checkbox(LabelComponent):
    """
    A checkbox component.

    ```py
    hd.checkbox("Check Me")
    ```

    An indeterminate checkbox:

    ```py
    hd.checkbox("Check Me", indeterminate=True)
    ```

    """

    _tag = "sl-checkbox"

    # The internal name of the checkbox. This is pertinent when using
    # checkboxes in @component(form)s.
    name = Prop(String, "")
    # The size of the checkbox.
    size = Prop(ShoelaceSize, "medium")
    # Whether the checkbox is checked.
    checked = Prop(Bool, False)
    # When disabled is `True`, the checkbox cannot be interacted with.
    disabled = Prop(Bool, False)
    # An indeterminate checkbox is neither checked nor unchecked.
    indeterminate = Prop(Bool, False)

    changed = Prop(BoolEvent, False)

    base_style = Prop(BasePart())
    control_style = Prop(StylePart("control"))
    control_checked_style = Prop(StylePart("control--checked"))
    control_indeterminate_style = Prop(StylePart("control--indeterminate"))
    checked_icon_style = Prop(StylePart("checked-icon"))
    label_style = Prop(StylePart("label"))

    def __init__(self, *label, name=None, **kwargs):
        if name is None:
            name = concat_text(label)

        super().__init__(*label, name=name, **kwargs)

    @property
    def value(self):
        return self.checked

    def reset(self):
        self.reset_prop("checked")
