from ..prop_types import String, BoolEvent, Bool
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.styled import Styled
from ..style_part import BasePart, StylePart
from .common.text_utils import concat_text
from .radio import radio
from .radio_button import radio_button
from .scope import scope


class radio_group(Component, Styled):
    """
    An exclusive choice component, allowing the user to select one
    from multiple choices. @component(radio)s and
    @component(radio_button)s can be nested within a `radio_group`.

    ### Radios

    ```py
    with hd.box(gap=1):
        with hd.radio_group(value="One") as group:
            hd.radio("One")
            hd.radio("Two")
            hd.radio("Three")

        hd.text("Selected:", group.value)
    ```

    ### Radio buttons

    ```py
    with hd.box(gap=1):
        with hd.radio_group(value="One") as group:
            hd.radio_button("One")
            hd.radio_button("Two")
            hd.radio_button("Three")

        hd.text("Selected:", group.value)
    ```

    Using the `pill` option to make a rounded radio button group:

    ```py
    with hd.box(gap=1):
        with hd.radio_group(value="One") as group:
            hd.radio_button("One", pill=True)
            hd.radio_button("Two")
            hd.radio_button("Three", pill=True)

        hd.text("Selected:", group.value)
    ```

    ### Shorthand syntax

    Radio groups can be quickly created in one shot by passing the `options` kwarg.

    ```py
    hd.radio_group(
        options=("One", "Two", "Three"),
        value="One"
    )
    ```

    Similarly, by passing `button_options` to create button groups:

    ```py
    hd.radio_group(
        button_options=("One", "Two", "Three"),
        value="One"
    )
    ```

    In addition, the helper functions `radios` and `radio_buttons` are provided:

    ```py
    with hd.box(gap=1):
        hd.radios(
            "One", "Two", "Three",
            value="One"
        )
        hd.radio_buttons(
            "One", "Two", "Three",
            value="One"
        )
    ```
    """

    _tag = "sl-radio-group"

    # The visible label of the group.
    label = Prop(String, "")
    # The name of the group. By default, if `name` is not provided, it
    # is set to the label of the group.
    name = Prop(String, "")
    # The value of the nested @component(radio) or
    # @component(radio_button) that is currently selected.
    value = Prop(String, "")
    # A small text hint further describing the radio group.
    help_text = Prop(String, "")
    # Whether the value of the radio group changed.
    changed = Prop(BoolEvent, False)
    # If this prop is True, the @component(radio) and
    # @component(radio_button) children of this radio group will be
    # disabled.
    disabled = Prop(Bool, False)

    base_style = Prop(BasePart("form-control"))
    label_style = Prop(StylePart("form-control-label"))
    input_wrapper_style = Prop(StylePart("form-control-input"))
    help_text_style = Prop(StylePart("form-control-help-text"))
    button_group_wrapper_style = Prop(StylePart("button-group"))
    button_group_style = Prop(StylePart("button-group__base"))

    def __init__(
        self,
        *label_args,
        options=None,
        button_options=None,
        name=None,
        label="",
        **kwargs,
    ):
        label = label or concat_text(label_args)
        if name is None:
            name = label

        super().__init__(label=label, name=name, **kwargs)

        if options is not None:
            with self:
                for o in options:
                    with scope(o):
                        radio(o)

        if button_options is not None:
            with self:
                for o in button_options:
                    with scope(o):
                        radio_button(o)

    def _collect_child(self, child):
        if isinstance(child, (radio, radio_button)):
            child.disabled = self.disabled
        super()._collect_child(child)

    def reset(self):
        self.reset_prop("value")


def radios(*options, label=None, **kwargs):
    """
    Creates a @component(radio_group) with the given label, with
    nested @component(radio)s, one @component(radio) per item in
    `options`.
    """
    return radio_group(label=label, options=options, **kwargs)


def radio_buttons(*options, label=None, **kwargs):
    """
    Creates a @component(radio_group) with the given label, with
    nested @component(radio_button)s, one @component(radio_button)
    per item in `options`.
    """
    return radio_group(label=label, button_options=options, **kwargs)
