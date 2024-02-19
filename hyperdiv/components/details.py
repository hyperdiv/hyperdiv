from ..prop_types import Bool
from ..prop import Prop
from ..component_base import Component
from ..slot import Slot
from ..component_mixins.styled import Styled
from ..component_mixins.togglable import Togglable
from ..style_part import BasePart, StylePart
from .common.text_utils import concat_text
from .icon import icon
from .text import text


class details(Component, Styled, Togglable):
    """
    Renders a summary that when clicked, reveals content.

    ```py
    with hd.details("Open Me"):
        hd.text("Contents")
    ```

    ### Custom style

    ```py
    with hd.details(
        "Open Me",
        border="none",
        header_style=hd.style(
            padding=(0.2, 0.5, 0.2, 0.5),
            background_color="primary",
            font_color="neutral-50",
        )
    ):
        hd.text("Contents")
    ```

    ### Opened by default

    ```py
    with hd.details("Open Me", opened=True):
        hd.text("Contents")
    ```

    ### Opened programmatically

    ```py
    with hd.box(gap=1):
        with hd.details("Open Me") as details:
            hd.text("Contents")

        if hd.button("Toggle").clicked:
            details.opened = not details.opened
    ```


    ### Custom Icons

    Note that the `collapse_icon` is implicitly rotated 90 degrees clockwise.

    ```py
    with hd.details(
        "Open Me",
        expand_icon="arrow-right",
        collapse_icon="arrow-bar-right"
    ):
        hd.text("Contents")
    ```
    """

    _tag = "sl-details"

    disabled = Prop(Bool, False)

    summary = Slot()
    expand_icon_slot = Slot(ui_name="expand-icon")
    collapse_icon_slot = Slot(ui_name="collapse-icon")

    base_style = Prop(BasePart())
    header_style = Prop(StylePart("header"))
    summary_style = Prop(StylePart("summary"))
    summary_icon_style = Prop(StylePart("summary-icon"))
    content_style = Prop(StylePart("content"))

    def __init__(self, *summary, expand_icon=None, collapse_icon=None, **kwargs):
        super().__init__(**kwargs)

        with self:
            if summary:
                text(concat_text(summary), slot=self.summary)
            if expand_icon:
                icon(expand_icon, slot=self.expand_icon_slot)
                if not collapse_icon:
                    icon(expand_icon, slot=self.collapse_icon_slot)
            if collapse_icon:
                icon(collapse_icon, slot=self.collapse_icon_slot)
