import asyncio
from functools import cache
from .prop import Prop
from .frame import AppRunnerFrame, StateAccessFrame, TaskFrame
from .renderer import render_component
from .slot import Slot
from .collector import Collector
from .component_keys import (
    get_component_key,
    validate_component_key,
    register_component_key,
)
from .component_mixins.slottable import Slottable
from .prop_types import Event


class Component(Collector):
    """
    The base class for all Hyperdiv components.

    Should not be instantiated directly.
    """

    def __init__(self, *, key=None, collect=True, **prop_kwargs):
        super().__init__()

        frame = StateAccessFrame.current()
        frame.component_count += 1

        fixed_key = getattr(type(self), "_key", None)

        # Tasks are not allowed to create components, but they're
        # allowed to access global states.
        if not (key or fixed_key or isinstance(frame, AppRunnerFrame)):
            if isinstance(frame, TaskFrame):
                raise Exception("Cannot create UI components in a task.")
            else:
                raise Exception("Cannot create UI components in this context.")

        if key is not None:
            if not validate_component_key(key):
                raise ValueError(
                    f"Invalid key: {key}. Keys should be strings that start with a letter "
                    'and may contain letters, numbers, and the characters "-" and "_".'
                )
            self._key = get_component_key(key=key)
            register_component_key(self._key)
        elif fixed_key:
            # We do not register fixed keys / do not check for
            # duplicates in fixed keys.
            self._key = fixed_key
            fixed_key = True
        else:
            self._key = get_component_key()
            register_component_key(self._key)

        # Hyperdiv internal component name -- normally derived from the class name
        self._name = getattr(type(self), "_name", None) or type(self).__name__
        # The component's HTML tag as rendered in the UI
        self._tag = getattr(type(self), "_tag", None)
        # The component's HTML classes
        self._classes = getattr(type(self), "_classes", [])
        # The component's props, a list of Prop objects
        self._props = self._get_props()
        # The component's slots, a list of Slot objects
        self._slots = self._get_slots()
        # Whether the component can contain "direct" children, meaning
        # other than slotted children. Some components may allow
        # children but only in slots.
        self._has_direct_children = getattr(type(self), "_has_direct_children", True)
        # Whether the component can accept children, direct or in slots
        self._has_children = self._has_direct_children or len(self._slots) > 0
        # Whether the component can accept any more children. A
        # component can accept some children, then become sealed, in
        # which case it raises an exception if you try to add more
        # children to it.
        self._sealed = False
        # Whether the component has been collected. The component can
        # only be collected once per frame.
        self._collected = False

        self._init_props(**prop_kwargs)
        if collect:
            self.collect()

    def collect(self):
        """
        Called when the component is collected into the dom. If the
        component was constructed with `collect=False`, this method has
        to be called by the user code. Otherwise it is called
        automatically when the component is constructed.
        """
        if self._collected:
            raise ValueError("The component has already been collected.")
        AppRunnerFrame.current().collector_stack.collect(self)
        self._collected = True

    def _collect_child(self, child):
        if isinstance(child, Slottable) and child.slot:
            if child.slot not in self._slots:
                raise Exception(
                    f'Slot "{child.slot.name}" is invalid on this component.'
                )
        elif not self._has_direct_children:
            raise Exception("Cannot collect non-slotted elements into this component.")

        super()._collect_child(child)

    def __enter__(self):
        if self._has_children and not self._sealed:
            AppRunnerFrame.current().collector_stack.push(self)
            return self
        raise Exception(f"'{self._name}' cannot have children.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        AppRunnerFrame.current().collector_stack.pop()

    @property
    def children(self):
        """
        Returns the list of children of this component, if this
        component can have children. If the component cannot have
        children, accessing this property raises `ValueError`.
        """

        if self._has_children:
            return self._children
        raise ValueError(f"'{self._name}' cannot have children.")

    def render(self):
        """
        Returns the rendered component in the internal Hyperdiv JSON
        format. This function is used internally, but may be useful
        for debugging.
        """
        return render_component(self)

    def _get_props(self):
        return type(self)._get_static_props()

    def _get_slots(self):
        return type(self)._get_static_slots()

    @classmethod
    @cache
    def _get_static_props(cls):
        props = dict()
        for klass in reversed(cls.__mro__[:-1]):
            props.update(
                {
                    attr.name: attr
                    for attr in klass.__dict__.values()
                    if isinstance(attr, Prop)
                }
            )
        return props.values()

    @classmethod
    @cache
    def _get_static_slots(cls):
        slots = dict()
        for klass in reversed(cls.__mro__[:-1]):
            slots.update(
                {
                    attr.name: attr
                    for attr in klass.__dict__.values()
                    if isinstance(attr, Slot)
                }
            )
        return slots.values()

    def _get_stored_props(self):
        return StateAccessFrame.current().get_props(self._key)

    def _get_stored_prop(self, prop_name):
        return self._get_stored_props().get(prop_name)

    def trigger_event(self, prop_name, value):
        """
        Triggers the event prop with name `prop_name` by setting its value
        to `value`.
        """
        StateAccessFrame.current().trigger_event(self._key, prop_name, value)

    sentinel = object()

    def _init_props(self, **prop_kwargs):
        props_with_values = []

        for prop in self._props:
            value = prop.default_value
            new_value = prop_kwargs.pop(prop.name, Component.sentinel)
            if new_value != Component.sentinel:
                if isinstance(prop.prop_type, Event):
                    raise Exception(
                        f"Cannot initialize the event prop '{prop.name}' "
                        f"on component '{self._name}'"
                    )
                value = new_value
            props_with_values.append((prop, value))

        if len(prop_kwargs) > 0:
            raise Exception(
                f"Invalid keyword arguments on {self._name}: "
                f"{', '.join(prop_kwargs.keys())}"
            )

        StateAccessFrame.current().init_props(self._key, props_with_values)

    def set_prop_delayed(self, prop_name, prop_value, delay=1):
        """
        Sets the prop with `prop_name` to the value `prop_value` after a
        delay of `delay` seconds.

        This may be useful for auto-closing an ephemeral alert, dropdown,
        or dialog, after being shown for some duration of time.
        """
        from .components.task import task

        async def set_delayed():
            await asyncio.sleep(delay)
            setattr(self, prop_name, prop_value)

        set_prop_task = task()
        set_prop_task.rerun(set_delayed)

    def reset_prop(self, prop_name):
        """
        Resets the prop with the given name to initial values, as if it were
        never mutated.
        """
        StateAccessFrame.current().reset_state(self._key, prop_name)

    def reset_prop_delayed(self, prop_name, delay=1):
        """
        Like `set_prop_delayed` but instead of mutating the prop it resets
        it to its initial value.
        """
        from .components.task import task

        async def reset_delayed():
            await asyncio.sleep(delay)
            self.reset_prop(prop_name)

        set_prop_task = task()
        set_prop_task.rerun(reset_delayed)


class BaseState(Component):
    """
    The base class for all non-UI components -- components that never
    get collected and sent to the browser.

    You can subclass this class to define your own custom state with
    typed props. You can initialize props by passing corresponding
    kwargs to your subclass constructor:

    ```py
    class MyState(hd.BaseState):
        count = hd.Prop(hd.Int, 0)

        def increment(self):
            self.count += 1

    # Then, in the app function:
    state = MyState(count=5)
    if hd.button("Increment").clicked:
        state.increment()

    hd.text(state.count)
    ```

    You can wrap your subclass in @component(global_state) to make the
    state global, so that all instances share the same underlying state.

    This class is useless if instantiated directly. You should only
    subclass it.
    """

    def __init__(self, key=None, **prop_kwargs):
        """
        This class should not be instantiated directly.
        """
        super().__init__(key=key, collect=False, **prop_kwargs)

    def collect(self):
        """
        This method is overridden to do nothing, since state components
        are not collected into the dom.
        """
        pass
