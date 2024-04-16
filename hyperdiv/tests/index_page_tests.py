import re
import pytest
from ..index_page import (
    index_page,
    js_tag_from_dict,
    js_tag_from_url,
    css_tag_from_dict,
    css_tag_from_url,
)


def test_index_page():
    page = index_page(
        title="Hyperdiv",
        description="Reactive Web Framework",
        keywords=("web", "framework", "python"),
        url="https://hyperdiv.io",
        image="https://hyperdiv.io/hd-logo-black.png",
        favicon="/hd-loco-black.png",
    )

    assert "<title>Hyperdiv</title>" in page
    assert '<meta name="twitter:title" content="Hyperdiv" />' in page
    assert '<meta property="og:site_name" content="Hyperdiv" />' in page
    assert '<meta property="og:title" content="Hyperdiv" />' in page
    assert '<meta name="description" content="Reactive Web Framework" />' in page
    assert (
        '<meta name="twitter:description" content="Reactive Web Framework" />' in page
    )
    assert '<meta property="og:description" content="Reactive Web Framework" />' in page
    assert '<meta name="keywords" content="web, framework, python" />' in page
    assert (
        '<link rel="apple-touch-icon" type="image/png" sizes="180x180" href="/hd-loco-black.png" />'
        in page
    )
    assert (
        '<link rel="icon" type="image/png" sizes="16x16" href="/hd-loco-black.png" />'
        in page
    )
    assert (
        '<link rel="icon" type="image/png" sizes="32x32" href="/hd-loco-black.png" />'
        in page
    )

    page = index_page(
        title="Hyperdiv",
        description="Reactive Web Framework",
        keywords="web, framework, python",
        url="https://hyperdiv.io",
        image="https://hyperdiv.io/hd-logo-black.png",
        favicon="/hd-loco-black.png",
    )

    assert '<meta name="keywords" content="web, framework, python" />' in page

    with pytest.raises(Exception):
        index_page(keywords=object())

    page = index_page(twitter_card_type="summary")
    assert '<meta name="twitter:card" content="summary" />' in page

    page = index_page(twitter_card_type="invalid")
    assert '<meta name="twitter:card" content="summary_large_image" />' in page


def test_assets_functions():
    assert (
        js_tag_from_url("/assets/script.js")
        == '<script src="/assets/script.js"></script>'
    )

    assert (
        css_tag_from_url("/assets/style.css")
        == '<link rel="stylesheet" href="/assets/style.css" />'
    )

    assert (
        js_tag_from_dict(
            {
                "id": "123",
                "async": True,
                "type": "module",
                "src": "/assets/script.js",
            }
        )
        == '<script id="123" async type="module" src="/assets/script.js"></script>'
    )

    assert (
        css_tag_from_dict(
            {
                "rel": "stylesheet",
                "referrerpolicy": "origin",
                "crossorigin": "use-credentials",
                "href": "/assets/styles.css",
            }
        )
        == '<link rel="stylesheet" referrerpolicy="origin" crossorigin="use-credentials" href="/assets/styles.css" />'
    )


def test_assets_in_index_page():
    page = index_page(
        js_assets=["/assets/script.js", "https://foo.com/script.js?x=123"],
        css_assets=["/assets/styles.css", "https://foo.com/styles.css?x=123"],
    )
    assert '<script src="/assets/script.js"></script>' in page
    assert '<script src="https://foo.com/script.js?x=123"></script>' in page
    assert '<link rel="stylesheet" href="/assets/styles.css" />' in page
    assert '<link rel="stylesheet" href="https://foo.com/styles.css?x=123" />' in page

    page = index_page(
        js_assets=[dict(defer=True, src="/assets/script.js")],
        css_assets=[
            dict(
                rel="stylesheet",
                crossorigin="use-credentials",
                href="https://foo.com/styles.css",
            )
        ],
    )
    assert '<script defer src="/assets/script.js"></script>' in page
    assert (
        '<link rel="stylesheet" crossorigin="use-credentials" href="https://foo.com/styles.css" />'
        in page
    )

    def contains_normalized(substring, string):
        normalized_substring = re.sub(r"\s+", " ", substring).strip()
        normalized_string = re.sub(r"\s+", " ", string).strip()

        # Check if normalized substring exists in the normalized string
        return normalized_substring in normalized_string

    page = index_page(
        js_assets=["/assets/script1.js"],
        raw_head_content=(
            """
            <script src="/assets/script2.js"></script>
            <link rel="stylesheet" href="/assets/styles.css" />
            <script>
              console.log("Hello World");
            <script>
            """
        ),
    )
    assert '<script src="/assets/script2.js"></script>' in page
    assert '<link rel="stylesheet" href="/assets/styles.css" />' in page
    assert contains_normalized(
        """
        <script>
          console.log("Hello World");
        <script>
        """,
        page,
    )
