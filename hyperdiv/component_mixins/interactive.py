from ..prop_types import BoolEvent
from ..prop import Prop


class Interactive:
    """
    A collection of props defining how a component can generally be
    interacted with. Currently only `clicked` is supported.
    """

    # Whether the component was clicked.
    clicked = Prop(BoolEvent, False)

    def __init__(self):
        """
        `Interactive` cannot be instantiated.
        """
        raise Exception("`Interactive` cannot be instantiated.")
