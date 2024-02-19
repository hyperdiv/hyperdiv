from ..prop_types import OneOf, Bool, BoolEvent
from ..prop import Prop
from ..component_mixins.interactive import Interactive
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.shoelace_types import ShoelaceSize
from .common.text_utils import concat_text
from .plaintext import plaintext


class tag(LabelComponent, Interactive):
    """
    A tag component similar to @component(badge).

    ```py
    state = hd.state(removed=False)

    with hd.box(gap=1):
        hd.tag("A tag")
        hd.tag("A danger tag", variant="danger")
        hd.tag("A small tag", size="small")
        hd.tag("A large tag", size="large")
        hd.tag(
            "A warning pill tag",
            variant="warning",
            pill=True
        )
    ```

    ### Removable tags

    When passing `removable=True`, the tag renders a close button.
    The event prop `removed` fires when the button is clicked.

    ```py
    state = hd.state(removed=False)

    if not state.removed:
        tag = hd.tag(
            "A removable tag",
            removable=True
        )
        if tag.removed:
            state.removed = True
    ```

    """

    _tag = "sl-tag"

    # The variant of the tag.
    variant = Prop(
        OneOf(
            "primary",
            "success",
            "neutral",
            "warning",
            "danger",
            "text",
        ),
        "neutral",
    )
    # The size of the tag.
    size = Prop(ShoelaceSize, "medium")
    # Whether the tag is rendered as a pill.
    pill = Prop(Bool, False)
    # Whether a closed button is rendered in the tag.
    removable = Prop(Bool, False)
    # Event prop that fires when the closed button is clicked.
    removed = Prop(BoolEvent, False)

    base_style = Prop(BasePart())
    content_style = Prop(StylePart("content"))
    remove_button_style = Prop(StylePart("remove-button"))
    remove_button_base_style = Prop(StylePart("remove-button__base"))

    def __init__(self, *label, width="fit-content", **kwargs):
        super().__init__(*label, width=width, **kwargs)
