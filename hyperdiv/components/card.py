from ..prop_types import Color, CSSField, Union, DesignToken, BoxSize, Size
from ..prop import Prop
from ..component_base import Component
from ..slot import Slot
from ..component_mixins.styled import Styled
from .. import design_tokens as tokens
from ..style_part import BasePart, StylePart


class card(Component, Styled):
    """
    A component that groups an image, a header, a footer, and contents
    into a container. All the slots are optional and can be combined
    in various ways.

    ### Image with contents

    ```py
    with hd.card() as card:
        hd.image("/assets/kitten.jpg", slot=card.image)
        with hd.box(gap=0.5):
            hd.text("Mittens", font_weight="bold")
            hd.text("Bring this kitten home.", font_size="small")
            hd.text("6 weeks old", font_color="neutral-400", font_size="x-small")
    ```

    ### Header

    ```py
    with hd.card() as card:
        with hd.hbox(slot=card.header, justify="space-between", align="center"):
            hd.text("Settings")
            hd.icon_button("gear")
        hd.text("This card has a header.")
    ```

    ### Footer

    ```py
    with hd.card() as card:
        hd.text("This card has a footer.")
        hd.button("Learn more", variant="primary", pill=True, slot=card.footer)
    ```

    """

    _tag = "sl-card"

    # The card's border color.
    card_border_color = Prop(CSSField("--border-color", Color))
    # The card's border radius.
    card_border_radius = Prop(
        CSSField(
            "--border-radius",
            Union(
                DesignToken(tokens.BorderRadius),
                BoxSize,
            ),
        )
    )
    # The card's border width.
    card_border_width = Prop(CSSField("--border-width", Size))
    # The card's padding.
    card_padding = Prop(CSSField("--padding", BoxSize))

    header = Slot()
    footer = Slot()
    image = Slot()

    base_style = Prop(BasePart())
    image_style = Prop(StylePart("image"))
    header_style = Prop(StylePart("header"))
    body_style = Prop(StylePart("body"))
    footer_style = Prop(StylePart("footer"))
