from .hyperdiv_type import HyperdivType


class Constant(HyperdivType):
    """A prop with type `Constant(c)` accepts only the constant `c`."""

    def __init__(self, constant):
        self.constant = constant

    def parse(self, value):
        if value != self.constant:
            raise ValueError(f"Only {self.constant} is a valid value.")
        return value

    def __repr__(self):
        return f"Constant[{repr(self.constant)}]"
