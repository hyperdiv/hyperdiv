from .hyperdiv_type import HyperdivType


class ColorConstantDef(HyperdivType):
    """
    Defines a hex, rgb, or rgba color constant.

    The accepted value shapes are:

    * Hex: A string of length 7 that starts with a `#`, which is followed
      by 6 characters in the rage `[0-9a-f]`.
    * RGB: A tuple of 3 integers in the range `0-255`.
    * RGBA: A tuple of 4 numbers. The first three are integers in the
      range `0-255` representing RGB values. The fourth is a float in
      the range `0-1` representing opacity, where `0` is fully transparent
      and `1` is fully opaque.

    Examples:
    ```py
    hd.box(
        width=2,
        height=2,
        background_color="#558833"
    )
    hd.box(
        width=2,
        height=2,
        background_color=(128, 0, 200)
    )
    hd.box(
        width=2,
        height=2,
        background_color=(128, 0, 200, 0.5)
    )
    ```
    """

    def parse(self, value):
        if isinstance(value, str):
            if not value.startswith("#"):
                raise ValueError('Expected a hex constant to start with "#".')
            if value.startswith("#"):
                if len(value) not in (4, 5, 7, 9):
                    raise ValueError(f"Invalid length of hex color: {value}")
                for c in value[1:]:
                    if not (c.isdigit() or c in ("a", "b", "c", "d", "e", "f")):
                        raise ValueError(f"Unexpected character {c} in hex constant.")
        elif isinstance(value, tuple):
            if len(value) not in (3, 4):
                raise ValueError("Unexpected rgb/rgba color constant.")
            for c in value[:3]:
                if not (isinstance(c, int) and c >= 0 and c <= 255):
                    raise ValueError(f"Unexpected component {c} in rgb/rgba constant.")
            if len(value) == 4:
                opacity = value[3]
                if opacity < 0 or opacity > 1:
                    raise ValueError(f"Unexpected opacity {opacity} in rgba constant.")
        else:
            raise ValueError("Unexpected color format.")
        return value

    def render(self, value):
        if isinstance(value, str):
            return value
        if len(value) == 3:
            return f"rgb{value}"
        else:
            return f"rgba{value}"

    def __repr__(self):
        return "ColorConstant"


ColorConstant = ColorConstantDef()
