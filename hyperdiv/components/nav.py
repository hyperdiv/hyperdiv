from .box import box


class nav(box):
    """
    A @component(box) that is useful for building usable navigation
    menus. Navigation menus should be wrapped in `nav` in order to
    help screen readers and other accessibility tools to better
    understand the website's structure.

    See more [here](https://www.w3schools.com/tags/tag_nav.asp).

    """

    _tag = "nav"
