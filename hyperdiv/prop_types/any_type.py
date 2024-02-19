from .hyperdiv_type import HyperdivType


class AnyDef(HyperdivType):
    """The universal type that accepts any value."""

    def __repr__(self):
        return "Any"


Any = AnyDef()
