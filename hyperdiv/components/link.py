from ..prop_types import CSS, Bool, PureString, OneOf
from ..prop import Prop
from ..component_mixins.interactive import Interactive
from .common.text_utils import concat_text
from .plaintext import plaintext
from .box import box


class LinkUnderlineDef(CSS):
    """
    A `Bool` type, accepting the values `True` and `False`,
    determining whether to render an underline on the given
    component's text.
    """

    def parse(self, value):
        return Bool.parse(value)

    def render(self, value):
        return {"text-decoration": "underline" if value else "none"}

    def __repr__(self):
        return "LinkUnderline"


LinkUnderline = LinkUnderlineDef()


class link(box, Interactive):
    """
    A HTML link.

    ```py
    hd.link(
        "Link to a remote website",
        href="https://google.com"
    )
    hd.link(
        "Link to a local path",
        href="/reference/components",
    )
    ```

    `link` inherits from @component(box), so it can be styled like a
    `box` and arbitrary components can be placed inside it.

    For accessibility, the link's body should be kept simple, and you
    should avoid nesting interactive components like buttons inside a
    link.

    ```py
    with hd.link(
        href="https://google.com",
        direction="horizontal",
        padding=1,
        gap=0.5,
        border="1px solid green",
        hover_background_color="green-50",
        border_radius="large",
        width="fit-content",
        align="center"
    ):
        hd.icon("google")
        hd.text("A fancy link")
    ```

    """

    _tag = "a"

    # The path or URL to navigate to when clicking the link.
    href = Prop(PureString)
    # Whether a classic underline should be rendered on the link text.
    underline = Prop(LinkUnderline, False)
    # Determines where the link is opened. See the [W3Schools target
    # documentation](https://www.w3schools.com/tags/att_a_target.asp)
    target = Prop(OneOf(None, "_blank", "_parent", "_self", "_top"), "_blank")
    # See `rel` docs [here](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel).
    rel = Prop(PureString, "noreferrer noopener")

    def __init__(self, *label, cursor="pointer", font_color="blue", **kwargs):
        label = concat_text(label)

        super().__init__(cursor=cursor, font_color=font_color, **kwargs)

        if label:
            with self:
                plaintext(label)
