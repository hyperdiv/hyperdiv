from ..component_base import Component
from ..component_mixins.styled import Styled
from ..prop import Prop
from ..prop_types import Bool, PureString


class audio_source(Component):
    _tag = "source"

    src = Prop(PureString, "")


class audio(Component, Styled):
    _tag = "audio"

    controls = Prop(Bool, True)
    muted = Prop(Bool, False)
    loop = Prop(Bool, False)
    playing = Prop(Bool, False)

    def __init__(self, src=None, **kwargs):
        super().__init__(**kwargs)
        if src:
            with self:
                audio_source(src=src)

    def source(self, src):
        audio_source(src=src)

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False
