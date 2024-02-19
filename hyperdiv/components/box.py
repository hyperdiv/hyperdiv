from functools import partial

from ..component_base import Component
from ..component_mixins.boxy import Boxy
from ..component_mixins.styled import Styled


class box(Component, Boxy, Styled):
    """
    `box` is the fundamental layout component in Hyperdiv. Its box
    props give you flexible control over how the children of the box
    are laid out. By nesting boxes, you can create complex app layouts
    with side bars, top bars, etc.

    ## Layout Direction

    By default, boxes align their children vertically, one under the
    other.

    ```py
    with hd.box():
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 1")
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 2")
    ```

    Horizontal layout:

    ```py
    with hd.box(direction="horizontal"):
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 1")
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 2")

    # hd.hbox() is a synonym for
    # hd.box(direction="horizontal")

    with hd.hbox():
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 1")
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 2")
    ```

    ## Gaps

    Boxes let you add uniform gaps between children:

    ```py
    with hd.box(gap=1, border="1px solid yellow"):
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 1")
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 2")
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 3")

    with hd.hbox(gap=1, border="1px solid green"):
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 1")
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 2")
        with hd.box(border="1px solid red"):
            hd.plaintext("Child 3")
    ```

    ## Alignment and Justification

    `box` exposes two props, `align` and `justify`, that can be used
    to control the positioning of the box's children.

    These props behave differently depending on the box's
    direction.

    In vertical boxes, `align` controls the positioning of children
    along the horizontal direction, and `justify` controls the
    positioning of children along the vertical direction.

    In horizontal boxes, `align` controls the positioning of children
    along the vertical direction, and `justify` controls the
    positioning of children along the horizontal direction.

    ```py
    align = hd.radio_group(
        "Align:",
        options=(
            "start", "end", "center", "stretch"
        ),
        value='start')

    justify = hd.radio_group(
        "Justify:",
        options=(
            "start", "end", "center", "space-between",
            "space-around", "space-evenly"
        ),
        value="start")

    def box(name):
        with hd.box(border="1px solid red"):
            hd.plaintext(name)

    hd.markdown("### Vertical box:")

    with hd.box(
        border="1px solid yellow",
        height=15,
        align=align.value,
        justify=justify.value,
    ):
        box("Child 1")
        box("Child 2")
        box("Child 3")

    hd.markdown("### Horizontal box:")

    with hd.hbox(
        border="1px solid yellow",
        height=15,
        align=align.value,
        justify=justify.value,
    ):
        box("Child 1")
        box("Child 2")
        box("Child 3")
    ```

    ## Scrolling

    `box` provides the boolean `horizontal_scroll` and
    `vertical_scroll` props to control whether content should scroll
    or clip in those respective directions.

    By default, these props are set to `None`, which causes child
    content to visibly overflow outside the boundaries of the parent.

    When either of these props is set to a value other than `None`, if
    the other prop is `None`, it will behave like it is set to `True`.

    When either of these props is set to `True`, the child content
    will scroll in that direction.

    When either of these props is set to `False`, the child content is
    clipped and will *not* scroll in that direction.

    ```py
    horizontal = hd.radio_group(
        "Horizontal Scroll",
        options=("None", "True", "False"),
        value="None"
    )
    vertical = hd.radio_group(
        "Vertical Scroll",
        options=("None", "True", "False"),
        value="None"
    )


    def parse(value):
        if value == "None":
            return None
        if value == "True":
            return True
        return False

    with hd.box(
        border="1px solid red",
        height=5,
        width=5,
        vertical_scroll=parse(vertical.value),
        horizontal_scroll=parse(horizontal.value),
    ):
        with hd.box(
            border="1px solid green",
            height=10,
            width=10,
            shrink=False,
        ):
            hd.text("Overflowing Child Box")
    ```

    """

    _tag = "div"
    _classes = ["box"]


vbox = partial(box, direction="vertical")
hbox = partial(box, direction="horizontal")
