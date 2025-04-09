from .. import design_tokens as tokens
from .hyperdiv_type import HyperdivType
from .design_token import DesignToken
from .color_constant import ColorConstant

ColorToken = DesignToken(tokens.Color)


class ColorDef(HyperdivType):
    """
    Defines the color values available for use in Hyperdiv. A
    color value can be one of:

    * A @design_token(Color) token
    * A @prop_type(ColorConstant)

    * A 6-tuple of the form `("color-mix", c1, p1, c2, p2, cs)`,
      representing a blending between colors `c1` and `c2`:

      * `c1` and `c2` are color values accepted by this `Color` type.
      * A percent `p1` of the color `c1` is mixed with a percent `p2`
        of the color `c2`.
      * Percent values `p1` and `p2` are floats between `0` and `1`.
      * `cs` is a colorspace constant, one of `"srgb"` or `"hsl"`.

    ## Color Mixing

    Hyperdiv @design_token(Color) tokens provide stepped constants
    like `"red-100"` and `"red-200"`. Color mixing providees colors
    that blend between these constants, enabling subtler color
    palettes.

    Color mixing is provided by the built-in functions
    @component(color_mix), @component(lighten), and
    @component(darken), so you won't have to construct color mixing
    tuples by hand.

    Color mixing is implemented in terms of CSS
    [color-mix](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix).

    ## Color Constants

    Although this type supports arbitrary hex/rgb/rgba colors by
    including @prop_type(ColorConstant), it is recommended to use the
    built-in @design_token(Color) design tokens, as these are designed
    to be visually consistent and render correctly in both light and
    dark mode. If you use a @prop_type(ColorConstant), the same color
    will be rendered regardless of mode, unless you manually set
    different color constants for each mode.
    """

    def parse(self, value):
        if value is None:
            return value

        try:
            return ColorToken.parse(value)
        except Exception:
            pass

        try:
            return ColorConstant.parse(value)
        except Exception:
            pass

        if isinstance(value, tuple) and len(value) == 6 and value[0] == "color-mix":
            _, c1, p1, c2, p2, cs = value
            c1 = self.parse(c1)
            c2 = self.parse(c2)
            if p1 < 0 or p1 > 1 or p2 < 0 or p1 > 1:
                raise ValueError("For color percent, values should be between 0 and 1.")
            if cs not in ("srgb", "hsl"):
                raise ValueError("Unknown color space.")
            return ("color-mix", c1, p1, c2, p2, cs)

        raise ValueError(f"Unknown color: {value}")

    def render(self, value):
        if value is None:
            return None

        if isinstance(value, tuple) and value[0] == "color-mix":
            _, c1, p1, c2, p2, cs = value
            c1 = self.render(c1)
            c2 = self.render(c2)
            return f"color-mix(in {cs}, {c1} {p1*100:.2f}%, {c2} {p2*100:.2f}%)"

        try:
            return ColorToken.render(value)
        except Exception:
            pass

        return ColorConstant.render(value)


Color = ColorDef()


def color_mix(color1, percent1, color2, percent2, color_space="srgb"):
    """
    Returns a @prop_type(Color) value that blends `percent1`
    percent of `color1` with `percent2` percent of color
    `color2`. Percentages are floats between `0` and `1` and colors
    are values accepted by the type @prop_type(Color). `color_space`
    can be one of `"srgb"` or `"hsl"`.

    For example, here is a gradual blending between `"blue-400"` and
    `"amber-100"`:

    ```py
    s = hd.slider(min_value=0, max_value=1, step=0.01)
    bg_color = hd.color_mix(
        "blue-400",
        1-s.value,
        "amber-100",
        s.value
    )
    with hd.box(
        padding=1,
        background_color=bg_color
    ):
        hd.text(
            f'hd.color_mix("blue-400", {1-s.value:.2f}, "amber-100", {s.value:.2f})',
            font_family="mono"
        )
    ```

    Also see @component(lighten) and @component(darken).
    """
    return ("color-mix", color1, percent1, color2, percent2, color_space)


def lighten(color, percent, color_space="srgb"):
    """
    It blends the given `color` into `"neutral-0"`. `percent` is a
    value between `0` and `1`, determining the intensity of the
    blending.

    Important: `"neutral-0"` is black in light mode and white in
    dark mode. So this function will physcally lighten a color in light
    mode but will darken it in dark mode.

    ```py
    s = hd.slider(min_value=0, max_value=1, step=0.01)
    bg_color = hd.lighten(
        "blue-400",
        s.value
    )
    with hd.box(
        padding=1,
        background_color=bg_color
    ):
        hd.text(
            f'hd.lighten("blue-400", {s.value:.2f})',
            font_family="mono",
            font_color=("neutral-900" if s.value >= 0.3 else "neutral-0")
        )
    ```

    Also see @component(color_mix) and @component(darken).
    """
    return ("color-mix", color, 1 - percent, "neutral-0", percent, color_space)


def darken(color, percent, color_space="srgb"):
    """
    It blends the given `color` into `"neutral-1000"`. `percent` is a
    value between `0` and `1`, determining the intensity of the
    blending.

    Important: `"neutral-1000"` is white in light mode and black in
    dark mode. So this function will physcally darken a color in light
    mode but will lighten it in dark mode.

    ```py
    s = hd.slider(min_value=0, max_value=1, step=0.01)
    bg_color = hd.darken(
        "blue-400",
        s.value
    )
    with hd.box(
        padding=1,
        background_color=bg_color
    ):
        hd.text(
            f'hd.darken("blue-400", {s.value:.2f})',
            font_family="mono",
            font_color=("neutral-900" if s.value < 0.3 else "neutral-0")
        )
    ```

    Also see @component(color_mix) and @component(lighten).
    """
    return ("color-mix", color, 1 - percent, "neutral-1000", percent, color_space)
