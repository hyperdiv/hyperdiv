from ..prop import Prop
from ..component_mixins.styled import Styled
from ..component_mixins.boxy import Boxy
from ..component_base import BaseState

boxy_props = [
    attr_name for attr_name in dir(Boxy) if isinstance(getattr(Boxy, attr_name), Prop)
]


class style(BaseState, Styled, Boxy):
    """A component holding the props for a style part."""

    def __init__(self, **kwargs):
        for boxy_prop in boxy_props:
            if kwargs.get(boxy_prop, None) is not None:
                if "direction" not in kwargs:
                    kwargs["direction"] = "vertical"
                break

        super().__init__(**kwargs)

    def props_as_dict(self):
        return {
            prop_name: prop.value
            for prop_name, prop in self._get_stored_props().items()
        }
