from ..prop_types import Bool
from ..prop import Prop
from ..component_mixins.interactive import Interactive
from ..style_part import BasePart
from .common.label_component import LabelComponent
from .common.shoelace_types import ShoelaceVariant


class badge(LabelComponent, Interactive):
    """
    A badge component, useful for making visual labels.

    ```py
    with hd.box(gap=1):
        hd.badge("A badge")
        hd.badge("A warning badge", variant="warning")
        hd.badge("A pill badge", pill=True)
        hd.badge(
            "A pulsating danger badge",
            variant="danger",
            pulse=True
        )
    ```
    """

    _tag = "sl-badge"

    # The variant of the badge.
    variant = Prop(ShoelaceVariant, "primary")
    # Whether to render the badge as a pill.
    pill = Prop(Bool, False)
    # Whether to visually pulsate the badge.
    pulse = Prop(Bool, False)

    base_style = Prop(BasePart())
