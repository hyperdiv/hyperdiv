from ..prop_types import CSSField, Optional, String, Size, Int, TimeValue
from ..prop import Prop
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.shoelace_types import (
    ProgressTrackColor,
    ProgressIndicatorColor,
    ProgressTrackWidth,
)


class progress_ring(LabelComponent):
    """
    A customizable circular progress component that can be used to
    indicate progress to the user.

    ```py
    with hd.box(gap=0.5):
        progress = hd.progress_ring(value=10)
        with hd.hbox():
            minus = hd.icon_button("dash")
            if minus.clicked:
                progress.value -= 10
            plus = hd.icon_button("plus")
            if plus.clicked:
                progress.value += 10
    ```

    """

    _tag = "sl-progress-ring"

    # The value of the progress ring. 0 indicates an empty ring, and
    # 100 indicates a full ring. Negative values or values over 100
    # will cause the ring to wrap around.
    value = Prop(Int, 0)
    # An invisible label useful for accessibility.
    assistive_label = Prop(String, "", ui_name="label")
    # The width of the background track.
    track_width = Prop(ProgressTrackWidth)
    # The color of the background track.
    track_color = Prop(ProgressTrackColor)
    # The width of the progress indicator.
    indicator_width = Prop(CSSField("--indicator-width", Size))
    # The color of the progress indicator.
    indicator_color = Prop(ProgressIndicatorColor)
    # The diameter of the progress ring.
    size = Prop(CSSField("--size", Size), 4)
    # How long it takes to visually transition from the current value
    # to the new value, when the value changes.
    transition_duration = Prop(
        CSSField("--indicator-transition-duration", Optional(TimeValue))
    )

    base_style = Prop(BasePart())
    label_style = Prop(StylePart("label"))
