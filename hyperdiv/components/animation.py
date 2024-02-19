from ..prop_types import (
    Bool,
    ClampedFloat,
    ClampedInt,
    Constant,
    HyperdivType,
    Int,
    List,
    OneOf,
    Optional,
    String,
    Union,
)
from ..prop import Prop
from ..frame import AppRunnerFrame
from ..component_base import Component, BaseState
from ..component_mixins.slottable import Slottable
from ..component_mixins.styled import Width, Height

animation_names = (
    "none",
    "backInDown",
    "backInLeft",
    "backInRight",
    "backInUp",
    "backOutDown",
    "backOutLeft",
    "backOutRight",
    "backOutUp",
    "bounce",
    "bounceIn",
    "bounceInDown",
    "bounceInLeft",
    "bounceInRight",
    "bounceInUp",
    "bounceOut",
    "bounceOutDown",
    "bounceOutLeft",
    "bounceOutRight",
    "bounceOutUp",
    "fadeIn",
    "fadeInBottomLeft",
    "fadeInBottomRight",
    "fadeInDown",
    "fadeInDownBig",
    "fadeInLeft",
    "fadeInLeftBig",
    "fadeInRight",
    "fadeInRightBig",
    "fadeInTopLeft",
    "fadeInTopRight",
    "fadeInUp",
    "fadeInUpBig",
    "fadeOut",
    "fadeOutBottomLeft",
    "fadeOutBottomRight",
    "fadeOutDown",
    "fadeOutDownBig",
    "fadeOutLeft",
    "fadeOutLeftBig",
    "fadeOutRight",
    "fadeOutRightBig",
    "fadeOutTopLeft",
    "fadeOutTopRight",
    "fadeOutUp",
    "fadeOutUpBig",
    "flash",
    "flip",
    "flipInX",
    "flipInY",
    "flipOutX",
    "flipOutY",
    "headShake",
    "heartBeat",
    "hinge",
    "jackInTheBox",
    "jello",
    "lightSpeedInLeft",
    "lightSpeedInRight",
    "lightSpeedOutLeft",
    "lightSpeedOutRight",
    "pulse",
    "rollIn",
    "rollOut",
    "rotateIn",
    "rotateInDownLeft",
    "rotateInDownRight",
    "rotateInUpLeft",
    "rotateInUpRight",
    "rotateOut",
    "rotateOutDownLeft",
    "rotateOutDownRight",
    "rotateOutUpLeft",
    "rotateOutUpRight",
    "rubberBand",
    "shake",
    "shakeX",
    "shakeY",
    "slideInDown",
    "slideInLeft",
    "slideInRight",
    "slideInUp",
    "slideOutDown",
    "slideOutLeft",
    "slideOutRight",
    "slideOutUp",
    "swing",
    "tada",
    "wobble",
    "zoomIn",
    "zoomInDown",
    "zoomInLeft",
    "zoomInRight",
    "zoomInUp",
    "zoomOut",
    "zoomOutDown",
    "zoomOutLeft",
    "zoomOutRight",
    "zoomOutUp",
)


animation_easing_names = (
    "linear",
    "ease",
    "easeIn",
    "easeOut",
    "easeInOut",
    "easeInSine",
    "easeOutSine",
    "easeInOutSine",
    "easeInQuad",
    "easeOutQuad",
    "easeInOutQuad",
    "easeInCubic",
    "easeOutCubic",
    "easeInOutCubic",
    "easeInQuart",
    "easeOutQuart",
    "easeInOutQuart",
    "easeInQuint",
    "easeOutQuint",
    "easeInOutQuint",
    "easeInExpo",
    "easeOutExpo",
    "easeInOutExpo",
    "easeInCirc",
    "easeOutCirc",
    "easeInOutCirc",
    "easeInBack",
    "easeOutBack",
    "easeInOutBack",
)


class keyframe(BaseState):
    """
    <sl-badge variant="danger">Experimental</sl-badge>
    """

    width = Prop(Width)
    height = Prop(Height)


class KeyframeDef(HyperdivType):
    """The definition of a keyframe type."""

    def parse(self, value):
        if value is None:
            return None
        if not isinstance(value, keyframe):
            raise ValueError(f"Expected type `keyframe` but got {type(value)}")
        return value

    def render(self, keyframe):
        if keyframe is None:
            return None

        props = AppRunnerFrame.current().get_props(keyframe._key)

        output = dict()

        for prop in props.values():
            css = prop.render()
            if css:
                output.update(css)

        return output

    def __repr__(self):
        return "Keyframe"


Keyframe = KeyframeDef()


class animation(Component, Slottable):
    """
    <sl-badge variant="danger">Experimental</sl-badge>
    """

    _tag = "sl-animation"

    name = Prop(OneOf(*animation_names), "fadeIn")
    play = Prop(Bool, False)
    easing = Prop(OneOf(*animation_easing_names), "linear")
    direction = Prop(
        OneOf("normal", "reverse", "alternate", "alternate-reverse"),
        "normal",
    )
    delay = Prop(ClampedInt(low=0), 0)
    duration = Prop(ClampedInt(low=0), 300)
    end_delay = Prop(ClampedInt(low=0), 0)
    fill = Prop(String, "auto")
    iterations = Prop(Union(Constant("Infinity"), ClampedInt(low=0)), 1)
    iteration_start = Prop(ClampedFloat(low=0, high=1), 0)
    playback_rate = Prop(Int, 1)
    keyframes = Prop(Optional(List(Keyframe)))
