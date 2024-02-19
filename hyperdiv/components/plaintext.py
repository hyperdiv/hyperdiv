from ..component_base import Component
from ..prop import Prop
from ..prop_types import String
from .common.text_utils import concat_text


class plaintext(Component):
    """
    A component that renders a block of plain text. Unlike
    @component(text), which wraps the text in a `<p>` tag, `plaintext`
    generates a raw block of text that isn't wrapped in an HTML
    tag. As such, it cannot be styled or slotted.

    ```py
    hd.plaintext("Hello")
    ```
    """

    # The text content.
    content = Prop(String, "")

    def __init__(self, *content, **kwargs):
        if content:
            kwargs["content"] = concat_text(content)
        super().__init__(**kwargs)
