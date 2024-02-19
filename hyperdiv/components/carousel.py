from ..prop_types import Bool, Int, OneOf, CSSField, StringEvent, Size
from ..prop import Prop
from ..component_base import Component
from ..slot import Slot
from ..component_mixins.styled import Styled
from .common.shoelace_types import CarouselAspectRatio
from ..style_part import BasePart, StylePart
from .carousel_item import carousel_item


class carousel(Component, Styled):
    """A carousel component that groups a set of
    @component(carousel_item) containers, which can contain arbitrary
    content. You can flip between the carousel items by interacting
    with the navigation controls.

    ```py
    with hd.carousel() as carousel:
        with hd.carousel_item() as it1:
            hd.text("1")
        with hd.carousel_item() as it2:
            hd.text("2")
        with hd.carousel_item() as it3:
            hd.text("3")
        with hd.carousel_item() as it4:
            hd.text("4")
    ```

    You can inspect which carousel item is selected by using the
    `selected_item` attribute.

    ```py
    with hd.carousel() as carousel:
        with hd.carousel_item() as it1:
            hd.text("1")
        with hd.carousel_item() as it2:
            hd.text("2")
        with hd.carousel_item() as it3:
            hd.text("3")
        with hd.carousel_item() as it4:
            hd.text("4")

    if carousel.selected_item == it1:
        hd.text("1")
    if carousel.selected_item == it2:
        hd.text("2")
    if carousel.selected_item == it3:
        hd.text("3")
    if carousel.selected_item == it4:
        hd.text("4")
    ```

    """

    _tag = "sl-carousel"

    # Whether to loop continuously when `autoplay` is `True`.
    loop = Prop(Bool, False)
    # Whether to render the left and right navigation buttons.
    navigation = Prop(Bool, True)
    # Whether to render the pagination buttons at the bottom of the
    # carousel.
    pagination = Prop(Bool, True)
    # Whether to flip between the carousel items automatically.
    autoplay = Prop(Bool, False)
    # How long to wait (in milliseconds) before going to the next item
    # in the carousel, when `autoplay` is set to `True`.
    autoplay_interval = Prop(Int, 3000)
    # How many slides (carousel items) should be rendered per page.
    slides_per_page = Prop(Int, 1)
    # How many carousel items to skip when navigating.
    slides_per_move = Prop(Int, 1)
    # Whether the carousel items move left-right or top-bottom when
    # navigating.
    orientation = Prop(OneOf("horizontal", "vertical"), "horizontal")
    # Whether the carousel can be navigated by grabbing and dragging
    # the carousel items with the mouse.
    mouse_dragging = Prop(Bool, False)
    # The aspect ratio of the carousel. A string taking values like
    # `"3/4"`, `"7/4"`, etc.
    aspect_ratio = Prop(CarouselAspectRatio)
    # The space between the slides.
    slide_gap = Prop(CSSField("--slide-gap", Size))
    # The amount of space to partially reveal the next slide.
    scroll_hint = Prop(CSSField("--scroll-hint", Size))
    _selected_item_key = Prop(StringEvent, "")

    next_icon = Slot()
    previous_icon = Slot()

    base_style = Prop(BasePart())
    scroll_container_style = Prop(StylePart("scroll-container"))
    pagination_style = Prop(StylePart("pagination"))
    pagination_item_style = Prop(StylePart("pagination-item"))
    pagination_item_active_style = Prop(StylePart("pagination-item--active"))
    navigation_style = Prop(StylePart("navigation"))
    navigation_button_style = Prop(StylePart("navigation-button"))
    navigation_button_previous_style = Prop(StylePart("navigation-button--previous"))
    navigation_button_next_style = Prop(StylePart("navigation-button--next"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._selected_item = None

    @property
    def selected_item(self):
        return self._selected_item

    def _collect_child(self, item):
        super()._collect_child(item)

        if not isinstance(item, carousel_item):
            return

        if (
            not (self._selected_item_key or self._selected_item)
        ) or item._key == self._selected_item_key:
            self._selected_item = item
