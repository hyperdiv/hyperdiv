from .. import design_tokens as tokens
from .optional import Optional
from .union import Union
from .design_token import DesignToken
from .base_size import BaseSize
from .color_constant import ColorConstant


# Defines the color constants available for use in Hyperdiv. Note that
# although this type supports arbitrary hex/rgb/rgba colors by
# including @prop_type(ColorConstant), it is recommended to use the
# built-in @design_token(Color) design tokens, as these are designed
# to be visually consistent and render correctly in both light and
# dark mode. If you use a @prop_type(ColorConstant), the same color
# will be rendered regardless of mode, unless you explicitly use
# different color constants for each mode.
Color = Optional(Union(DesignToken(tokens.Color), ColorConstant))
# A type that defines component dimensions and spacing. This type
# accepts `Spacing` tokens in addition to `BaseSize` values.
Size = Union(DesignToken(tokens.Spacing), BaseSize)
