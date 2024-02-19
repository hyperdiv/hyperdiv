from ..prop_types import Optional, Int, BoolEvent
from ..prop import Prop
from ..ui_singleton import BrowserSingleton


class window(BrowserSingleton):
    """
    `window` gives access to the browser's window dimensions, to allow
    rendering responsively based on window size.

    ```py
    window = hd.window()
    if window.width < 1200:
        size = "small"
        color = "red"
    else:
        size = "large"
        color = "green"
    hd.button("Hello", size=size, font_color=color)
    ```

    To do something when the window dimensions change, use the
    `changed` event prop.

    ```py
    window = hd.window()
    state = hd.state(count=0)
    if window.changed:
        state.count += 1
    hd.text("Window resized", state.count, "times.")
    ```

    """

    _key = "window"

    # Whether the browser window was resized.
    changed = Prop(BoolEvent, False)

    def __init__(self):
        super().__init__()

    # The window width in pixels.
    width = Prop(Optional(Int), backend_immutable=True)
    # The window height in pixels.
    height = Prop(Optional(Int), backend_immutable=True)
