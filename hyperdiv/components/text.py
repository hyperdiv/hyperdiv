from ..prop import Prop
from ..prop_types import String
from ..component_base import Component
from ..component_mixins.styled import Styled
from .common.text_utils import concat_text


class text(Component, Styled):
    """
    Renders a block of text.

    ```py
    hd.text("Hello World")
    ```

    ### Can be styled

    ```py
    hd.text(
        "Hello World",
        border="1px solid green-200",
        background_color="green-50",
        padding=1,
        border_radius="large",
        width="fit-content",
    )
    ```

    """

    _tag = "p"

    content = Prop(String, "")

    def __init__(self, *content, **kwargs):
        """
        The chunks passed in `*content` will be joined by `" "` and used
        to initialize the `content` prop.

        ```py
        x = 2
        hd.text("I have", x, "chickens.")
        # is equivalent to
        hd.text(content=f"I have {x} chickens.")
        ```

        """
        if content:
            kwargs["content"] = concat_text(content)
        super().__init__(**kwargs)


class h1(text):
    """
    A component that works identically to @component(text) but renders
    an HTML `<h1>` tag, the largest possible heading.

    This is roughly equivalent to using one hash-mark in Markdown:
    `hd.markdown("# Heading")`.

    """

    _name = "text"
    _tag = "h1"


class h2(text):
    """
    A component that works identically to @component(text) but renders
    an HTML `<h2>` tag, one step smaller than @component(h1).

    This is roughly equivalent to using two hash-marks in Markdown:
    `hd.markdown("## Heading")`.
    """

    _name = "text"
    _tag = "h2"


class h3(text):
    """
    A component that works identically to @component(text) but renders
    an HTML `<h3>` tag, one step smaller than @component(h2).

    This is roughly equivalent to using three hash-marks in Markdown:
    `hd.markdown("### Heading")`.
    """

    _name = "text"
    _tag = "h3"


class h4(text):
    """
    A component that works identically to @component(text) but renders
    an HTML `<h4>` tag, one step smaller than @component(h3).

    This is roughly equivalent to using four hash-marks in Markdown:
    `hd.markdown("#### Heading")`.
    """

    _name = "text"
    _tag = "h4"


class h5(text):
    """
    A component that works identically to @component(text) but renders
    an HTML `<h5>` tag, one step smaller than @component(h4).

    This is roughly equivalent to using five hash-marks in Markdown:
    `hd.markdown("##### Heading")`.
    """

    _name = "text"
    _tag = "h5"
