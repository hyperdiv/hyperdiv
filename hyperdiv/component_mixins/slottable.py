from ..prop_types import HyperdivType
from ..slot import Slot
from ..prop import Prop


class SlotTypeDef(HyperdivType):
    """
    The type of Hyperdiv component slots.
    """

    def parse(self, value):
        if value is None:
            return None
        if not isinstance(value, Slot):
            raise ValueError(f"Expected a Slot but got {type(value)}")
        return value

    def render(self, value):
        if value is None:
            return None
        return value.ui_name

    def __repr__(self):
        return "SlotType"


SlotType = SlotTypeDef()


class Slottable:
    """
    A base class defining the `slot` prop, which allows a component to
    be nested within a slot of a parent component. All Hyperdiv UI
    components, except @component(text), support this interface.
    """

    slot = Prop(SlotType)

    def __init__(self):
        """
        `Slottable` cannot be instantiated.
        """
        raise Exception("`Slottable` cannot be instantiated.")
