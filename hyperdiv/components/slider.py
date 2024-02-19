from ..prop_types import String, CSSField, Bool, Size, Float, OneOf, Color, BoolEvent
from ..prop import Prop
from ..slot import Slot
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text
from .text import text


class slider(LabelComponent):
    """
    A slider (range) input component allowing users to choose a value
    from interval by sliding a knob.

    ```py
    with hd.box(gap=1):
        slider = hd.slider()
        hd.text(slider.value)
    ```

    ### Custom range

    ```py
    with hd.box(gap=1):
        slider = hd.slider(min_value=30, max_value=50)
        hd.text(slider.value)
    ```

    ### Default value with custom step

    ```py
    with hd.box(gap=1):
        slider = hd.slider(
            min_value=30,
            max_value=50,
            step=5,
            value=35,
        )
        hd.text(slider.value)
    ```

    ### Customizable

    ```py
    with hd.box(gap=1):
        slider = hd.slider(
            value=40,
            track_active_color="primary",
            track_height=1,
            thumb_size=2,
        )
        hd.text(slider.value)
    ```

    """

    _tag = "sl-range"

    # The name of the component. If `name` is not provided, it is set
    # to the slider's label.
    name = Prop(String, "")
    # The value of the slider.
    value = Prop(Float, 0)
    # Small hint text rendered below the slider.
    help_text = Prop(String, "")
    # Whether the slider can be interacted with.
    disabled = Prop(Bool, False)
    # The minimum value of the slider.
    min_value = Prop(Float, 0, ui_name="min")
    # The maximum value of the slider.
    max_value = Prop(Float, 100, ui_name="max")
    # The step/increment of the slider.
    step = Prop(Float, 1)
    # Where to position the knob/thumb tooltip.
    tooltip = Prop(OneOf("top", "bottom", "none"), "top")
    # The size of the draggable thumb.
    thumb_size = Prop(CSSField("--thumb-size", Size))
    # The offset of the tooltip.
    tooltip_offset = Prop(CSSField("--tooltip-offset", Size))
    # The color of the track to the left of the thumb.
    track_active_color = Prop(CSSField("--track-color-active", Color))
    # The color of the track to the right of the thumb.
    track_inactive_color = Prop(CSSField("--track-color-inactive", Color))
    # The height of the track.
    track_height = Prop(CSSField("--track-height", Size))
    # The point around which the "active" track color activates.
    track_active_offset = Prop(CSSField("--track-active-offset", Size))

    changed = Prop(BoolEvent, False)

    label_slot = Slot(ui_name="label")

    base_style = Prop(BasePart("form-control"))
    label_style = Prop(StylePart("form-control-label"))
    slider_style = Prop(StylePart("form-control-input"))
    input_wrapper_style = Prop(StylePart("base"))
    input_style = Prop(StylePart("input"))
    tooltip_style = Prop(StylePart("tooltip"))
    help_text_style = Prop(StylePart("form-control-help-text"))

    def __init__(
        self,
        *label,
        name=None,
        min_value=0,
        max_value=100,
        value=None,
        **kwargs,
    ):
        if name is None:
            name = concat_text(label)

        if min_value >= max_value:
            raise ValueError("min_value should be less than max_value")

        if value is not None:
            if value < min_value or value > max_value:
                raise ValueError("value should be between min_value and max_value")
        else:
            value = min_value

        super().__init__(
            *label,
            name=name,
            min_value=min_value,
            max_value=max_value,
            value=value,
            **kwargs,
        )

    def _get_label_slot(self):
        return self.label_slot

    def reset(self):
        self.reset_prop("value")
