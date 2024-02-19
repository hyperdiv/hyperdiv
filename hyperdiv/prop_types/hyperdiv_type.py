class HyperdivType:
    """
    `HyperdivType` is the base class of all Hyperdiv types.

    Hyperdiv types are used to dynamically type-check component prop
    values, and to render those values into shapes suitable for
    sending to the UI.

    The core purpose of a Hyperdiv type is to provide two methods,
    `parse` and `render`:

    * `parse(value)` will dynamically check that `value` is in the right
      shape for the given type. It may also coerce or transform the
      value into a canonical shape.

    * `render(value)` takes a *parsed value* of the given type and
      transforms it into a shape suitable to be sent to the browser.

    Custom types used to define internal state props don't have
    to implement `render`.
    """

    def parse(self, value):
        return value

    def render(self, value):
        return value
