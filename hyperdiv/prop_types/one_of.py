from .hyperdiv_type import HyperdivType


class OneOf(HyperdivType):
    """
    `OneOf(*values)` creates a Hyperdiv type that accepts one of the
    given values and raises `ValueError` otherwise.
    """

    def __init__(self, *values):
        self.values = set(values)

    def parse(self, value):
        if value not in self.values:
            raise ValueError(f"Unexpected value: {value}")
        return value

    def __repr__(self):
        return "OneOf"
