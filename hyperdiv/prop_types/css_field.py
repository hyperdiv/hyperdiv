from .css import CSS


class CSSField(CSS):
    """
    `CSSField(field_name, typ)` creates a Hyperdiv type that accepts
    the values of `typ`, but whose rendered values will be rendered in
    the UI as CSS, instead of being passed to the UI component as
    attributes.

    `field_name` is a valid CSS attribute name.

    The `render` method on this type is expected to return a
    dictionary mapping the field name to a valid CSS value. For a font
    size prop, the `render` method would return, for example:

    ```
    { 'font-size': '1rem' }
    ```
    """

    def __init__(self, field_name, typ):
        self.field_name = field_name
        self.typ = typ

    def parse(self, value):
        return self.typ.parse(value)

    def render(self, value):
        rendered = self.typ.render(value)
        if rendered is not None:
            return {self.field_name: rendered}

    def __repr__(self):
        return f'CSSField["{self.field_name}":{repr(self.typ)}]'
