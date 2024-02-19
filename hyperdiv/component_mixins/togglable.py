from ..prop import Prop
from ..prop_types import Bool, BoolEvent


class Togglable:
    """
    A collection of props representing a component that can be opened
    and closed.
    """

    # Whether this component is visible
    opened = Prop(Bool, False, ui_name="open")
    # Whether the visibility of this component changed -- the
    # component was opened or closed.
    visibility_changed = Prop(BoolEvent, False)

    @property
    def was_opened(self):
        """True for one frame when the component was opened."""
        return self.visibility_changed and self.opened

    @property
    def was_closed(self):
        """True for one frame when the component was closed."""
        return self.visibility_changed and not self.opened

    def __init__(self):
        """
        `Togglable` cannot be instantiated.
        """
        raise Exception("`Togglable` cannot be instantiated.")
