from ..prop_types import OneOf, Optional, String
from ..prop import Prop
from ..slot import Slot
from ..component_mixins.interactive import Interactive
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text
from .plaintext import plaintext


class breadcrumb_item(LabelComponent, Interactive):
    """
    A breadcrumb item to be used within @component(breadcrumb). This
    component accepts a `href` attribute and works like a
    @component(link).
    """

    _tag = "sl-breadcrumb-item"

    # A path to navigate to when clicked.
    href = Prop(Optional(String))
    # Determines where the link is opened. See the [W3Schools target
    # documentation](https://www.w3schools.com/tags/att_a_target.asp)
    target = Prop(OneOf(None, "_blank", "_parent", "_self", "_top"))
    # See `rel` docs [here](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel).
    rel = Prop(String, "noreferrer noopener")

    prefix = Slot()
    suffix = Slot()
    separator = Slot()

    base_style = Prop(BasePart())
    label_style = Prop(StylePart("label"))
    prefix_style = Prop(StylePart("prefix"))
    suffix_style = Prop(StylePart("suffix"))
    separator_style = Prop(StylePart("separator"))
