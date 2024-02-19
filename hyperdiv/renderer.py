from jinja2 import Template
import json
from .prop_types import Bool


def render_css_props(css_props):
    # Format string allowing the caller to replace '{selector}' with
    # the real selector.
    selector = "{selector}"
    active_selector = f"{selector}:active"
    hover_selector = f"{selector}:hover"

    style = {
        selector: dict(),
        active_selector: dict(),
        hover_selector: dict(),
    }

    for prop in css_props:
        css = prop.render()
        if css:
            if prop.name == "hover_background_color":
                style[hover_selector].update(css)
            elif prop.name == "active_background_color":
                style[active_selector].update(css)
            else:
                style[selector].update(css)

    return style


def flatten_style(style):
    output = dict()
    for selector, css in style.items():
        if not css:
            continue
        output[selector] = ";".join([f"{k}:{v}" for k, v in css.items()])
    return output


def render_css(key, css_props):
    # TODO: fix circular import
    from .style_part import StylePart

    if not css_props:
        return None

    root_props = []
    css_parts = []
    base_part = None

    for prop in css_props:
        if isinstance(prop.prop_type, StylePart):
            if prop.prop_type.is_base_part:
                base_part = prop
            css_parts.append(prop)
        else:
            root_props.append(prop)

    root_selector = f"#{key}"

    # Render the root style
    style = {
        css_key.format(selector=root_selector): css_value
        for css_key, css_value in render_css_props(root_props).items()
    }

    # Render the part styles
    for css_part in css_parts:
        rendered_part = css_part.render()
        if rendered_part:
            part_selector = f"{root_selector}::part({css_part.prop_type.part_name})"
            part_style = {
                css_key.format(selector=part_selector): css_value
                for css_key, css_value in css_part.render().items()
            }
            style.update(part_style)

    root_style = style.get(root_selector)

    if base_part and root_style:
        # If the component has a base part, we move the root styles to
        # the base selector. If the component has a root selector (the
        # vast majority of components do), we leave dimension and flex
        # attributes on the root.
        base_selector = f"{root_selector}::part({base_part.prop_type.part_name})"

        style.setdefault(base_selector, dict())

        for attr_name, attr_value in dict(root_style).items():
            if base_part.prop_type.has_root:
                if attr_name in ("width", "height", "max-width", "max-height"):
                    if attr_name not in style[base_selector]:
                        style[base_selector][attr_name] = "100%"
                    continue
                if attr_name in ("flex-basis", "flex-grow", "flex-shrink"):
                    continue
            # If the attribute is not set in the base selector, we
            # move it from the root to the base.
            if attr_name not in style[base_selector]:
                style[base_selector][attr_name] = attr_value
                root_style.pop(attr_name)

    return flatten_style(style)


def render_slot_name(name):
    return name.replace("_", "-")


def render_props(key, props):
    css_props, normal_props = [], []

    for prop in props:
        if prop.name == "slot" and prop.value is None:
            continue
        if prop.is_css_prop:
            css_props.append(prop)
        elif not prop.internal:
            normal_props.append(prop)

    output = dict(props={prop.ui_name: prop.render() for prop in normal_props})

    style = render_css(key, css_props)
    if style is not None:
        output["style"] = style

    return output


def render_component(component):
    key = component._key
    name = component._name
    tag = component._tag
    classes = component._classes
    props = component._get_stored_props().values()

    output = dict(key=key, name=name, tag=tag, classes=classes) | render_props(
        key, props
    )

    if component._has_children:
        output["children"] = [child.render() for child in component._children]

    return output


# Experimental HTML Renderer -- Currently Unused.


def render_value(value):
    import json

    return json.dumps(value)


def render_prop_to_html(prop):
    value = prop.render()
    if isinstance(value, (list, tuple)):
        value = " ".join(value)
    return value


def render_component_to_html(component, indent=0):
    key = component._key
    name = component._name
    tag = component._tag
    classes = component._classes
    props = component._get_stored_props()

    if name == "plaintext":
        return (" " * indent) + component.content, {}

    css_props, normal_props = [], []

    for prop in props.values():
        if prop.name == "slot" and prop.value is None:
            continue
        if prop.is_css_prop:
            css_props.append(prop)
        elif not prop.is_event_prop:
            normal_props.append(prop)

    css = render_css(key, css_props) or dict()

    rendered_props = []

    for prop in normal_props:
        if prop.value == prop.default_value:
            continue

        if name in ("markdown", "text") and prop.name == "content":
            continue

        if prop.prop_type == Bool and prop.value:
            rendered_props.append(f"{prop.ui_name}")
            continue

        rendered_props.append(f"{prop.ui_name}={json.dumps(render_prop_to_html(prop))}")

    opening_tag = f'<{tag} id="{key}"'

    if len(classes) > 0:
        opening_tag += f" class=\"{' '.join(classes)}\""

    if len(rendered_props) > 0:
        opening_tag += " " + " ".join(rendered_props) + ">"
    else:
        opening_tag += ">"

    closing_tag = f"</{tag}>"

    output = (" " * indent) + opening_tag

    if name == "text":
        content = props.get("content")
        output += content.render() + closing_tag
    elif name == "markdown":
        content = props.get("content")
        if content.value:
            output += content.render()
        output += closing_tag
    elif (
        component._has_children
        and len(component._children) == 1
        and component._children[0]._name == "plaintext"
    ):
        child_html, child_css = render_component_to_html(component._children[0])
        output += child_html.strip() + closing_tag
        css |= child_css
    elif component._has_children and len(component._children) > 0:
        output += "\n"
        for child in component._children:
            child_html, child_css = render_component_to_html(child, indent=(indent + 1))
            output += child_html
            output += "\n"
            css |= child_css
        output += (" " * indent) + closing_tag
    else:
        output += closing_tag

    return output, css


def flatten_css(css):
    output = ""

    for selector, rules in css.items():
        if not rules:
            continue
        output += selector + " { " + rules + " }\n"

    return output


def render_into_template(html, css, template_text):
    template = Template(template_text)
    return template.render(body=html, style=flatten_css(css))
