from ..prop_types import String, Bool, BoolEvent
from ..prop import Prop
from ..frame import AppRunnerFrame
from ..component_keys import get_component_key
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent


class tab(LabelComponent):
    """
    Renders a tab component. This component is not useful
    directly. Instead, a group of tabs should be nested inside a
    @component(tab_group).
    """

    _tag = "sl-tab"

    # Whether this tab is the active tab.
    active = Prop(Bool, False)
    # Whether to render a close button.
    closable = Prop(Bool, False)
    # Whether the close button was clicked.
    closed_clicked = Prop(BoolEvent, False)
    # Whether this tab is disabled. If it is disabled, it cannot be
    # activated.
    disabled = Prop(Bool, False)
    _panel = Prop(String, "", ui_name="panel")

    base_style = Prop(BasePart())
    close_button_style = Prop(StylePart("close-button"))
    close_button_base_style = Prop(StylePart("close-button__base"))

    def __init__(self, *label, slot=None, **kwargs):
        # TODO: circular import
        from .tab_group import tab_group

        key = get_component_key()

        if slot is None:
            frame = AppRunnerFrame.current()
            collector = frame.collector_stack.current()
            if isinstance(collector, tab_group):
                slot = collector.nav

        super().__init__(*label, key=key, _panel=key, slot=slot, **kwargs)
