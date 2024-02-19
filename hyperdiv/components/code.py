from textwrap import dedent
from .markdown import markdown


def code(code_block, language="python", **kwargs):
    """
    Calls @component(markdown) to render the given code block.
    `**kwargs` are passed down to @component(markdown).

    `language` can be the short name of any lexer supported by
    [Pygments](https://pygments.org/docs/lexers/).

    ```py
    hd.code(
        '''
        def f(x, y):
            return x + y
        '''
    )
    ```
    ```py
    hd.code(
        '''
        async function hello() {
            const a = await f("foo");
            const b = await g("bar");
            return a + b;
        }
        ''',
        language="javascript"
    )
    ```
    """
    markdown(f"```{language}\n{dedent(code_block)}\n```", **kwargs)
