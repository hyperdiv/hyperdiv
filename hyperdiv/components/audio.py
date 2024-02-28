from ..component_base import Component
from ..component_mixins.styled import Styled
from ..prop import Prop
from ..prop_types import Bool, PureString, ClampedFloat


class media_source(Component):
    """
    A media source.
    """

    _tag = "source"

    # A local or remote path to an audio file.
    src = Prop(PureString, "")


class audio(Component, Styled):
    """A simple component for playing audio files in the browser. The
    look & feel of the component is currently browser-dependent.

    ```py
    src = "https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3"

    audio = hd.audio(src, volume=0.3)
    ```

    You can hide the built-in controls and control playback
    programmatically.

    ```py
    src = "https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3"

    audio = hd.audio(src, volume=0.3, controls=False)

    if audio.playing:
        if hd.button(
            "Stop",
            prefix_icon="pause",
            font_color="red"
        ).clicked:
            audio.pause()
    else:
        if hd.button(
            "Play",
            prefix_icon="play-fill",
            font_color="blue"
        ).clicked:
            audio.play()
    ```

    ## Custom Sources

    To provide multiple file formats and let the browser choose which
    one to play, use @component(media_source):

    ```py-nodemo
    with hd.audio() as audio:
        hd.media_source("/assets/my-file.ogg")
        hd.media_source("/assets/my-file.mp3")
    ```
    """

    _tag = "audio"

    # Whether to show the built-in browser controls.
    controls = Prop(Bool, True)
    # Whether the volume is muted.
    muted = Prop(Bool, False)
    # The percent level of the volume control.
    volume = Prop(ClampedFloat(0, 1), 1)
    # Whether the audio should play repeatedly.
    loop = Prop(Bool, False)
    # Whether the audio is currently playing.
    playing = Prop(Bool, False)

    def __init__(self, src=None, **kwargs):
        """
        `src` is a local or remote path to an audio file.

        If `src` is provided, an @component(media_source) will
        automatically be created.
        """
        super().__init__(**kwargs)
        if src:
            with self:
                media_source(src=src)

    def play(self):
        """Start playback."""
        self.playing = True

    def pause(self):
        """Pause playback."""
        self.playing = False
