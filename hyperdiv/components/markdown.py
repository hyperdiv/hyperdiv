from textwrap import dedent
from functools import cache
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import html
from ..prop_types import HyperdivType
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.boxy import Boxy
from ..component_mixins.styled import Styled
from .common.text_utils import concat_text


def mistune_renderer():
    class HighlightRenderer(mistune.HTMLRenderer):
        def block_code(self, code, info=None):
            if not info:
                info = "text"
            try:
                lexer = get_lexer_by_name(info.strip())
            except Exception:
                lexer = TextLexer()
            formatter = html.HtmlFormatter(cssclass="codehilite", wrapcode=True)
            return highlight(code, lexer, formatter)

    return mistune.create_markdown(
        renderer=HighlightRenderer(escape=False),
        plugins=["strikethrough", "abbr", "table", "url", "task_lists"],
    )


mistune_markdown = mistune_renderer()


@cache
def parse_markdown(value):
    return mistune_markdown(dedent(value)).strip()


class MarkdownDef(HyperdivType):
    """This type accepts markdown text and renders it to HTML."""

    def parse(self, value):
        return parse_markdown(value)

    def __repr__(self):
        return "Markdown"


Markdown = MarkdownDef()


class markdown(Component, Boxy, Styled):
    """
    The `markdown` component accepts content in markdown syntax and
    uses the [Mistune](https://mistune.lepture.com/) Markdown parser
    to render it as HTML in the browser.

    You can use `markdown` to style text:

    ```py
    hd.markdown("# A heading")
    hd.markdown("## A subheading")
    hd.markdown("~~Strikethrough text~~")
    hd.markdown("*Italics text*")
    hd.markdown("**Bold text**")
    ```

    You can also use triple-quote strings to render multi-paragraph
    content:

    ```py
    hd.markdown(
        '''
        # A heading

        A paragraph.

        Another paragraph.

        [A link](https://my-link.com)

        ## A subheading

        An ordered list:
        1. Item one
        2. Item two
        3. Item three

        An unordered list:
        * Item one
        * Item two
        * Item three

        A code block:

        ```js
        const add = (a, b) => a + b;
        ```
        '''
    )
    ```

    Markdown supports box props, so you can adjust the gap between its
    children, alignment, etc., but you cannot control the individual
    styles of its child components.

    To learn Markdown syntax, see:

    * [CommonMark](https://commonmark.org)
    * [CommonMark Tutorial](https://commonmark.org/help)

    """

    _tag = "div"
    _classes = ["markdown"]

    # The markdown content.
    content = Prop(Markdown, "")

    def __init__(self, *content, gap=1.5, **kwargs):
        content_text = None
        if content:
            content_text = concat_text(content)
        super().__init__(gap=gap, content=content_text, **kwargs)
