from ..prop_types import String, Bool
from ..prop import Prop
from ..slot import Slot
from ..component_mixins.styled import Styled
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text
from .icon import icon
from .plaintext import plaintext


class option(LabelComponent, Styled):
    """
    An option component that is not usable by itself, but should be
    nested within @component(select).

    Options support `prefix` and `suffix` slots, that are typically
    used to slot prefix and suffix icons.

    ```py
    hd.option("An option", prefix_icon="gear")
    ```
    """

    _tag = "sl-option"

    # The value of the option. By default it is set to its label.
    value = Prop(String, "")
    # Whether this option can be selected.
    disabled = Prop(Bool, False)

    prefix = Slot()
    suffix = Slot()

    base_style = Prop(BasePart())
    checked_icon_style = Prop(StylePart("checked-icon"))
    label_style = Prop(StylePart("label"))
    prefix_style = Prop(StylePart("prefix"))
    suffix_style = Prop(StylePart("suffix"))

    def __init__(
        self, *label, value=None, prefix_icon=None, suffix_icon=False, **kwargs
    ):
        if value is None:
            value = concat_text(label)

        super().__init__(*label, value=value, **kwargs)

        with self:
            if prefix_icon:
                icon(prefix_icon, slot=self.prefix)
            if suffix_icon:
                icon(suffix_icon, slot=self.suffix)
