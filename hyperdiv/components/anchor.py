from ..component_base import Component


class anchor(Component):
    """Creates an invisible anchor that can be linked to using a location
    hash. When navigating to an anchor link, the page auto-scrolls to
    where the anchor is.

    ```py-nodemo
    # Create an anchor
    hd.anchor("my-anchor")

    # A link to the anchor
    hd.link("Scroll to the anchor", href="#my-anchor")
    ```

    Of course you can link to full URLs that include an anchor hash:

    ```py-nodemo
    hd.link("A Link", href="/path/to/page#my-anchor")
    # or
    hd.link("A Link", href="https://app.hello.com/path/to/page#my-anchor")
    ```
    """

    _tag = "a"

    def __init__(self, name):
        super().__init__(key=name)
