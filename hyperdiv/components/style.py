from ..prop import Prop
from ..prop_types import CSSField, Constant, Optional
from ..component_mixins.styled import Styled
from ..component_mixins.boxy import Boxy
from ..component_base import BaseState

boxy_props = [
    attr_name for attr_name in dir(Boxy) if isinstance(getattr(Boxy, attr_name), Prop)
]

styled_props = [
    attr_name
    for attr_name in dir(Styled)
    if isinstance(getattr(Styled, attr_name), Prop)
]


class style(BaseState, Styled, Boxy):
    """A component holding the props for a style part."""

    _display = Prop(CSSField("display", Optional(Constant("flex"))))

    def __init__(self, **kwargs):
        has_boxy_kwargs = False

        for boxy_prop in boxy_props:
            if boxy_prop in kwargs:
                has_boxy_kwargs = True
                break

        display = None
        direction = None

        if has_boxy_kwargs:
            display = "flex"
            if direction not in kwargs:
                kwargs["direction"] = "vertical"

        super().__init__(_display=display, **kwargs)

    def props_as_dict(self, **default_values):
        output = dict()

        for prop_name in boxy_props + styled_props:
            value = getattr(self, prop_name)
            output[prop_name] = (
                default_values[prop_name]
                if value is None and prop_name in default_values
                else value
            )

        return output
