from ..prop_types import String, Bool, Optional, Int, OneOf, BoolEvent
from ..prop import Prop
from ..component_base import Component
from ..component_mixins import Boxy, Styled
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


class file_input_element(Component):
    _tag = "input"
    _type = Prop(String, "file", ui_name="type")


class file_input(Component, Styled, Boxy):
    _tag = "label"
    _name = "file_input"
    _classes = ["file-upload"]

    def __init__(
        self,
        *content,
        padding="large",
        gap="large",
        font_color="neutral-700",
        font_size="small",
        direction="horizontal",
        align="center",
        cursor="pointer",
        background_color="neutral-50",
        border="1px solid neutral-200",
        border_radius="medium",
        **kwargs,
    ):
        super().__init__(
            padding=padding,
            gap=gap,
            font_color=font_color,
            font_size=font_size,
            direction=direction,
            align=align,
            cursor=cursor,
            background_color=background_color,
            border=border,
            border_radius=border_radius,
            **kwargs,
        )

        with self:
            file_input_element()
            icon("cloud-upload", font_size="large", font_color="primary")
            text("Click to upload files.")
