from ..prop_types import OneOf, StringEvent, Bool
from ..prop import Prop
from ..component_base import Component
from ..slot import Slot
from ..component_mixins.styled import Styled
from ..style_part import BasePart, StylePart
from .scope import scope
from .tab import tab


class tab_group(Component, Styled):
    """
    `tab_group` groups together a set of @component(tab)
    components. You can inspect the `active` prop on each tab to see
    which tab is currently selected, and render content specific to
    that tab.

    ```py
    with hd.tab_group() as tabs:
        t1 = hd.tab("One")
        t2 = hd.tab("Two")
        t3 = hd.tab("Three")

    with hd.box(padding=1):
        if t1.active:
            hd.text("One")
        elif t2.active:
            hd.text("Two")
        else:
            hd.text("Three")
    ```

    If you don't need control over how each tab is rendered, there is
    a much terser alternative shorthand notation by passing the tab
    names directly in the constructor, and using the `active` prop on
    the tab group to inspect which tab is active, using the tab name:

    ```py
    tabs = hd.tab_group("One", "Two", "Three")

    with hd.box(padding=1):
        if tabs.active == "One":
            hd.text("One")
        elif tabs.active == "Two":
            hd.text("Two")
        else:
            hd.text("Three")
    ```

    ### Vertical tabs

    ```py
    with hd.hbox():
        tabs = hd.tab_group(
            "One", "Two", "Three",
            placement="start"
        )
        with hd.box(padding=1):
            if tabs.active == "One":
                hd.text("One")
            elif tabs.active == "Two":
                hd.text("Two")
            else:
                hd.text("Three")
    ```
    """

    _tag = "sl-tab-group"

    # The placement of the tabs:
    #
    # * top: the tabs are laid out horizontally, the underline is
    #   rendered below the tabs, and the tab group is placed at the
    #   top of the tab group container.
    #
    # * bottom: the tabs are laid out horizontally, the underline is
    #   rendered above the tabs, and the tab group is placed at the
    #   bottom of the tab group container.
    #
    # * start: the tabs are laid out vertically, the underline is
    #   rendered to the right of the tabs, and the tab group is placed
    #   at the start of the tab group container.
    #
    # * end: the tabs are laid out vertically, the underline is
    #   rendered to the left of the tabs, and the tab group is placed
    #   at the end of the tab group container.
    placement = Prop(OneOf("top", "bottom", "start", "end"), "top")
    # By default, when navigating with the keyboard, tabs are
    # automatically activated when pressing the left or right arrow
    # keys. When activation is set to `"manual"`, you have to press
    # Space or Enter to activate the focused tab.
    activation = Prop(OneOf("auto", "manual"), "auto")
    # Whether to render scroll buttons when the tabs overflow.
    no_scroll_controls = Prop(Bool, False)
    _active_tab_key = Prop(StringEvent, "")

    nav = Slot()

    base_style = Prop(BasePart())
    nav_style = Prop(StylePart("nav"))
    tabs_style = Prop(StylePart("tabs"))
    active_tab_indicator_style = Prop(StylePart("active-tab-indicator"))
    body_style = Prop(StylePart("body"))
    scroll_button_style = Prop(StylePart("scroll-button"))
    scroll_button_start_style = Prop(StylePart("scroll-button--start"))
    scroll_button_end_style = Prop(StylePart("scroll-button--end"))
    scroll_button_base_style = Prop(StylePart("scroll-button__base"))

    def __init__(self, *tabs, **kwargs):
        self.tabs = []
        self.active_tab = None
        self.closed_tab = None

        super().__init__(**kwargs)

        if tabs:
            with self:
                for tab_label in tabs:
                    with scope(tab_label):
                        tab(tab_label, font_size=self.font_size)

    @property
    def closed(self):
        return self.closed_tab.label if self.closed_tab else None

    @property
    def active(self):
        return self.active_tab.label if self.active_tab else None

    def _collect_child(self, child):
        if isinstance(child, tab):
            if child.slot and child.slot != self.nav:
                raise Exception("`tab` cannot be in a slot other than `tab_group.nav`.")
            if not child.slot:
                child.slot = self.nav

        super()._collect_child(child)

        if not isinstance(child, tab):
            return

        self.tabs.append(child)

        if self._active_tab_key:
            # Setting a new active tab. Reminder: `active_child_key` is
            # only set for one frame.
            if child._key == self._active_tab_key:
                child.active = True
                self.active_tab = child
            elif child.active:
                # Make the prior active tab inactive.
                child.active = False
        else:
            # Tentatively assume the first tab is active
            if not self.active_tab:
                self.active_tab = child
            # But if we find an actually active tab later, set that
            # one as active.
            if child.active:
                self.active_tab = child

        if child.closed_clicked:
            self.closed_tab = child

    def __exit__(self, exc_type, exc_val, exc_tb):
        # On body exit, if the tab we assumed would be active
        # isn't active, then set it to active. This happens when there
        # are no active tabs, and we force the first tab to be active.
        super().__exit__(exc_type, exc_val, exc_tb)
        if self.active_tab and not self.active_tab.active:
            self.active_tab.active = True


tabs = tab_group
