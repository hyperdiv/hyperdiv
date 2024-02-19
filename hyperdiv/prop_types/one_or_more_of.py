from .hyperdiv_type import HyperdivType


class OneOrMoreOf(HyperdivType):
    """
    `OneOrMoreOf(*values)` is a Hyperdiv type that accepts a tuple
    made of a subset of the values in `*values` and raises
    `ValueError` otherwise.
    """

    def __init__(self, *values):
        if len(values) <= 0:
            raise ValueError("Provide at least one value.")
        self.values = set(values)

    def parse(self, value):
        if not isinstance(value, tuple):
            raise ValueError(f"Expected a tuple but got {type(value)}.")
        diff = set(value).difference(self.values)
        if len(diff) > 0:
            raise ValueError(f"Unexpected values: {diff}")
        return value

    def __repr__(self):
        return "OneOrMoreOf"
