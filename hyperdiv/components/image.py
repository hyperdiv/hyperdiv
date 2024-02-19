import base64
from ..prop_types import PureString, HyperdivType
from ..prop import Prop
from ..component_base import Component
from ..component_mixins.interactive import Interactive
from ..component_mixins.styled import Styled


class ImageSrcDef(HyperdivType):
    """
    The type of an @component(image) `src` prop.

    It accepts the following value shapes:

    (a) A string that is either a (local or remote) path to an
    image. This is the most common case. For example
    `"/assets/my-image.jpg"` or `"https://url.com/path/to/image.png"`.

    (b) A string that contains browser-ready base64-encoded image
    bytes. The string must take this shape, otherwise the browser will
    not be able to render it:

    ```sh
    "data:{mime_type};base64,{the_actual_base64_string}"
    ```

    The `{mime_type}` can generally be left blank, and browsers will
    auto-infer it. See here for a list of mime types:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types

    (c) Raw image bytes. The bytes will automatically be converted to a
    browser-ready base64 string. The image mime type will be left
    blank, letting the browser infer it.

    (d) A tuple `(image_bytes, mime_type)`. Same as (c), but allows
    explicitly adding a mime type. The mime type will be passed on to
    the browser verbatim.

    Note that if you explicitly set a mime type, browsers will
    likely ignore it if it doesn't match what the browser inferred
    from the bytes. In general it's safe to not worry about mime types.
    """

    def parse(self, value):
        if isinstance(value, bytes):
            # Base64 encode the bytes
            encoded_image_data = base64.b64encode(value).decode("utf-8")
            value = f"data:;base64,{encoded_image_data}"
        elif isinstance(value, tuple):
            image_bytes, mime_type = value
            if not isinstance(image_bytes, bytes) or not isinstance(mime_type, str):
                raise ValueError("Bad image src format.")
            encoded_image_data = base64.b64encode(image_bytes).decode("utf-8")
            value = f"data:{mime_type};base64,{encoded_image_data}"
        else:
            value = PureString.parse(value)
        return value


ImageSrc = ImageSrcDef()


class image(Component, Styled, Interactive):
    """
    An image component.

    ```py
    hd.image("/assets/kitten.jpg")
    ```

    When the image source is a path, it can either refer to a local
    `/assets` path or a remote URL.

    In addition to paths, the `src` prop can also be base64-encoded
    image bytes. If you pass raw image bytes into the `image`
    constructor, they will automatically be converted to base64.
    """

    _tag = "img"

    # The source path or URL of the image.
    src = Prop(ImageSrc, "")

    def __init__(self, src, **kwargs):
        super().__init__(src=src, **kwargs)
