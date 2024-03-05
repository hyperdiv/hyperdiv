from ..prop_types import OneOf, BoolEvent
from ..prop import Prop
from ..ui_singleton import BrowserSingleton
from .local_storage import local_storage


class theme(BrowserSingleton):
    """
    Allows access to the light/dark mode theme setting. You can set
    the theme by mutating the `mode` prop.

    ```py
    theme = hd.theme()
    icon = "sun"
    mode = "light"
    if theme.is_light:
        icon = "moon"
        mode = "dark"
    if hd.icon_button(icon).clicked:
        theme.mode = mode
    ```
    """

    _key = "theme"

    # The current system theme setting. This prop is automatically,
    # internally-updated as the system setting changes. Even though
    # this prop technically accepts `None` as a value, `None` is never
    # visible from a user perspective. It is set to `None` only
    # briefly on startup, and is immediately updated to a concrete
    # value before the application runs.
    system_mode = Prop(OneOf(None, "light", "dark"), backend_immutable=True)
    # The theme mode. If the mode is set to `"system"`, the theme
    # follows the value of the `system_mode` prop.
    mode = Prop(OneOf(None, "system", "light", "dark"))
    # True for one run when one of the theme props changed.
    changed = Prop(BoolEvent, False)

    def __init__(self):
        super().__init__()

    @property
    def is_light(self):
        """
        Returns `True` if the theme is in light mode, and `False` if the
        theme is in dark mode, regardless of whether the theme mode is
        set by the user or follows system.
        """
        if self.mode == "system":
            return self.system_mode == "light"
        else:
            return self.mode == "light"

    @property
    def is_dark(self):
        """The inverse of `is_light`."""
        return not self.is_light

    def set_and_remember_theme_mode(self, mode):
        """
        Sets the theme mode and updates the browser's local storage to
        remember this setting. Upon app revisits/reloads, the theme
        will load with this setting.
        """
        self.mode = mode
        local_storage.set_item("$hyperdiv.theme_mode", mode)

    def reset_and_forget_theme_mode(self):
        """
        Removes the theme mode setting from the browser's local storage,
        causing the theme setting to default to `system`.
        """
        self.mode = "system"
        local_storage.remove_item("$hyperdiv.theme_mode")
