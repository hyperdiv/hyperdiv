from ..prop_types import CSSField, ClampedFloat, Bool, String, Color, Size
from ..prop import Prop
from .common.label_component import LabelComponent
from ..style_part import BasePart, StylePart
from .common.text_utils import concat_text
from .common.shoelace_types import ProgressTrackColor, ProgressIndicatorColor
from .plaintext import plaintext


class progress_bar(LabelComponent):
    """
    Renders a progress bar that can be either indeterminate, or have a
    concrete percentage value.

    ### Indeterminate

    ```py
    hd.progress_bar(indeterminate=True)
    ```

    ### Concrete value

    ```py
    hd.progress_bar(value=40)
    ```

    ### Custom progress bar

    ```py
    hd.progress_bar(
        "40%",
        value=40,
        track_color="blue-50",
        indicator_color="green-300",
        label_color="yellow",
        bar_height=4,
        label_style=hd.style(
            font_size=2,
            font_family="mono"
        ),
    )
    ```

    ### Mutating the value

    ```py
    with hd.box(gap=1):
        bar = hd.progress_bar(value=40)
        with hd.hbox(gap=1):
            if hd.button("Increase").clicked:
                if bar.value <= 95:
                    bar.value += 5
            if hd.button("Reset").clicked:
                    bar.value = 40
    ```

    """

    _tag = "sl-progress-bar"

    value = Prop(ClampedFloat(0, 100), 0)
    indeterminate = Prop(Bool, False)
    assistive_label = Prop(String, "", ui_name="label")
    bar_height = Prop(CSSField("--height", Size))
    track_color = Prop(ProgressTrackColor)
    indicator_color = Prop(ProgressIndicatorColor)
    label_color = Prop(CSSField("--label-color", Color))

    base_style = Prop(BasePart())
    indicator_style = Prop(StylePart("indicator"))
    label_style = Prop(StylePart("label"))
