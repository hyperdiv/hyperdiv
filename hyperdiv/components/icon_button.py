from ..prop_types import Bool
from ..prop import Prop
from ..component_mixins.interactive import Interactive
from ..style_part import BasePart
from .icon import icon


class icon_button(icon, Interactive):
    """
    An @component(icon) that behaves like a clickable button. Its
    `clicked` event prop fires when the icon button is clicked.

    ```py
    button = hd.icon_button("apple")
    ```
    """

    _tag = "sl-icon-button"

    # Whether the icon button is disabled.
    disabled = Prop(Bool, False)

    base_style = Prop(BasePart())

    def __init__(
        self, name="emoji-laughing-fill", width="fit-content", padding=0, **kwargs
    ):
        super().__init__(name=name, padding=padding, width=width, **kwargs)
