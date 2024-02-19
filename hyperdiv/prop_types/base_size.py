from .hyperdiv_type import HyperdivType


def parse_number(string, low=float("-inf"), high=float("+inf")):
    num = None
    try:
        num = int(string)
    except Exception:
        pass

    if num is None:
        try:
            num = float(string)
        except Exception:
            pass

    if num is not None and num >= low and num <= high:
        return num

    raise ValueError(f"{string} is not a number between {low} and {high}.")


class BaseSizeDef(HyperdivType):
    """
    A hyperdiv type that accepts generic size values that can be used
    to define the widths, heights, padding, margins, of components,
    gaps between components, border sizes, etc.

    This type accepts the following shapes of values:

    * `None`, an unspecified size, denoting default browser behavior.

    * The string `"fit-content"`, denoting that the component should
      be only large enough to fit its interior content.

    * A bare floating point number or integer, which is implicitly
      assigned the unit `"rem"` (more on this below).

    * A 2-tuple of a number and a unit. For example `(10, "px")`,
      which denotes a size of 10 pixels.

    * A string notation for the 2-tuple notation above, concatenating
      the number and the unit. For example, `"10px"`.

    The supported units are:

    * `rem`: This is the default, when no unit is specified. `rem` is
      a multiplier of the "base font size", which by default is 16
      pixels. `"1rem"` means 16 pixels. `"0.5rem"` means 8
      pixels. `"2rem"` means 32 pixels, etc. This is the recommended
      unit to use, because the entire UI can be scaled up and down by
      modifying only the base font size.

    * `em`: A multiplier of the font size of the parent
      component. This works like `rem` but instead of being a
      multiplier of the root font size, it is a multiplier of the font
      size of the parent component that the given component is nested
      inside of.

    * `px`: Pixels.

    * `%`: A percentage of some other value. For example a width of
      `"50%"` on a component means half the width of its parent
      component.

    * `vh`: A percentage of the *viewport height*. The viewport is the
      size of the browser window the app is running in.

    * `vw`: A percentage of the *viewport width*.

    Examples:

    ```py
    def box(width):
        with hd.box(
            border="1px solid red",
            padding=0.5,
            width=width
        ):
            hd.text(width)

    box("fit-content")
    box(8)
    box("8rem") # Equivalent to the above
    box("50%")
    box("10vw")
    box("90px")

    hd.markdown("## Tuple notation:")

    box((8, "rem"))
    box((50, "%"))
    box((10, "vw"))
    box((90, "px"))
    ```

    The canonical value stored by this type is either the string
    `"fit-content"` or a tuple of `(value, unit)`.

    """

    def parse(self, value):
        def parse_tuple(num, units):
            if units not in ("em", "px", "vh", "vw", "%", "rem"):
                raise ValueError(f"Invalid size expression: {value}.")
            try:
                high = 100
                if units in ("em", "rem", "px"):
                    high = float("+inf")
                num = parse_number(num, low=0, high=high)
                return (num, units)
            except Exception:
                raise ValueError(f"Invalid size expression: {value}.")

        default_unit = "rem"

        if value is None:
            return None

        if value == "fit-content":
            return value

        if isinstance(value, (tuple, list)) and len(value) == 2:
            return parse_tuple(*value)

        if isinstance(value, (float, int)) and value >= 0:
            return (value, default_unit)

        if not isinstance(value, str):
            raise ValueError(f"Invalid size expression: {value}")

        try:
            num = parse_number(value, low=0)
            return (num, default_unit)
        except Exception:
            pass

        if value.endswith("%"):
            try:
                num = parse_number(value[:-1], low=0)
                return (num, "%")
            except Exception as e:
                raise ValueError(f"Invalid percent expression: {value} ({e})")

        if len(value) < 3:
            raise ValueError(f"Invalid size expression: {value}")

        units = value.strip(".0123456789")
        number_str = value[: -len(units)]

        return parse_tuple(number_str, units)

    def render(self, value):
        if value is None:
            return None
        if value == "fit-content":
            return value
        num, units = value
        return f"{num}{units}"

    def __repr__(self):
        return "BaseSize"


BaseSize = BaseSizeDef()
