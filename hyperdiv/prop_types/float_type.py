from .native import Native


class FloatDef(Native):
    """
    Accepts only Python `float` and `int` values. `int` values are
    coerced to `float` by calling `float()` on them.
    """

    def __init__(self):
        super().__init__(float, coercible_types=[int])

    def render(self, value):
        """Specialized render function for floats.

        We need this because `json` will render float('inf') and
        float('-inf') as special constants that don't correspond to
        anything in JS. The strings "+Infinity" and "-Infinity" behave
        correctly when coerced to numbers on the JS side.
        """
        if value == float("inf"):
            return "+Infinity"
        if value == float("-inf"):
            return "-Infinity"
        return value


Float = FloatDef()
