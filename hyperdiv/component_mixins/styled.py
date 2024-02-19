from ..prop_types import (
    CSS,
    Native,
    Color,
    Border,
    BorderEdge,
    BoxSize,
    CSSField,
    Int,
    OneOf,
    Optional,
    Size,
    Union,
    DesignToken,
    BaseSize,
)
from ..prop import Prop
from .. import design_tokens as tokens
from .slottable import Slottable


class BackgroundGradientDef(CSS):
    """
    Represents background color gradient values. The accepted values
    are either `None`, or 3-tuples `(degree, color_start, color_end)`
    of types (@prop_type(Int), @prop_type(Color), @prop_type(Color)).

    The `degree` component determines the angle, in degrees, at which
    to render the gradient. The `start_color` and `end_color` are the
    two colors between which the gradient will blend.

    ```py
    hd.box(
        height=5,
        width=5,
        background_gradient=(0, "red", "blue")
    )
    hd.box(
        height=5,
        width=5,
        background_gradient=(45, "green-200", "purple")
    )
    ```
    """

    def parse(self, value):
        if value is None:
            return None
        if isinstance(value, tuple) and len(value) == 3:
            deg, start, end = value
            deg = Int.parse(deg)
            start = Color.parse(start)
            end = Color.parse(end)
            return (deg, start, end)
        raise ValueError(f"Unexpected value: {value}")

    def render(self, value):
        if value is None:
            return None
        deg, start, end = value
        return {
            "background-image": (
                f"linear-gradient({Int.render(deg)}deg, "
                f"{Color.render(start)}, {Color.render(end)})"
            )
        }

    def __repr__(self):
        return "BackgroundGradient"


BackgroundGradient = BackgroundGradientDef()


class TextGradientDef(BackgroundGradientDef):
    """
    A type that takes the same values as
    @prop_type(BackgroundGradient) but represents the gradient color
    of *text* inside a box, as opposed to the background gradient of
    the box.

    ```py
    hd.text(
        "Gradient",
        width="fit-content",
        font_size=3,
        font_weight="bold",
        text_gradient=(0, "red", "blue")
    )
    hd.text(
        "Gradient",
        width="fit-content",
        font_size=3,
        font_weight="bold",
        text_gradient=(45, "emerald", "rose")
    )
    ```
    """

    def render(self, value):
        if value is None:
            return None
        rendered = super().render(value)
        return rendered | {
            "background-clip": "text",
            "-webkit-background-clip": "text",
            "color": "transparent",
        }

    def __repr__(self):
        return "TextGradient"


TextGradient = TextGradientDef()

# A type that takes @prop_type(Color) values, used to style the
# backgrounds of components.
BackgroundColor = CSSField("background-color", Color)
# A type whose values represent the line heights of text. In addition
# to @design_token(LineHeight) values, it accepts generic
# @prop_type(Size) values like `3.5` or `"10px"`, or `"x-small"`.
LineHeight = CSSField("line-height", Union(DesignToken(tokens.LineHeight), Size))
# A type that takes font size values, used to style the font sizes of
# components. In addition to @design_token(FontSize) values, it
# accepts generic @prop_type(BaseSize) values like `3.5` or `10px`.
FontSize = CSSField("font-size", Union(DesignToken(tokens.FontSize), BaseSize))
# A type that takes @prop_type(Size) values and represents the widths
# of components.
Width = CSSField("width", Size)
# A type that takes @prop_type(Size) values and represents the heights
# of components.
Height = CSSField("height", Size)


