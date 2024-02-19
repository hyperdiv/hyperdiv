from .hyperdiv_type import HyperdivType


class Native(HyperdivType):
    """
    `Native(typ)` will accept values only from the Python type
    `typ`. It will type-check values `v` with `isinstance(v, typ)` and
    raise an error if that check returns `False`.

    However, `Native` can be constructed by passing an extra argument,
    `coercible_types`:

    `Native(typ, coercible_types=[typ1, typ2, ...])` will accept
    values from `typ`, as well as `typ1`, `typ2`, etc. However, it
    will coerce all values `v` to `typ` by calling `typ(v)` on them.

    If `typ(v)` fails, that error will be raised.

    """

    def __init__(self, typ, name=None, coercible_types=None):
        """
        `typ` should be a Python type. `coercible_types` is a list of
        additional accepted types. However, the final value will be
        coerced to `typ`.

        `name` is an optional name. By default, a name will be derived
        from `typ`.
        """

        self.typ = typ
        self.name = name or typ.__name__.capitalize()
        self.coercible_types = coercible_types

    def parse(self, value):
        types_to_check = (self.typ,)
        if self.coercible_types:
            types_to_check = (self.typ,) + tuple(self.coercible_types)

        if not isinstance(value, types_to_check):
            if len(types_to_check) == 1:
                type_list = self.typ.__name__
            else:
                type_list = (
                    f"one of ({', '.join([t.__name__ for t in types_to_check])})"
                )
            raise TypeError(f"Expected {type_list} but got {type(value).__name__}")

        return self.typ(value)

    def __repr__(self):
        return self.name


# Accepts only Python `int` values.
Int = Native(int)
# Coerces any given value into a Python string by calling `str()` on it.
String = Native(str, coercible_types=[object], name="String")
# Accepts only Python `str` values.
PureString = Native(str, name="PureString")
# Accepts only Python `bool` values, namely `True` and `False`.
Bool = Native(bool)
