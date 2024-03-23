from .prop_types import CSS
from .components.style import style, boxy_props
from .renderer import render_css_props, selector_template


class StylePart(CSS):
    """
    The type of a style part.

    The values accepted by this type are `hyperdiv.style()` objects.
    """

    def __init__(self, part_name, /, is_base_part=False, has_root=True):
        self.part_name = part_name
        self.is_base_part = is_base_part
        self.has_root = has_root

    def parse(self, value):
        if value is None:
            return None
        if not isinstance(value, style):
            raise ValueError(f"Expected type `style` but got {type(style)}")
        return value

    def render(self, style_part):
        if style_part is None:
            return None

        props = style_part._get_stored_props()
        rendered = render_css_props(props.values())

        for boxy_prop in boxy_props:
            if props[boxy_prop].value is not None:
                # If a boxy prop is set to a concrete value, we tack
                # "display:flex" onto the output CSS, because boxy props
                # don't make sense in non-flex context.
                rendered[selector_template] |= dict(display="flex")
                break

        return rendered

    def __repr__(self):
        return f"StylePart[{self.part_name}]"


def BasePart(part_name="base", has_root=True):
    return StylePart(part_name, is_base_part=True, has_root=has_root)
