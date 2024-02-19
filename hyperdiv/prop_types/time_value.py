from .hyperdiv_type import HyperdivType


class TimeValueDef(HyperdivType):
    """
    A type that supports time values. See
    [here](https://developer.mozilla.org/en-US/docs/Web/CSS/time).

    It accepts a numeric value followed by a unit, where the unit has
    to be one of `"s"` (seconds) or `"ms"` (milliseconds).

    The value shape can be either a string, like `"12ms"`, or a tuple
    like `(12, "ms")`.

    Examples:

    ```py
    "12ms"
    "+12.5ms"
    "-1.6s"
    (12, "ms")
    (12.5, "ms")
    (-1.6, "s")
    ```
    """

    def parse(self, value):
        if isinstance(value, (tuple, list)):
            if len(value) != 2:
                raise ValueError(f"Expected a tuple of length 2 but got {value}")
            scalar, unit = value
            unit = unit.lower()
            if unit not in ("s", "ms"):
                raise ValueError(f"Unknown unit for TimeValue: {unit}")
            if not isinstance(scalar, (int, float)):
                raise ValueError(f"Expected an int or float but got {scalar}")
        else:
            value = value.lower()
            if value.endswith("ms"):
                unit = "ms"
                scalar = value[:-2]
            elif value.endswith("s"):
                unit = "s"
                scalar = value[:-1]
        return (float(scalar), unit)

    def render(self, value):
        scalar, unit = value
        return f"{scalar}{unit}"

    def __repr__(self):
        return "TimeValue"


TimeValue = TimeValueDef()
