from ..prop_types import Any
from ..prop import Prop
from ..frame import StateAccessFrame
from ..component_base import BaseState


class state(BaseState):
    """
    `state` is the default and quickest means by which users can
    create and maintain custom application and UI state. The keyword
    arguments passed into the `state` constructor are dynamically
    converted into untyped props that persist across the application
    session.

    ```py
    state = hd.state(count=0, name="Henry")

    if hd.button("Increment Count").clicked:
        state.count += 1

    if hd.button("Toggle Name").clicked:
        if state.name == "Henry":
            state.name = "Bob"
        else:
            state.name = "Henry"

    hd.text("Count:", state.count)
    hd.text("Name:", state.name)

    ```

    In the example above, `count` and `name` become props of
    `state`. When the user clicks the buttons, the props are mutated.

    ## Initial Values

    Since the app function re-runs over and over, the initial values
    passed to `state` are recreated on every run. This is fine in most
    cases, but can cause unexpected behaviors if the initialization
    value is an object that is supposed to be unique.

    For example:

    ```py-nodemo
    state = hd.state(lock=threading.Lock())
    ```

    Here, the lock will be a *different lock object* every time the
    app re-runs, since `threading.Lock()` is called on every run. To
    get a unique lock object, use this pattern:

    ```py-nodemo
    state = hd.state(lock=None)
    if state.lock is None:
        state.lock = threading.Lock()
    ```

    In this example, the lock object is created only once, on the
    first run, and stored in `state.lock`. Since the `lock` prop is
    mutated on the first run, subsequent initializations to `None`
    will be ignored, and the prop will take its value from its
    internal, mutated state.

    If you want to define state with typed props, see @component(BaseState).
    """

    def __init__(self, /, **prop_kwargs):
        self._state_kwargs = prop_kwargs
        super().__init__(key=None, **prop_kwargs)

    def _get_props(self):
        return [
            Prop(Any, name=name, default_value=value)
            for name, value in self._state_kwargs.items()
        ]

    def __getattribute__(self, attr):
        frame = StateAccessFrame.current()

        try:
            is_prop = attr != "_key" and frame.has_prop(self._key, attr)
        except AttributeError:
            is_prop = False

        if is_prop:
            return frame.get_state(self._key, attr)

        return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        frame = StateAccessFrame.current()

        try:
            is_prop = attr != "_key" and frame.has_prop(self._key, attr)
        except AttributeError:
            is_prop = False

        if is_prop:
            return frame.update_state(self._key, attr, value)

        return super().__setattr__(attr, value)
