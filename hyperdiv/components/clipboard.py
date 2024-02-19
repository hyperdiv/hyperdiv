from ..prop_types import Optional, String
from ..prop import Prop
from ..ui_singleton import BrowserSingleton


class clipboard(BrowserSingleton):
    """
    This component allows writing data to the user's clipboard.

    ```py
    clipboard = hd.clipboard()
    if hd.button("Copy to clipboard").clicked:
        clipboard.write("Clipboard value")
    ```

    This component only allows you write to the clipboard. You cannot
    inspect the current clipboard value.
    """

    _key = "clipboard"

    _value = Prop(Optional(String), ui_name="value")

    def __init__(self):
        super().__init__()

    def write(self, value):
        """Writes `value` to the user's clipboard."""
        self._value = value
