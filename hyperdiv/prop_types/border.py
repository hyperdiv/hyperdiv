from .css import CSS
from .box_size import uniform_box
from .border_edge import BorderEdge


class BorderDef(CSS):
    """
    A Hyperdiv type for simultaneously defining the four borders of a component.

    The values it accepts are:
    * `None`, indicating an unspecified border.
    * The string `"none"`, indicating no border.
    * A `Border` value, which sets all four borders to the same value.
    * A 4-tuple of `Border` values, which sets each border
      independently, starting at the top border and going clockwise.

    Example values:

    ```py
    with hd.box(gap=1):
        # Unspecified:
        hd.button("Hello", border=None)
        # No border:
        hd.button("Hello", border="none")

        # Set all four border edges to the same value:
        hd.button(
            "Hello",
            border="0.5 solid neutral"
        )
        # Or, using tuple syntax:
        hd.button(
            "Hello",
            border=(0.5, "solid", "neutral")
        )

        # Set the border edges independently,
        # using string syntax:
        hd.button("Hello", border=(
            "0.5 solid neutral",
            "0.5 dashed red",
            "0.5 solid green",
            "0.5 dashed yellow"
        ))

        # Set the border edges independently,
        # using tuple syntax:
        hd.button("Hello", border=(
            (0.5, "solid", "neutral"),
            (0.5, "dashed", "red"),
            (0.5, "solid", "green"),
            (0.5, "dashed", "yellow")
        ))
    ```

    String and tuple syntax is interchangeable.
    """

    def parse(self, value):
        if value is None:
            return None

        if value == "none":
            return value

        try:
            edge = BorderEdge.parse(value)
            return tuple([edge] * 4)
        except Exception:
            pass

        if len(value) <= 0 or len(value) > 4:
            raise ValueError(f"Invalid border value: {value}.")

        output = []
        for v in value:
            output.append(BorderEdge.parse(v))

        while len(output) < 4:
            output.append(None)

        return tuple(output)

    def render(self, value):
        if value is None:
            return None

        if value == "none":
            return dict(border=value)

        if uniform_box(value) and value[0] is not None:
            return {"border": BorderEdge.render(value[0])}

        fields = ["border-top", "border-right", "border-bottom", "border-left"]

        output = dict()
        for i, f in enumerate(fields):
            if value[i]:
                output[f] = BorderEdge.render(value[i])

        return output or None

    def __repr__(self):
        return "Border"


Border = BorderDef()
