import pytest
from ..index_page import index_page


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
