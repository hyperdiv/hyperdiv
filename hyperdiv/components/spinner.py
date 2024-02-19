from ..prop_types import CSSField, Optional, TimeValue
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.slottable import Slottable
from ..style_part import BasePart
from .common.shoelace_types import (
    ProgressTrackColor,
    ProgressIndicatorColor,
    ProgressTrackWidth,
)


class spinner(Component, Slottable):
    """
    An customizable component that can be used to show indeterminate
    progress.

    ```py
    with hd.box(font_size=4):
        hd.spinner(
            speed="5s",
            track_width=0.5
        )
    ```
    """

    _tag = "sl-spinner"

    # The width of the background spinner track.
    track_width = Prop(ProgressTrackWidth)
    # The color of the background spinner track.
    track_color = Prop(ProgressTrackColor)
    # The color of the spinning indicator.
    indicator_color = Prop(ProgressIndicatorColor)
    # The speed of the spinner. A higher time value causes the spinner
    # to spin slower.
    speed = Prop(CSSField("--speed", Optional(TimeValue)))

    base_style = Prop(BasePart())
