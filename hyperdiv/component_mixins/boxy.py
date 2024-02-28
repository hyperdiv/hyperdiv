from ..prop_types import Bool, CSSField, OneOf, Optional, Size
from ..prop import Prop


class DirectionDef(CSSField):
    """
    Represents the layout direction of @component(box) components.
    """

    def __init__(self):
        super().__init__(
            "flex-direction",
            OneOf(
                None, "horizontal", "vertical", "horizontal-reverse", "vertical-reverse"
            ),
        )

    def render(self, value):
        if value is None:
            return None

        css_value = None
        if value == "vertical":
            css_value = "column"
        elif value == "horizontal":
            css_value = "row"
        elif value == "vertical-reverse":
            css_value = "column-reverse"
        elif value == "horizontal-reverse":
            css_value = "row-reverse"

        return {"flex-direction": css_value}

    def __repr__(self):
        return "Direction"


class ScrollDef(Optional):
    """
    Defines whether the content inside a component can scroll within
    the component's "box". The accepted values are:

    * `None` - Unspecified/default behavior.

    * `True` - The component's contents will scroll when they overflow
      the component's dimensions.

    * `False` - The component's contents will not scroll.

    """

    def __init__(self):
        super().__init__(Bool)

    def render(self, value):
        if value is None:
            return None
        return "auto" if value else "hidden"

    def __repr__(self):
        return "Scroll"


Scroll = ScrollDef()
Direction = DirectionDef()


class Boxy:
    """
    A collection of props for components that are containers. These
    props control how the children of the component are organized inside
    the component.
    """

    """
    Whether the children of the component are placed side by side
    (`"horizontal"`) or stacked vertically, with each subsequent
    component being placed below the previous. In the case of the
    `-reverse` values, the components are rendered in reverse,
    starting at the opposite edge:

    ```py
    hd.markdown("`horizontal`:")

    with hd.box(
        padding=1,
        gap=1,
        direction="horizontal",
        border="1px solid red"
    ):
        hd.button("B1")
        hd.button("B2")

    hd.markdown("`horizontal-reverse`:")

    with hd.box(
        padding=1,
        gap=1,
        direction="horizontal-reverse",
        border="1px solid red"
    ):
        hd.button("B1")
        hd.button("B2")
    ```

    The `-reverse` values are rarely used, but they come in handy in
    niche cases. For example, when building a chat UI, the component
    that contains the chat messages may be set to
    `"vertical-reverse"`. That way, new messages are naturally inserted
    at the bottom and the component naturally stays scrolled to the
    bottom as new messages are inserted.
    """
    direction = Prop(Direction)
    # This prop controls how child components are placed *along the
    # direction* of the component. If the component is `"horizontal"`,
    # this prop controls the horizontal alignment of the children. If
    # the component is `"vertical"`, this prop controls the vertical
    # alignment of the children.
    align = Prop(
        CSSField(
            "align-items",
            OneOf(
                None,
                "start",
                "center",
                "end",
                "stretch",
            ),
        )
    )
    # This prop complements `direction` and controls how child
    # components are placed on the axis *opposite to the direction* of
    # the component. If the component is `"horizontal"`, this prop
    # controls the *vertical* alignment of the children. If the
    # component is `"vertical"`, this prop control the *horizontal*
    # alignment of the children.
    justify = Prop(
        CSSField(
            "justify-content",
            OneOf(
                None,
                "start",
                "center",
                "end",
                "space-between",
                "space-around",
                "space-evenly",
                "stretch",
            ),
        )
    )
    # The gap space between the children of the component.
    gap = Prop(CSSField("gap", Size))
    # Whether this component can scroll horizontally.
    horizontal_scroll = Prop(CSSField("overflow-x", Scroll))
    # Whether this component can scroll vertically.
    vertical_scroll = Prop(CSSField("overflow-y", Scroll))
    # Whether the components children should wrap around when they run
    # out of space. For example, in a component with
    # `direction="horizontal"`, children are placed side by side. When
    # there are too many children to fit within the width of the
    # component, and `wrap` is set to `"wrap"`, the children will wrap
    # around onto a new "row" starting at the left edge again.
    wrap = Prop(CSSField("flex-wrap", Optional(OneOf("wrap", "nowrap", "reverse"))))

    def __init__(self):
        """
        `Boxy` cannot be instantiated.
        """
        raise Exception("`Boxy` cannot be instantiated.")
