import re
from functools import cache
from .hyperdiv_type import HyperdivType
from .common_type_defs import Size, Color


class BorderEdgeDef(HyperdivType):
    """
    A Hyperdiv type that accepts values defining a single edge of a component's border.

    The value shapes accepted by this type are:

    * The Python value `None`, indicating that the border is unspecified.
    * The string constant `"none"`, indicating no border.
    * A 3-tuple of values `(size, style, color)`, indicating the size, style, and color
      of the border.
    * A string representation of the 3-tuple above, where the tuple is given as a
      string of the three values, separated by spaces.


    Example values:
    ```py-nodemo
    # Unspecified:
    None
    # No border:
    "none"

    # Using string syntax:
    "1 solid red"
    "10px dashed primary"

    # Using tuple syntax:
    (1, "solid", "red")
    ("10px", "dashed", "primary")
    ```

    The size part accepts the same values as the `Size` prop type.

    The style part accepts the values `"solid"`, `"dotted"`, and `"dashed"`.

    The color part accepts the same values as the `Color` prop type.
    """

    @cache
    def parse(self, value):
        if value is None:
            return None

        if value == "none":
            return value

        if isinstance(value, str):
            value = re.split(r"\s+", value)

        if len(value) != 3:
            raise ValueError(f"Invalid border value: {value}")

        size, style, color = value

        size = Size.parse(size)

        if style not in ("dotted", "dashed", "solid"):
            raise ValueError(f"Invalid border style: {style}")

        color = Color.parse(color)

        return size, style, color

    def render(self, value):
        if value is None:
            return None
        if value == "none":
            return value
        size, style, color = value
        return f"{Size.render(size)} {style} {Color.render(color)}"

    def __repr__(self):
        return "BorderEdge"


BorderEdge = BorderEdgeDef()
