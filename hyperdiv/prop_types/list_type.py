from .hyperdiv_type import HyperdivType


class List(HyperdivType):
    """
    `List(typ)` Creates a type that accepts Python tuples or lists of
    values with Hyperdiv type `typ`. The individual elements of the
    given tuple/list will be parsed with `typ.parse`, and rendered
    with `typ.render`.

    The internally stored prop value will be a tuple of parsed values.
    """

    def __init__(self, typ):
        self.typ = typ

    def parse(self, value):
        if not isinstance(value, (tuple, list)):
            raise ValueError(f"Expected a tuple or list but got {type(value)}")
        return tuple([self.typ.parse(obj) for obj in value])

    def render(self, value):
        return tuple([self.typ.render(obj) for obj in value])

    def __repr__(self):
        return f"List[{repr(self.typ)}]"
