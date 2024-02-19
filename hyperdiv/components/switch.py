from ..prop_types import String, CSSField, Bool, Size, BoolEvent
from ..prop import Prop
from ..style_part import BasePart, StylePart
from .common.shoelace_types import ShoelaceSize
from .common.label_component import LabelComponent
from .common.text_utils import concat_text


class switch(LabelComponent):
    """
    Essentially a checkbox that is rendered in a on/off switch style.

    ```py
    hd.switch("Toggle Me", checked=True)
    ```
    """

    _tag = "sl-switch"

    # The name of the switch, which is relevant when a switch is used
    # inside a @component(form). Set to the switch's label if a name
    # is not provided.
    name = Prop(String, "")
    # The size of the switch.
    size = Prop(ShoelaceSize, "medium")
    # Disables the ability to toggle the switch.
    disabled = Prop(Bool, False)
    # Whether the switch is checked/toggled on.
    checked = Prop(Bool, False)
    # The width of the switch.
    switch_width = Prop(CSSField("--width", Size))
    # The height of the switch.
    switch_height = Prop(CSSField("--height", Size))
    # The size of the "thumb" button that toggles the switch.
    thumb_size = Prop(CSSField("--thumb-size", Size))

    changed = Prop(BoolEvent, False)

    base_style = Prop(BasePart())
    control_style = Prop(StylePart("control"))
    thumb_style = Prop(StylePart("thumb"))
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
