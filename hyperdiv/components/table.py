from math import ceil
from ..component_base import Component
from ..component_mixins.styled import Styled
from ..prop_types import CSSField, OneOf, Int
from ..prop import Prop
from .common.text_utils import concat_text
from .common.label_component import LabelComponent
from .plaintext import plaintext


class table(Component, Styled):
    """An HTML table component. Using @component(thead),
    @component(tbody), @component(tfoot), @component(tr),
    @component(td), you can manually assemble tables.

    ```py
    with hd.table():
        # Table header
        with hd.thead():
            # Header row
            with hd.tr():
                hd.td("Name")
                hd.td("Age")
                hd.td()
        # Table body
        with hd.tbody():
            # Body rows
            with hd.tr():
                hd.td("Amy")
                hd.td(28)
                with hd.td():
                    with hd.box(align="end"):
                        hd.button("Delete Amy")
            with hd.tr():
                hd.td("Jim")
                hd.td(35)
                with hd.td():
                    with hd.box(align="end"):
                        hd.button("Delete Jim")
        # Table footer
        with hd.thead():
            # Footer row
            with hd.tr():
                hd.td("Average Age")
                hd.td((28+35)/2)
                hd.td()
    ```

    Each of the table sections is optional.

    The direct children of `table` should be @component(thead),
    @component(tbody), or @component(tfoot), at most one of each.

    However, browsers are generally lenient and allow omitting the
    @component(tbody) wrapper, so you can nest rows (@component(tr)s)
    directly within `table`.

    ```py
    with hd.table():
        with hd.tr():
            hd.td("Amy")
            hd.td(28)
        with hd.tr():
            hd.td("Jim")
            hd.td(35)
    ```
    """

    _tag = "table"

    border_collapse = Prop(
        CSSField("border-collapse", OneOf("collapse", "separate")),
        "collapse",
    )

    def __init__(
        self,
        *,
        border="1px solid neutral-100",
        **kwargs,
    ):
        super().__init__(border=border, **kwargs)


class tr(Component, Styled):
    """
    A table row container. To be used with @component(table).

    Its direct children should be @component(td)s.
    """

    _tag = "tr"


class td(LabelComponent):
    """
    A table cell container. To be used with @component(table).

    Arbitrary components can be nested within a `td`. If you want to
    control the alignment of children, you should place a
    @component(box) in the `td`, and the children inside that
    box. `td` itself does not expose box props.

    ## Spans

    `td` supports props `colspan` and `rowspan` that allow a table
    cell to take up the space otherwise occupied by cells to the
    right, or cells below, respectively.

    Here's a 3 rows x 2 columns table:

    ```py
    with hd.table():
        with hd.tr():
            hd.td("(0, 0)")
            hd.td("(0, 1)")
        with hd.tr():
            hd.td("(1, 0)")
            hd.td("(1, 1)")
        with hd.tr():
            hd.td("(2, 0)")
            hd.td("(2, 1)")
    ```

    And using `colspan` and `rowspan`:

    ```py
    with hd.table():
        with hd.tr():
            hd.td("(0, 0) and (0, 1)", colspan=2)
            # No td for (0, 1)
        with hd.tr():
            hd.td("(1, 0) and (2, 0)", rowspan=2)
            hd.td("(1, 1)")
        with hd.tr():
            # No td for (2, 0)
            hd.td("(2, 1)")
    ```

    By default, `rowspan` and `colspan` are `1`, indicating that the
    cell takes up one cell's worth of space.
    """

    _tag = "td"

    # The horizontal/rightward span of this cell.
    colspan = Prop(Int, 1)
    # The vertical/downward span of this cell.
    rowspan = Prop(Int, 1)

    def __init__(
        self,
        *label,
        border="1px solid neutral-100",
        padding=(0.5, 0.8, 0.5, 0.8),
        **kwargs,
    ):
        super().__init__(*label, border=border, padding=padding, **kwargs)


class thead(Component, Styled):
    """
    A table header container. To be used with @component(table).

    Its direct children should be @component(tr)s.
    """

    _tag = "thead"

    def __init__(
        self,
        *,
        background_color="neutral-50",
        font_weight="bold",
        **kwargs,
    ):
        super().__init__(
            background_color=background_color,
            font_weight=font_weight,
            **kwargs,
        )


class tfoot(Component, Styled):
    """
    A table footer container. To be used with @component(table).

    Its direct children should be @component(tr)s.
    """

    _tag = "tfoot"

    def __init__(
        self,
        *,
        background_color="neutral-50",
        font_weight="bold",
        **kwargs,
    ):
        super().__init__(
            background_color=background_color,
            font_weight=font_weight,
            **kwargs,
        )


class tbody(Component, Styled):
    """
    A table body container. To be used with @component(table).

    Its direct children should be @component(tr)s.
    """

    _tag = "tbody"
