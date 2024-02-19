from .hyperdiv_type import HyperdivType
from .native import Native


class ClampedNumber(HyperdivType):
    """
    `ClampedNumber(num_type, low, high)` creates a Hyperdiv type that
    accepts values of numeric Python type `num_type` that are between
    `low` and `high` (inclusive). If `low` or `high` are set to `None`,
    the interval is open on that end.

    `ClampedNumber(int, low=None, high=None)` is equivalent to `Int`,
    because the interval is open at both ends.
    """

    def __init__(self, num_type, low=None, high=None):

        if num_type not in (int, float):
            raise ValueError(f"Cannot create a ClampedNumber out of {num_type}")

        coercible_types = [int] if num_type == float else []
        self.typ = Native(num_type, coercible_types=coercible_types)
        self.low = low
        self.high = high

    def parse(self, value):
        parsed = self.typ.parse(value)
        if self.low is not None and parsed < self.low:
            raise ValueError(f"Expected value >= {self.low} but got {parsed}.")
        if self.high is not None and parsed > self.high:
            raise ValueError(f"Expected value <= {self.high} but got {parsed}.")
        return parsed

    def render(self, value):
        return self.typ.render(value)

    def __repr__(self):
        return (
            f"ClampedNumber[{repr(self.typ)}, "
            f"{'-inf' if self.low is None else self.low}, "
            f"{'+inf' if self.high is None else self.high}]"
        )


class ClampedInt(ClampedNumber):
    """
    `ClampedInt(low, high)` creates a Hyperdiv type that
    accepts values of numeric Python type `int` that are between
    `low` and `high` (inclusive). If `low` or `high` are set to `None`,
    the interval is open on that end.

    `ClampedInt()` is equivalent to `Int`, because the interval is
    open at both ends.
    """

    def __init__(self, low=None, high=None):
        super().__init__(int, low=low, high=high)


class ClampedFloat(ClampedNumber):
    """
    `ClampedFloat(low, high)` creates a Hyperdiv type that
    accepts values of numeric Python type `float` that are between
    `low` and `high` (inclusive). If `low` or `high` are set to `None`,
    the interval is open on that end.

    `ClampedFloat()` is equivalent to `Float`, because the interval is
    open at both ends.
    """

    def __init__(self, low=None, high=None):
        super().__init__(float, low=low, high=high)
