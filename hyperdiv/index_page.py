import mimetypes
import os
from textwrap import dedent
import xxhash
from jinja2 import Template
from .frontend import get_frontend_public_path


def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def index_page(
    title="Hyperdiv",
    description=None,
    keywords=None,
    url=None,
    image=None,
    twitter_card_type="summary_large_image",
    favicon="/hd-logo-white.svg",
    favicon_16=None,
    favicon_32=None,
    apple_touch_icon=None,
):
    """
    This function generates the app's HTML index page that is served
    to the browser when users load the app's URL. It generates SEO meta
    tags as well as Twitter (`twitter:`) and Meta OpenGraph (`og:`)
    tags, so Twitter/Meta will generate nice-looking preview cards
    when the app is shared on these platforms.

    This function's only use is to pass its return value into the
    `index_page` parameter of Hyperdiv's @component(run) function.

    Passing `title`, `description`, `url`, `favicon`, and `image`,
    should be enough to generate a useful set of meta tags.

    Parameters:

    * `title`: The title of the app.
    * `description`: A short one-line description of the app.

    * `keywords`: An iterable of short keywords describing the app, or
      a comma-separated string of keywords.

    * `url`: The external full URL of the app, for example
      `"https://my-app.foo.com"`.

    * `image`: A full URL to an image that should be included in
      previews when sharing the app on social media. For example
      `"https://my-app.foo.com/my-app-image.png"`.

    * `twitter_card_type`: One of `"summary"` or
      `"summary_large_image"`. The former causes Twitter to render a
      smaller card with the image to the left of the
      title/description, when the app's URL is shared on Twitter. The
      latter causes a larger card to be rendered, where the image is
      prominently displayed above the title/description.

    * `favicon`: A URL pointing to a favicon. Can be a local URL like
      `"/assets/favicon.png"`. The favicon is an icon displayed next
      to the title in browser tab headers.

    * `favicon_16`: A URL pointing to the 16x16px version of the favicon.

    * `favicon_32`: A URL pointing to the 32x32px version of the favicon.

    * `apple_touch_icon`: A URL pointing to the Apple touch icon. This
      is a favicon specifically used by Apple software in certain
      situations. A recommended size is 180x180px. If this isn't
      specified, the favicon will be used.

    """

    template_contents = index_page_template(
        title=title,
        description=description,
        keywords=keywords,
        url=url,
        image=image,
        twitter_card_type=twitter_card_type,
        favicon=favicon,
        favicon_16=favicon_16,
        favicon_32=favicon_32,
        apple_touch_icon=apple_touch_icon,
    )
    template = Template(template_contents)
    return template.render(body="", style="")


def index_page_template(
    title="Hyperdiv",
    description=None,
    keywords=None,
    url=None,
    image=None,
    twitter_card_type="summary_large_image",
    favicon=None,
    favicon_16=None,
    favicon_32=None,
    apple_touch_icon=None,
):
    public_path = get_frontend_public_path()

    css_bundle_path = os.path.join(public_path, "build", "bundle.css")
    css_hash = xxhash.xxh32(str(int(os.path.getmtime(css_bundle_path)))).hexdigest()

    js_bundle_path = os.path.join(public_path, "build", "bundle.js")
    js_hash = xxhash.xxh32(str(int(os.path.getmtime(js_bundle_path)))).hexdigest()

    prefix = """
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width,initial-scale=1" />
        """

    suffix = f"""
            <style id="hyperdiv-styles">{{{{style}}}}</style>
            <link rel="stylesheet" href="/build/bundle.css?v={css_hash}" />
            <script defer src="/build/bundle.js?v={js_hash}"></script>
          </head>
          <body>{{{{body}}}}</body>
        </html>
        """

    lines = ['<meta property="og:type" content="website" />']

    if title:
        lines.append(f"<title>{title}</title>")
        lines.append(f'<meta property="og:title" content="{title}" />')
        lines.append(f'<meta property="og:site_name" content="{title}" />')
        lines.append(f'<meta name="twitter:title" content="{title}" />')
    if keywords:
        if not isinstance(keywords, str):
            try:
                keywords = ", ".join([str(k) for k in keywords])
            except TypeError:
                raise ValueError(
                    "keywords should a string containing keywords separated by ', ' "
                    "or an iterable of keywords"
                )
        lines.append(f'<meta name="keywords" content="{keywords}" />')
    if description:
        lines.append(f'<meta name="description" content="{description}" />')
        lines.append(f'<meta property="og:description" content="{description}" />')
        lines.append(f'<meta name="twitter:description" content="{description}" />')
    if twitter_card_type not in ("summary", "summary_large_image"):
        twitter_card_type = "summary_large_image"
    lines.append(f'<meta name="twitter:card" content="{twitter_card_type}" />')
    if url:
        lines.append(f'<meta property="og:url" content="{url}" />')
    if image:
        lines.append(f'<meta property="og:image" content="{image}" />')
        lines.append(f'<meta name="twitter:image" content="{image}" />')

    if not favicon_16:
        favicon_16 = favicon or favicon_32 or apple_touch_icon
    if not favicon_32:
        favicon_32 = favicon or favicon_16 or apple_touch_icon
    if not apple_touch_icon:
        apple_touch_icon = favicon or favicon_16 or favicon_32

    if favicon_16:
        mime_type = get_mime_type(favicon_16)
        lines.append(
            f'<link rel="icon" type="{mime_type}" sizes="16x16" href="{favicon_16}" />'
        )
    if favicon_32:
        mime_type = get_mime_type(favicon_32)
        lines.append(
            f'<link rel="icon" type="{mime_type}" sizes="32x32" href="{favicon_32}" />'
        )
    if apple_touch_icon:
        mime_type = get_mime_type(apple_touch_icon)
        lines.append(
            f'<link rel="apple-touch-icon" type="{mime_type}" sizes="180x180" href="{apple_touch_icon}" />'
        )

    return dedent(prefix) + "    " + "\n    ".join(sorted(lines)) + dedent(suffix)
