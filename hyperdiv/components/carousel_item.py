from ..prop import Prop
from ..component_base import Component
from ..component_mixins.styled import Styled
from .common.shoelace_types import CarouselAspectRatio


# TODO: carousel_item doesn't respond to style props
class carousel_item(Component, Styled):
    """
    To be used with @component(carousel).
    """

    _tag = "sl-carousel-item"

    aspect_ratio = Prop(CarouselAspectRatio)
