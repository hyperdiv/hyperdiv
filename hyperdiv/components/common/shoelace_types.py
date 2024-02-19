from ...prop_types import OneOf, CSSField, Color, Size, String, Optional

# The variant of the component.
ShoelaceVariant = OneOf(
    "primary",
    "success",
    "neutral",
    "warning",
    "danger",
)

# The size of the component.
ShoelaceSize = OneOf(
    "small",
    "medium",
    "large",
)

# The placement of the component. `start` and `end` mean left/right or
# top/bottom depending on the base orientation. For example top-start
# means top-left, and right-start means right-top.
ShoelacePlacement = OneOf(
    "top",
    "top-start",
    "top-end",
    "bottom",
    "bottom-start",
    "bottom-end",
    "right",
    "right-start",
    "right-end",
    "left",
    "left-start",
    "left-end",
)

# The track color of the progress indicator.
ProgressTrackColor = CSSField("--track-color", Color)
# The color of the progress indicator.
ProgressIndicatorColor = CSSField("--indicator-color", Color)
# The track width of the progress indicator.
ProgressTrackWidth = CSSField("--track-width", Size)
# The aspect ratio of the carousel or carousel item.
CarouselAspectRatio = CSSField("--aspect-ratio", String)
# The auto-capitalize setting of the text input field.
InputAutoCapitalize = Optional(
    OneOf("off", "none", "on", "sentences", "words", "characters")
)
# Whether input auto correct is turned on in the text input field.
InputAutoCorrect = Optional(OneOf("on", "off"))
# Defines the behavior of the enter key while typing in the text
# field. See more [here](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/enterkeyhint).
InputEnterKeyHint = Optional(
    OneOf("enter", "done", "go", "next", "previous", "search", "send")
)
# Determines the kind of virtual keyboard to show when typing in
# the text input. See more [here](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inputmode).
InputMode = Optional(
    OneOf("none", "text", "decimal", "numeric", "tel", "search", "email", "url")
)
