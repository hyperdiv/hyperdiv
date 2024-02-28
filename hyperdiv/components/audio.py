from .common.media_base import MediaBase


class audio(MediaBase):
    """
    A simple component for playing audio files in the browser. The
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
            "Pause",
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
