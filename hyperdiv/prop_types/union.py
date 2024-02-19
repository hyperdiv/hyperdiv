from .hyperdiv_type import HyperdivType


class Union(HyperdivType):
    """
    `Union(typ1, typ2)` creates a type that accepts values of either
    `typ1` or `typ2`. It tries to parse the value with `typ1` first,
    and if that fails, it tries `typ2`.
    """

    def __init__(self, typ1, typ2):
        self.typ1 = typ1
        self.typ2 = typ2

    def parse(self, value):
        try:
            return self.typ1.parse(value)
        except Exception:
            return self.typ2.parse(value)

    def render(self, value):
        try:
            return self.typ1.render(value)
        except Exception:
            return self.typ2.render(value)

    def __repr__(self):
        return f"Union[{repr(self.typ1)}, {repr(self.typ2)}]"
