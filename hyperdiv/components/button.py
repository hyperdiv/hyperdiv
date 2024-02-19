from ..prop_types import OneOf, Bool
from ..prop import Prop
from ..slot import Slot
from ..component_mixins.interactive import Interactive
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text
from .common.shoelace_types import ShoelaceSize
from .plaintext import plaintext
from .icon import icon


class button(LabelComponent, Interactive):
    """A button component.

    ```py
    hd.button("Default")
    hd.button("Primary", variant="primary")
    hd.button("Success", variant="success")
    hd.button("Neutral", variant="neutral")
    hd.button("Warning", variant="warning")
    hd.button("Danger", variant="danger")
    hd.button("Primary",
        variant="primary",
        outline=True
    )
    hd.button("Success",
        variant="success",
        outline=True
    )
    hd.button("Neutral",
        variant="neutral",
        outline=True
    )
    hd.button("Warning",
        variant="warning",
        outline=True
    )
    hd.button("Danger",
        variant="danger",
        outline=True
    )
    hd.button("Text", variant="text")
    hd.button("Pill Button", pill=True)
    hd.button("With Caret", caret=True)
    hd.button("Loading", loading=True)
    hd.button("Large", size="large")
    hd.button("Small", size="small")
    ```

    ### Slots

    `button` supports `prefix` and `suffix` slots that can be used for
    slotting icons into the button. Shorthand arguments `prefix_icon`
    and `suffix_icon` are also provided.

    ```py
    hd.button("Settings", prefix_icon="gear")
    # Equivalent to:
    with hd.button("Settings") as button:
        hd.icon("gear", slot=button.prefix)
    ```
    """

    _tag = "sl-button"

    # The button variant.
    variant = Prop(
        OneOf(
            "default",
            "primary",
            "success",
            "neutral",
            "warning",
            "danger",
            "text",
        ),
        "default",
    )
    # The size of the button.
    size = Prop(ShoelaceSize, "medium")
    # The type of the button. Usually you do not need to use this prop
    # directly. When using buttons with @component(form)s, the button
    # type is set implicitly.
    button_type = Prop(OneOf("button", "submit", "reset"), "button", ui_name="type")
    # Whether to render the button as a pill.
    pill = Prop(Bool, False)
    # Whether to render the button's variant as an outline instead of
    # a background fill.
    outline = Prop(Bool, False)
    # Whether to render the button as a circle.
    circle = Prop(Bool, False)
    # Whether to render a caret in the suffix slot. This is useful
    # shorthand when the button is used as a trigger for a
    # @component(dropdown).
    caret = Prop(Bool, False)
    # Whether to render a loading spinner in the button.
    loading = Prop(Bool, False)
    # Whether the button is disabled. Disabled buttons do not respond to clicks.
    disabled = Prop(Bool, False)

    prefix = Slot()
    suffix = Slot()

    base_style = Prop(BasePart())
    label_style = Prop(StylePart("label"))
    prefix_style = Prop(StylePart("prefix"))
    suffix_style = Prop(StylePart("suffix"))
    caret_style = Prop(StylePart("caret"))

    def __init__(
        self,
        *label,
        prefix_icon=None,
        suffix_icon=None,
        width="fit-content",
        **kwargs,
    ):
        super().__init__(*label, width=width, **kwargs)

        if prefix_icon:
            with self:
                icon(prefix_icon, slot=self.prefix)
        if suffix_icon:
            with self:
                icon(suffix_icon, slot=self.suffix)