class Styled(Slottable):
    """A collection of props defining element style."""

    # The width of the component.
    width = Prop(Width)
    # The height of the component.
    height = Prop(Height)
    # The minimum width of the component. The component may be wider
    # than this value, but not narrower.
    min_width = Prop(CSSField("min-width", Size))
    # The minimum height of the component. The component may be taller
    # than this value, but not shorter.
    min_height = Prop(CSSField("min-height", Size))
    # The maximum width of the component. The component may be
    # narrower than this value, but not wider.
    max_width = Prop(CSSField("max-width", Size))
    # The maximum height of the component. The component may be
    # shorter than this value, but not taller.
    max_height = Prop(CSSField("max-height", Size))
    # Whether the component should expand to take up as much space as
    # it can.
    grow = Prop(
        CSSField(
            "flex-grow",
            Optional(
                Native(int, coercible_types=[bool]),
            ),
        )
    )
    # Whether the component is allowed to shrink within its parent
    # component when other sibling components try to claim space. It
    # may be necessary to set `shrink` to `True` in addition to setting
    # a `width` or `height` value, to prevent the component from
    # shrinking below that value.
    shrink = Prop(
        CSSField(
            "flex-shrink",
            Optional(
                Native(int, coercible_types=[bool]),
            ),
        )
    )
    # The basis sets the "initial size" allocated to the component
    # before its actual size is calculated. If you want children with
    # equal-width, it helps to set an equal basis on all of them.
    basis = Prop(
        CSSField(
            "flex-basis",
            Optional(Size),
        ),
    )
    # The border of the component. This prop sets the border
    # simultaneously for all four edges (top, right, bottom, left).
    border = Prop(Border)
    # The border of the top edge.
    border_top = Prop(CSSField("border-top", BorderEdge))
    # The border of the left edge.
    border_left = Prop(CSSField("border-left", BorderEdge))
    # The border of the bottom edge.
    border_bottom = Prop(CSSField("border-bottom", BorderEdge))
    # The border of the right edge.
    border_right = Prop(CSSField("border-right", BorderEdge))
    # The border radius of the component -- how round its corners
    # are. When using @prop_type(BoxSize) values, the four values represent the
    # four corners starting at the top-left corner and going
    # clockwise.
    border_radius = Prop(
        CSSField("border-radius", Union(DesignToken(tokens.BorderRadius), BoxSize))
    )
    # The margin of the component -- the space "around" the edges of
    # the component. This prop sets the margin
    # simultaneously for all four edges (top, right, bottom, left).
    margin = Prop(CSSField("margin", BoxSize))
    # The margin of the top edge.
    margin_top = Prop(CSSField("margin-top", Size))
    # The margin of the left edge.
    margin_left = Prop(CSSField("margin-left", Size))
    # The margin of the bottom edge.
    margin_bottom = Prop(CSSField("margin-bottom", Size))
    # The margin of the right edge.
    margin_right = Prop(CSSField("margin-right", Size))
    # The padding of the component -- the space "within" the edges of
    # the component; the space between the edges of the component and
    # its internal content. This prop sets the padding simultaneously
    # for all four edges (top, right, bottom, left).
    padding = Prop(CSSField("padding", BoxSize))
    # The padding of the top edge.
    padding_top = Prop(CSSField("padding-top", Size))
    # The padding of the left edge.
    padding_left = Prop(CSSField("padding-left", Size))
    # The padding of the bottom edge.
    padding_bottom = Prop(CSSField("padding-bottom", Size))
    # The padding of the right edge.
    padding_right = Prop(CSSField("padding-right", Size))
    # The color of the background surface of the component -- the
    # total surface contained within its borders. The background color
    # encompasses the content and padding of the component, but not
    # its margins.
    background_color = Prop(BackgroundColor)
    # This prop works like `background_color` but sets the background
    # color to a gradient blending between multiple colors, instead of
    # a fixed color.
    background_gradient = Prop(BackgroundGradient)
    # This prop sets the color of the *text content* within a
    # component to a color gradient.
    text_gradient = Prop(TextGradient)
    # The background color of the component when the mouse pointer is
    # hovered over the component's area.
    hover_background_color = Prop(BackgroundColor)
    # The background color of the component when the mouse is actively
    # being clicked within the component's area.
    active_background_color = Prop(BackgroundColor)
    # The font color of the text within the component.
    font_color = Prop(CSSField("color", Color))
    # The font size of the text within the component.
    font_size = Prop(FontSize)
    # The font family of the text within the component.
    font_family = Prop(
        CSSField("font-family", Optional(DesignToken(tokens.FontFamily)))
    )
    # The font weight (how bold the font is) of the text within the
    # component.
    font_weight = Prop(
        CSSField("font-weight", Optional(DesignToken(tokens.FontWeight)))
    )
    # How spaced apart the letters of the font within the component
    # are.
    letter_spacing = Prop(
        CSSField("letter-spacing", Union(DesignToken(tokens.LetterSpacing), Size))
    )
    # How much vertical space each line of text within the component
    # occupies.
    line_height = Prop(LineHeight)
    # What the mouse cursor looks like when the mouse pointer is
    # hovered over the component surface.
    cursor = Prop(
        CSSField(
            "cursor",
            OneOf(
                None,
                "pointer",
                "text",
                "move",
                "not-allowed",
                "grab",
            ),
        )
    )
    # The drop shadow of the component -- the shadow that the
    # component box casts on the background surface.
    shadow = Prop(CSSField("box-shadow", Optional(DesignToken(tokens.Shadow))))
    # How the text within the component is horizontally aligned.
    text_align = Prop(CSSField("text-align", OneOf(None, "start", "center", "end")))
    # Whether the text should wrap.
    white_space = Prop(CSSField("white-space", OneOf(None, "normal", "nowrap")))

    def __init__(self):
        """
        `Styled` cannot be instantiated.
        """
        raise Exception("`Styled` cannot be instantiated.")
