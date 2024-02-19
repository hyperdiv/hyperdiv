from .hyperdiv_type import HyperdivType
from .common_type_defs import Size


def uniform_box(values):
    return len(values) == 4 and all([v == values[0] for v in values[1:]])


class BoxSizeDef(HyperdivType):
    """
    A type that accepts size values defining all four edges or corners
    of a box. It can be used for the padding, margin, border radius,
    etc., of a Hyperdiv component.

    The values of this type are either

    * A single @prop_type(Size) value, in which case all four dimensions are set
      simultaneously to that size.

    * A four-tuple of @prop_type(Size) values, in which case the dimensions are
      set independently.

    The canonical value shape of this type is a four-tuple of
    canonical @prop_type(Size) shapes.

    Example values:

    ```py-nodemo
    1.5
    "10px"
    (10, "px")
    (1, 1, 1, 1)
    (1, "10px", (1.5, "rem"), "2vh")
    ```

    """

    def parse(self, value):
        if value is None:
            return None

        try:
            val = Size.parse(value)
            return tuple([val] * 4)
        except Exception:
            pass

        try:
            iter(value)
            assert 0 < len(value) <= 4
        except Exception:
            raise ValueError(f"Invalid box size value: {value}")

        output = []

        for v in value:
            output.append(Size.parse(v))

        while len(output) < 4:
            output.append(Size.parse(0))

        return tuple(output)

    def render(self, value):
        if not value:
            return None

        if uniform_box(value):
            return Size.render(value[0])

        return " ".join([Size.render(v or (0, "px")) for v in value])

    def __repr__(self):
        return "BoxSize"


BoxSize = BoxSizeDef()
