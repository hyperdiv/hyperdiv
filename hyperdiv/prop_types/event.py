from .hyperdiv_type import HyperdivType
from .css import CSS
from .native import Bool, String


class Event(HyperdivType):
    """
    `Event(typ)` creates an event type out of an existing Hyperdiv
    type `typ`. This type represents events. For example
    @prop_type(BoolEvent) is used to represent mouse clicks.

    A prop with type `Event(typ)` will accept the values of `typ`, but
    automatically reset back to the prop's default value at the end of
    the run.

    In the case of mouse clicks, a `clicked` prop defined with
    `Prop(BoolEvent, False)` will become `True` for one run when the
    respective component is clicked, and is automatically reset back
    to `False` at the end of the run.

    """

    def __init__(self, typ):
        if isinstance(typ, CSS):
            raise ValueError(f"Cannot make a Event type out of CSS type {typ}")

        self.typ = typ

    def parse(self, value):
        return self.typ.parse(value)

    def render(self, value):
        return self.typ.render(value)

    def __repr__(self):
        return f"Event[{repr(self.typ)}]"


# A @prop_type(Event) type that accepts @prop_type(Bool) values.
BoolEvent = Event(Bool)
# A @prop_type(Event) type that accepts @prop_type(String) values.
StringEvent = Event(String)
