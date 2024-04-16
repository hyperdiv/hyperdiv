import mimetypes
import os
from textwrap import dedent, indent
import xxhash
from jinja2 import Template
from .frontend import get_frontend_public_path


def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def attributes_from_dict(d):
    attributes = []
    for k, v in d.items():
        if isinstance(v, bool):
            if v:
                attributes.append(k)
        else:
            attributes.append(f'{k}="{v}"')
    return " ".join(attributes)


def js_tag_from_dict(d):
    return f"<script {attributes_from_dict(d)}></script>"


def js_tag_from_url(u):
    return js_tag_from_dict(dict(src=u))


def css_tag_from_dict(d):
    return f"<link {attributes_from_dict(d)} />"


def css_tag_from_url(u):
    return css_tag_from_dict(dict(rel="stylesheet", href=u))


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
    css_assets=(),
    js_assets=(),
    raw_head_content="",
):
    """
    This function generates the app's HTML index page that is served
    to the browser when users load the app's URL. It generates SEO meta
    tags as well as Twitter (`twitter:`) and Meta OpenGraph (`og:`)
    tags, so Twitter/Meta will generate nice-looking preview cards
    when the app is shared on these platforms.

    Custom Javascript and CSS assets can also be added to the index
    page. More on this below.

    Passing `title`, `description`, `url`, `favicon`, and `image`,
    should be enough to generate a useful set of meta tags.

    This function's only use is to pass its return value into the
    `index_page` parameter of Hyperdiv's @component(run) function.

    ## Parameters

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

    * `css_assets`: Custom CSS assets to load into the index page.

    * `js_assets`: Custom Javascript assets to load into the index page.

    * `raw_head_content`: A string of arbitrary content to add to the
      `<head>` tag of the generated index page.

    ## Loading Custom Assets

    The `css_assets`, `js_assets`, and `raw_head_content` parameters
    can be used to load custom local or remote assets into the index
    page.

    ```py-nodemo
    hd.run(main, index_page=hd.index_page(
        js_assets=[
            # A local Javascript asset:
            "/assets/my-script.js",
            # A remote Javascript asset:
            "https://foo.com/remote-script.js"
        ],
        css_assets=[
            # A local CSS asset
            "/assets/my-styles.css",
            "https//foo.com/remote-styles.css",
        ]
    ))
    ```

    Hyperdiv will generate basic `<script>` and `<link>` tags to load
    these scripts.

    ### Custom Attributes

    Instead of a string, you can pass a dictionary mapping attributes
    to values. This can be useful when you want to add extra
    attributes that Hyperdiv does not add by default:

    ```py-nodemo
    hd.run(main, index_page=hd.index_page(
        js_assets=[dict(
            defer=True
            src="https://foo.com/remote-script.js?x=1",
        )]
    ))
    ```

    The code above will generate the tag `<script defer src="https://foo.com/remote-script.js?x=1"></script>`.

    When you use a dictionary, Hyperdiv will not set any attributes
    implicitly. For example to properly load a CSS asset, you should
    set the `rel` attribute:

    ```py-nodemo
    hd.run(main, index_page=hd.index_page(
        js_assets=[dict(
            rel="stylesheet",
            href="/assets/custom-styles.css",
        )]
    ))
    ```

    ### Raw Head Content

    If the options above don't fit your use case, you can use the
    `raw_head_content` argument to cause Hyperdiv to insert a
    string into the page's `<head>` tag:

    ```py-nodemo
    hd.run(main, index_page=hd.index_page(
        raw_head_content=(
            '''
            <link rel="stylesheet" href="/assets/my-styles.css" />
            <script defer src="https://foo.com/remote-script.js"></script>
            <script>
              console.log("Hello world!")
            </script>
            '''
        )
    ))
    ```

    Note that Hyperdiv will re-indent this string to try to match the
    indentation of the index page.

    Hyperdiv inserts custom head content in this order:

    1. The tags generated by `css_assets`, in the order they are
       specified, if any.
    2. Followed by the tags generated by `js_assets`, in the order
       they are specified, if any.
    3. Followed The content specified by `raw_head_content`.

    """

    head_tags = []

    for css_tag in css_assets:
        if isinstance(css_tag, dict):
            head_tags.append(css_tag_from_dict(css_tag))
        else:
            head_tags.append(css_tag_from_url(css_tag))

    for js_tag in js_assets:
        if isinstance(js_tag, dict):
            head_tags.append(js_tag_from_dict(js_tag))
        else:
            head_tags.append(js_tag_from_url(js_tag))

    if head_tags:
        raw_head_content = "\n".join(head_tags + [dedent(raw_head_content).strip()])

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
        raw_head_content=raw_head_content,
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
    raw_head_content="",
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

    # Indent by 12 spaces to match the indent where the
    # raw_head_content is inserted in the suffix string below:
    if raw_head_content:
        raw_head_content = indent(raw_head_content, " " * 12).strip()

    suffix = f"""
            <style id="hyperdiv-styles">{{{{style}}}}</style>
            <link rel="stylesheet" href="/build/bundle.css?v={css_hash}" />
            <script defer src="/build/bundle.js?v={js_hash}"></script>
            {raw_head_content}
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
