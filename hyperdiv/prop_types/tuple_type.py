from .hyperdiv_type import HyperdivType


class Tuple(HyperdivType):
    """
    `Tuple(type1, type2, ... typeN)` creates a Hyperdiv type that
    accepts Python tuples of the shape `(value1, value2, ... valueN)`
    such that `value1` has Hyperdiv type `type1`, `value2` has
    Hyperdiv type `type2`, and so on.

    For example `hd.Tuple(hd.Int, hd.PureString)` will accept values
    like `(1, "Hello")`, `(50, "Bunnies")`, etc.

    The internally stored value is a tuple of values parsed by their
    respective types.
    """

    def __init__(self, *types):
        self.types = types

    def parse(self, value):
        if not isinstance(value, (tuple, list)):
            raise ValueError(f"Expected a tuple or list but got {type(value)}")

        if len(value) != len(self.types):
            raise ValueError(
                f"Tuple should have length {len(self.types)} but got {len(value)}"
            )

        output = []
        for i, component in enumerate(value):
            output.append(self.types[i].parse(component))
        return tuple(output)

    def render(self, value):
        output = []
        for i, component in enumerate(value):
            output.append(self.types[i].render(component))
        return tuple(output)

    def __repr__(self):
        args_str = ", ".join(repr(t) for t in self.types)
        return f"Tuple[{args_str}]"
