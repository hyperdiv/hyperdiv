from .component_base import Component
from .diff import Insert


class UIPropState:
    """Holds the prop values that the browser holds at this moment. This is
    used to determine if a prop changed and the new value should be
    sent to the browser.

    This data structure is updated

    (a) When a new dom or dom diff is sent to the browser. The data
        structure is updated to hold those new prop values before the
        dom or diff are sent off.

    (b) When a prop change is received from the browser. For example
        when the user checks a checkbox and `checked` is updated to
        `True`, this prop state is updated also.

    Note that (b) implicitly prevents browser-modified values from
    being echoed back to the browser.
    """

    Unset = object()

    def __init__(self, state):
        # A reference to component global state
        self.state = state
        # The values of props held by the UI
        self.props = dict()

    def get_prop_value(self, key, prop_name):
        if key not in self.props:
            return UIPropState.Unset
        if prop_name not in self.props[key]:
            return UIPropState.Unset
        return self.props[key][prop_name]

    def set_prop_values(self, props):
        for prop in props:
            if prop.internal:
                continue
            if isinstance(prop.value, Component):
                self.set_prop_values_from_component(prop.value)
            else:
                self.set_prop_value(prop)

    def set_prop_value(self, prop):
        if prop.internal:
            return
        if prop.key not in self.props:
            self.props[prop.key] = dict()
        self.props[prop.key][prop.name] = prop.value

    def set_prop_values_from_component(self, component):
        key = component._key
        props = self.state.get_props(key).values()
        self.set_prop_values(props)
        if component._has_children:
            for child in component._children:
                self.set_prop_values_from_component(child)

    def set_prop_values_from_diff(self, diff):
        for component_diff in diff._diff:
            self.set_prop_values(component_diff.props)
            for command in component_diff.children:
                if isinstance(command, Insert):
                    for component in command.components:
                        self.set_prop_values_from_component(component)

    def prop_changed(self, prop):
        if isinstance(prop.value, Component):
            return self.component_changed(prop.value)

        if prop.internal:
            return False

        ui_prop_value = self.get_prop_value(prop.key, prop.name)

        if ui_prop_value == UIPropState.Unset:
            return True

        return ui_prop_value != prop.value

    def component_changed(self, component):
        props = self.state.get_props(component._key)

        for prop in props.values():
            if self.prop_changed(prop):
                return True

        return False
