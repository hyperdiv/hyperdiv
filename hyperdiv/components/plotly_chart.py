from ..prop_types import OneOf, Bool, HyperdivType, Any
from ..prop import Prop
from ..slot import Slot
from ..component_base import Component
from ..component_mixins.styled import Styled
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text
from .common.shoelace_types import ShoelaceSize
from .plaintext import plaintext
from .icon import icon

import plotly
import plotly.graph_objects as go
import json


class PlotlyFigDef(HyperdivType):
    def parse(self, value):
        if not isinstance(value, go.Figure):
            raise ValueError(
                f"Expected a `plotly.graph_objects.Figure` but got {type(value)}"
            )
        return value

    def render(self, value):
        return json.loads(plotly.io.to_json(value))


PlotlyFig = PlotlyFigDef()


class plotly_chart(Component, Styled):
    _tag = "div"

    fig = Prop(PlotlyFig)
    browser_config = Prop(Any, dict(responsive=True, displayModeBar=False))

    def __init__(self, fig, **kwargs):
        super().__init__(fig=fig, **kwargs)
