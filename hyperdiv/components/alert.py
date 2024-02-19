from ..component_mixins.togglable import Togglable
from ..slot import Slot
from ..prop import Prop
from ..prop_types import Bool, Float
from ..style_part import StylePart, BasePart
from .common.label_component import LabelComponent
from .common.shoelace_types import ShoelaceVariant
from .icon import icon


class alert(LabelComponent, Togglable):
    """
    A component that renders inline notices.

    ```py
    with hd.box(gap=1):
        hd.alert("An info alert", opened=True)
        hd.alert("A success alert", variant="success", opened=True)
        hd.alert("A warning alert", variant="warning", opened=True)
        hd.alert("A danger alert", variant="danger", opened=True)
    ```
    """

    _tag = "sl-alert"

    # Whether to render a close button, which closes the alert when
    # clicked.
    closable = Prop(Bool, False)
    # The alert variant.
    variant = Prop(ShoelaceVariant, "primary")
    # How long the alert is visible before it self-closes, in
    # milliseconds.
    duration = Prop(Float, float("inf"))

    icon = Slot()

    base_style = Prop(BasePart(has_root=False))
    icon_style = Prop(StylePart("icon"))
    message_style = Prop(StylePart("message"))
    close_button_style = Prop(StylePart("close-button"))
    close_button_base_style = Prop(StylePart("close-button__base"))

    def __init__(
        self,
        *label,
        icon_name=None,
        variant="primary",
        **kwargs,
    ):
        if icon_name is None:
            if variant in ["primary", "neutral"]:
                icon_name = "info-circle"
            elif variant == "success":
                icon_name = "check2-circle"
            elif variant == "warning":
                icon_name = "exclamation-triangle"
            elif variant == "danger":
                icon_name = "exclamation-octagon"

        super().__init__(*label, variant=variant, **kwargs)

        if icon_name:
            with self:
                if icon_name:
                    icon(icon_name, slot=self.icon)
