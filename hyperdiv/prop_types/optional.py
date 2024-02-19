from .hyperdiv_type import HyperdivType


class Optional(HyperdivType):
    """
    `Optional(typ)` creates a type that, in addition to the values
    accepted by `typ`, also accepts the value `None`.
    """

    def __init__(self, typ):
        self.typ = typ

    def parse(self, value):
        if value is None:
            return None
        return self.typ.parse(value)

    def render(self, value):
        if value is None:
            return None
        return self.typ.render(value)

    def __repr__(self):
        return f"Optional[{repr(self.typ)}]"
