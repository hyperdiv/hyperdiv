from .common.media_base import MediaBase
from ..prop import Prop
from ..prop_types import ClampedInt, Optional


class video(MediaBase):
    """
    A simple component for playing video files in the browser. The
    look & feel of the component is currently browser-dependent.

    ```py
    src = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"

    video = hd.video(src, volume=0.3)
    ```

    You can hide the built-in controls and control playback
    programmatically.

    ```py
    src = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"

    video = hd.video(src, volume=0.3, controls=False)

    if video.playing:
        if hd.button(
            "Pause",
            prefix_icon="pause",
            font_color="red"
        ).clicked:
            video.pause()
    else:
        if hd.button(
            "Play",
            prefix_icon="play-fill",
            font_color="blue"
        ).clicked:
            video.play()
    ```

    ## Custom Sources

    To provide multiple file formats and let the browser choose which
    one to play, use @component(media_source):

    ```py-nodemo
    with hd.video() as video:
        hd.media_source("/assets/my-file.webm")
        hd.media_source("/assets/my-file.mp4")
    ```

    """

    _tag = "video"

    # The width of the video in pixels. If non-`None`, it sets the `width`
    # attribute on the video tag.
    video_width = Prop(Optional(ClampedInt(low=0)), ui_name="width")
    # The height of the video in pixels. If non-`None`, it sets the
    # `height` attribute on the video tag.
    video_height = Prop(Optional(ClampedInt(low=0)), ui_name="height")
