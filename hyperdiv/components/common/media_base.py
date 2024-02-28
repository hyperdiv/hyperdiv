from ...component_base import Component
from ...component_mixins.styled import Styled
from ...prop import Prop
from ...prop_types import Bool, ClampedFloat
from ..media_source import media_source


class MediaBase(Component, Styled):
    """
    A base class providing common props and playback methods for
    @component(audio) and @component(video).
    """

    # Whether to show the built-in browser media player.
    controls = Prop(Bool, True)
    # Whether the volume is muted.
    muted = Prop(Bool, False)
    # The percent level of the volume control.
    volume = Prop(ClampedFloat(0, 1), 1)
    # Whether the media should play repeatedly.
    loop = Prop(Bool, False)
    # Whether the media is currently playing.
    playing = Prop(Bool, False)

    def play(self):
        """Start playback."""
        self.playing = True

    def pause(self):
        """Pause playback."""
        self.playing = False

    def __init__(self, src=None, **kwargs):
        """
        `src` is a local or remote path to an audio file.

        If `src` is provided, a @component(media_source) will
        automatically be created.
        """
        super().__init__(**kwargs)
        if src:
            with self:
                media_source(src=src)
