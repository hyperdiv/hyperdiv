from ..component_base import Component
from ..prop import Prop
from ..prop_types import PureString


class media_source(Component):
    """
    A media source usable with @component(video) and @component(audio).
    """

    _tag = "source"

    # A local or remote path to an audio or video file.
    src = Prop(PureString, "")
