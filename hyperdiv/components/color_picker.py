from ..prop_types import Bool, String, CSSField, Size, OneOf, BoolEvent
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.slottable import Slottable
from ..style_part import BasePart, StylePart
from .common.shoelace_types import ShoelaceSize


class color_picker(Component, Slottable):
    """
    A component that allows picking a color value graphically. By
    default it works like dropdown, rendering a color indicator that
    when clicked, opens the picker. When you pass `inline=True`, the
    picker will render inline.

    ```py
    with hd.box(gap=1):
        picker = hd.color_picker(value="#000000")
        hd.text(picker.value)
    ```

    ### Rendered inline

    ```py
    with hd.box(gap=1):
        picker = hd.color_picker(
            inline=True,
            value="#000000",
        )
        hd.text(picker.value)
    ```

    ### Swatches

    You can use the `swatches` prop to add a `;`-delimited list of
    preset colors that will be rendered at the bottom of the picker.

    ```py
    with hd.box(gap=1):
        picker = hd.color_picker(
            inline=True,
            value="#000000",
            swatches="#ffaabb;#ccdd00;#bb00ff"
        )
        hd.text(picker.value)
    ```

    """

    _tag = "sl-color-picker"
    _has_direct_children = False

    # The picked color, in the format determined by the `color_format` prop.
    value = Prop(String, "")
    # An invisible descriptive label that is helpful for accessibility.
    assistive_label = Prop(String, "", ui_name="label")
    # The format of the `value` prop.
    color_format = Prop(OneOf("hex", "rgb", "hsl", "hsv"), "hex", ui_name="format")
    # Whether to render the picker inline. By default, it works like a dropdown.
    inline = Prop(Bool, False)
    # The size of the picker. This size affects the "dropdown trigger"
    # when `inline` is `False`. It does not affect the picker component itself.
    size = Prop(ShoelaceSize, "medium")
    # Whether to disable the part of the picker that allows color format toggling.
    no_format_toggle = Prop(Bool, False)
    # The internal name of the picker. This is only relevant when
    # using pickers in @component(form)s.
    name = Prop(String, "")
    # Whether the picker is disabled, preventing user interaction.
    disabled = Prop(Bool, False)
    hoist = Prop(Bool, False)
    # Whether to show a slider for choosing the opacity of the
    # color. The `value` prop values will include opacity values.
    opacity = Prop(Bool, False)
    # Whether to uppercase the color values.
    uppercase = Prop(Bool, False)
    # A `;`-delimited list of color values to show as "swatches" --
    # color presets.
    swatches = Prop(String, "")
    # The width of the color grid.
    grid_width = Prop(CSSField("--grid-width", Size))
    # The height of the color grid.
    grid_height = Prop(CSSField("--grid-height", Size))
    # The diameter of the color choosing handle.
    grid_handle_size = Prop(CSSField("--grid-handle-size", Size))
    # The height of the color slider track below the grid.
    slider_height = Prop(CSSField("--slider-height", Size))
    # The diameter of the slider handle.
    slider_handle_size = Prop(CSSField("--slider-handle-size", Size))
    # The size of the swatch squares.
    swatch_size = Prop(CSSField("--swatch-size", Size))

    changed = Prop(BoolEvent, False)

    base_style = Prop(BasePart())
    trigger_style = Prop(StylePart("trigger"))
    swatches_style = Prop(StylePart("swatches"))
    swatch_style = Prop(StylePart("swatch"))
    grid_style = Prop(StylePart("grid"))
    grid_handle_style = Prop(StylePart("grid-handle"))
    slider_style = Prop(StylePart("slider"))
    slider_handle_style = Prop(StylePart("slider-handle"))
    hue_slider_style = Prop(StylePart("hue-slider"))
    hue_slider_handle_style = Prop(StylePart("hue-slider-handle"))
    opacity_slider_style = Prop(StylePart("opacity-slider"))
    opacity_slider_handle_style = Prop(StylePart("opacity-slider-handle"))
    preview_style = Prop(StylePart("preview"))
    input_style = Prop(StylePart("input"))
    eye_dropper_button_style = Prop(StylePart("eye-dropper-button"))
    eye_dropper_button_base_style = Prop(StylePart("eye-dropper-button__base"))
    eye_dropper_button_prefix_style = Prop(StylePart("eye-dropper-button__prefix"))
    eye_dropper_button_label_style = Prop(StylePart("eye-dropper-button__label"))
    eye_dropper_button_suffix_style = Prop(StylePart("eye-dropper-button__suffix"))
    eye_dropper_button_caret_style = Prop(StylePart("eye-dropper-button__caret"))
    format_button_style = Prop(StylePart("format-button"))
    format_button_base_style = Prop(StylePart("format-button__base"))
    format_button_prefix_style = Prop(StylePart("format-button__prefix"))
    format_button_label_style = Prop(StylePart("format-button__label"))
    format_button_suffix_style = Prop(StylePart("format-button__suffix"))
    format_button_caret_style = Prop(StylePart("format-button__caret"))

    def __init__(self, *, swatches="", **kwargs):
        if isinstance(swatches, (list, tuple)):
            swatches = ";".join(swatches)

        super().__init__(swatches=swatches, **kwargs)

    def reset(self):
        self.reset_prop("value")
