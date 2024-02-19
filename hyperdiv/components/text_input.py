from ..prop_types import String, Bool, Optional, Int, OneOf, BoolEvent
from ..prop import Prop
from ..slot import Slot
from .common.shoelace_types import (
    ShoelaceSize,
    InputAutoCapitalize,
    InputAutoCorrect,
    InputEnterKeyHint,
    InputMode,
)
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text
from .icon import icon
from .text import text


class text_input(LabelComponent):
    """
    The Hyperdiv text input component.

    ```py
    ti = hd.text_input(placeholder="Enter some text")
    hd.text("You entered:", ti.value)
    ```

    ## Input Types

    `text_input` supports multiple types of inputs, including
    passwords, numbers, dates, and times.

    ```py
    hd.text_input(
        "Enter a number:",
        input_type="number"
    )
    hd.text_input(
        "Enter a password:",
        input_type="password",
        password_toggle=True,
    )
    hd.text_input(
        "Enter a date:",
        input_type="date"
    )
    hd.text_input(
        "Enter a date and time:",
        input_type="datetime-local"
    )
    hd.text_input(
        "Enter a time:",
        input_type="time"
    )
    ```

    Some of the props of `text_input` are only relevant for certain
    input types. For example the `password_toggle` prop, shown above,
    will only affect the `password` input type.

    ## Slots

    `text_input` supports slots for adding prefix and suffix icons to
    the input.

    ```py
    hd.text_input(
        prefix_icon="gear",
        suffix_icon="chevron-right"
    )
    ```

    The password show/hide icons can also be customized:

    ```py
    hd.text_input(
        value="mypassword",
        input_type="password",
        password_toggle=True,
        show_password_icon="sunglasses",
        hide_password_icon="eyeglasses",
    )
    ```
    """

    _tag = "sl-input"
    _has_direct_children = False

    # The type of the input.
    #
    # * `text`: The default type.
    # * `time`: Renders a time picker in the input.
    # * `date`: Renders a date picker in the input.
    # * `datetime-local`: Renders a date and time picker.
    # * `number`: Restricts the input to a number, and shows a number
    #   keyboard on mobile.`text_input` exposes additional options
    #   specific to this input type.
    # * `password`: Renders a password input, with the input value
    #   obscured by default. `text_input` exposes additional options
    #   specific to this input type.
    # * `tel`: Functionally identical to `text` but may render a
    #   keyboard specific for inputting phone numbers while on mobile.
    # * `search`: Functionally identical to `text` but may be styled
    #   specifically by the browser.
    input_type = Prop(
        OneOf(
            "date",
            "datetime-local",
            # "email",
            "number",
            "password",
            "search",
            "tel",
            "text",
            "time",
            # "url",
        ),
        "text",
        ui_name="type",
    )
    # The name of the text input. If left unspecified, it is set to
    # the label.
    name = Prop(String, "")
    # The value/contents of the text input.
    value = Prop(String, "")
    # The size of the text input.
    size = Prop(ShoelaceSize, "medium")
    # Whether the text input should be rendered with a filled style.
    filled = Prop(Bool, False)
    # Whether the text input should be rendered as a pill.
    pill = Prop(Bool, False)
    # Help text/hint to be rendered under the input.
    help_text = Prop(String, "")
    # Whether a "x" button should be rendered that clears the input
    # when clicked.
    clearable = Prop(Bool, False)
    # Whether the text input should be rendered as disabled.
    disabled = Prop(Bool, False)
    # A placeholder to show when the input is empty. This prop will
    # not render anything for date and time inputs, which are
    # pre-populated with a date/time picker.
    placeholder = Prop(String, "")
    # Whether the input is readonly.
    readonly = Prop(Bool, False)
    # If the input type is `"password"`, whether to render a button
    # that allows revealing the password.
    password_toggle = Prop(Bool, False)
    # Whether the password is visible.
    password_visible = Prop(Bool, False)
    # When the input type is `number`, this option hides the
    # increment/decrement buttons.
    no_spin_buttons = Prop(Bool, False)
    # The minimum length of the input, in number of characters.
    minlength = Prop(Optional(Int))
    # The maximum length of the input, in number of characters.
    maxlength = Prop(Optional(Int))
    # If the input type is `"number"` this sets the minimum value that
    # can be typed in.
    min_value = Prop(Optional(Int), ui_name="min")
    # If the input type is `"number"`, this sets the maximum value that
    # can be typed in.
    max_value = Prop(Optional(Int), ui_name="max")
    # If the input type is `"number"`, this determines the
    # step/increment that the value increments/decrements by when
    # clicking the up/down buttons.
    step = Prop(Optional(Int))
    # Determines how input text will be auto-capitalized.
    autocapitalize = Prop(InputAutoCapitalize)
    # Determines how input text will be auto-corrected.
    autocorrect = Prop(InputAutoCorrect)
    autocomplete = Prop(Optional(String))
    # Whether this text input should be auto-focused.
    autofocus = Prop(Optional(Bool))
    # Determines the behavior of the Enter key.
    enterkeyhint = Prop(InputEnterKeyHint)
    # Whether spell-check is turned on.
    spellcheck = Prop(Bool, False)
    # Determines the virtual keyboard shown on mobile.
    inputmode = Prop(InputMode)
    # A regex pattern that restricts what can be typed in this input.
    pattern = Prop(Optional(String))
    # Whether the input value changed in this run.
    changed = Prop(BoolEvent, False)

    label_slot = Slot(ui_name="label")
    prefix = Slot()
    suffix = Slot()
    clear = Slot(ui_name="clear-icon")
    show_password = Slot(ui_name="show-password-icon")
    hide_password = Slot(ui_name="hide-password-icon")

    base_style = Prop(BasePart("form-control"))
    label_style = Prop(StylePart("form-control-label"))
    help_text_style = Prop(StylePart("form-control-help-text"))
    input_wrapper_style = Prop(StylePart("form-control-input"))
    input_base_style = Prop(StylePart("base"))
    input_style = Prop(StylePart("input"))
    prefix_style = Prop(StylePart("prefix"))
    clear_button_style = Prop(StylePart("clear-button"))
    password_toggle_button_style = Prop(StylePart("password-toggle-button"))
    suffix_style = Prop(StylePart("suffix"))

    def __init__(
        self,
        *label,
        name=None,
        prefix_icon=None,
        suffix_icon=None,
        clear_icon=None,
        show_password_icon=None,
        hide_password_icon=None,
        **kwargs,
    ):
        """
        The `*label` argument sets the text input's label.

        The kwargs suffixed by `_icon` each take an icon name and slot
        that icon into the respective slot.
        """
        if name is None:
            name = concat_text(label)

        super().__init__(*label, name=name, **kwargs)

        with self:
            if prefix_icon:
                icon(prefix_icon, slot=self.prefix)
            if suffix_icon:
                icon(suffix_icon, slot=self.suffix)
            if clear_icon:
                icon(clear_icon, slot=self.clear)
            if show_password_icon:
                icon(show_password_icon, slot=self.show_password)
            if hide_password_icon:
                icon(hide_password_icon, slot=self.hide_password)

    def reset(self):
        self.reset_prop("value")

    def _get_label_slot(self):
        return self.label_slot
