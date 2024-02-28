from .frame import StateAccessFrame
from .prop_types import Event, CSS
from .equalities import equalities


def to_caml_case(name):
    parts = name.split("_")
    return "".join([parts[0], *[part.capitalize() for part in parts[1:]]])


class Prop:
    """A `Prop` is a descriptor that proxies reads and writes to its
    corresponding `StoredProp` which is stored in `State`. A `Prop` is
    (a) the static description of the prop, including its name, type,
    and default value, and (b) a read/write proxy to its `StoredProp`.

    See how descriptors work:

    https://docs.python.org/3/howto/descriptor.html
    """

    def __init__(
        self,
        prop_type,
        default_value=None,
        name=None,
        ui_name=None,
        backend_immutable=False,
        internal=False,
    ):
        self.prop_type = prop_type
        self.default_value = default_value
        self.name = name
        self.ui_name = ui_name
        self.backend_immutable = backend_immutable
        self.internal = internal

    def __set_name__(self, klass, name):
        """Called when the definition of `klass` is interpreted by Python, on
        module load. `name` is the prop's attribute name.
        """
        self.name = name

    def __get__(self, component, objtype):
        """Called when the prop attribute is read."""
        if component is None:
            return self
        return StateAccessFrame.current().get_state(component._key, self.name)

    def __set__(self, component, value):
        """Called when the prop attribute is written."""
        return StateAccessFrame.current().update_state(component._key, self.name, value)


class StoredProp:
    """A `StoredProp` is the runtime representation of a prop. A
    `StoredProp` is what is actually stored in `State` and holds the
    current value of the prop.
    """

    Unset = object()

    def __init__(self, key, prop):
        """`key` is the key of the component to which this prop is
        attached. The other args come from `Prop`. See `create()`
        below.
        """
        self.key = key
        self.prop = prop

        self.name = prop.name
        self.ui_name = prop.ui_name
        self.prop_type = prop.prop_type
        self.default_value = prop.default_value
        self.backend_immutable = prop.backend_immutable
        self.internal = prop.internal

        # The value of the prop. This value starts off as Unset and is
        # set in init() when the component is first instantiated.
        self.value = StoredProp.Unset

        # Whether this prop has been mutated.
        self.mutated = False

        # The value this prop would have if it hadn't been mutated (or
        # the value it has now, if it hasn't yet been mutated). This
        # attribute starts off as Unset and is set in init() when the
        # component is first instantiated.
        self.init_value = StoredProp.Unset

        # Whether this prop is a resettable event prop like `clicked`
        self.is_event_prop = isinstance(prop.prop_type, Event)
        if self.is_event_prop:
            self.internal = True

        # Whether this is a CSS/style prop, which will get translated
        # to CSS instead of a component attribute.
        self.is_css_prop = isinstance(prop.prop_type, CSS)

        # The name that is shipped to the UI. Some shoelace attributes
        # are named `type` and `open` which are Python
        # keywords/built-ins. In that case, they'll be named
        # `item_type`, `opened` etc. on the Python side.
        self.ui_name = to_caml_case(prop.ui_name or prop.name)

    def init(self, value):
        """Called on every frame."""
        # Keep tracking the latest init value to use when resetting
        # this prop.
        parsed = self.parse(value)
        self.init_value = parsed
        if not self.mutated:
            self.value = parsed

    def parse(self, value):
        try:
            return self.prop_type.parse(value)
        except Exception as e:
            raise ValueError(f"Parse error in prop '{self.name}': {e}") from e

    def render(self):
        return self.prop_type.render(self.value)

    def value_changed(self, old, new):
        try:
            return bool(old != new)
        except Exception as e:
            if type(old) is not type(new):
                return True
            if type(old) in equalities:
                return not equalities[type(old)](old, new)

            raise ValueError(f"Comparison of values of type {type(old)} failed: {e}")

    def update(self, value):
        self.mutated = True
        parsed = self.parse(value)
        updated = self.value_changed(self.value, parsed)
        self.value = parsed
        return updated

    def reset(self):
        # Reset the prop to the latest init value.
        updated = self.value_changed(self.value, self.init_value)
        self.value = self.init_value
        self.mutated = False
        return updated

    @staticmethod
    def create(key, prop):
        """Create a `StoredProp` from a `Prop`"""
        return StoredProp(key, prop)
