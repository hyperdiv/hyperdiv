import pytest
from ..test_utils import (
    mock_frame,
    MockManualRunner,
    MockRunner,
)
from ..frame import TaskFrame
from ..component_base import Component, BaseState
from ..prop import Prop
from ..prop_types import Int, Bool
from ..slot import Slot
from ..component_mixins.slottable import Slottable
from ..components.state import state
from ..components.button import button


@mock_frame
def test_bad_key():
    with pytest.raises(Exception):
        Component(key="-foo")

    with pytest.raises(Exception):
        Component(key="123")

    with pytest.raises(Exception):
        Component(key="a?b")


def test_tasks_cannot_create_components():
    mr = MockManualRunner()
    with TaskFrame(mr.app_runner):
        with pytest.raises(Exception):
            Component(key="abc")


class MyComponent(Component):
    x = Prop(Int, 0)


@mock_frame
def test_collect_twice_1():
    root = Component(collect=False)
    with root:
        # Implicitly collected
        child = Component()
        with pytest.raises(Exception):
            # Cannot collect again
            child.collect()


@mock_frame
def test_collect_twice_2():
    root = Component(collect=False)
    child = Component(collect=False)
    with root:
        # Collect once
        child.collect()
        with pytest.raises(Exception):
            # Cannot collect again
            child.collect()


class Parent(Component):
    foo = Slot()


class OtherComponent(Component):
    bar = Slot()


class Child(Component, Slottable):
    pass


@mock_frame
def test_slots():
    with Parent(collect=False) as p:
        Child(slot=p.foo)
        o = OtherComponent()

        # Cannot use a slot that is not a slot of the parent:
        with pytest.raises(Exception):
            Child(slot=o.bar)


class NoChildComponent(Component):
    _has_direct_children = False


@mock_frame
def test_no_children():
    p = NoChildComponent(collect=False)

    with pytest.raises(Exception):
        with p:
            Component()


class NoChildComponentWithSlot(Component):
    _has_direct_children = False
    foo = Slot()


@mock_frame
def test_no_children_with_slots():
    p = NoChildComponentWithSlot(collect=False)

    with p:
        Child(slot=p.foo)

    with pytest.raises(Exception):
        with p:
            Child()


@mock_frame
def test_children():
    p = NoChildComponent(collect=False)

    with pytest.raises(Exception):
        p.children


class ComponentWithProps(Component):
    x = Prop(Int, 0)
    y = Prop(Bool, False)


@mock_frame
def test_init_props():
    c = ComponentWithProps(collect=False, x=1, y=True)
    assert c.x == 1
    assert c.y is True

    with pytest.raises(Exception):
        c = ComponentWithProps(collect=False, x=1, y=True, z="Hello")


class MyState(BaseState):
    x = Prop(Int, 0)
    y = Prop(Bool, False)


@mock_frame
def test_state_no_collect():
    # Instantiating / collecting state without a parent to collect
    # into does not raise errors, since collection does nothing.
    s = MyState()
    s.collect()


def test_set_prop_delayed():
    state_key = None
    button1_key = None
    button2_key = None

    def my_app():
        nonlocal state_key, button1_key, button2_key

        s = state(count=0)
        state_key = s._key

        b1 = button("Click Me")
        button1_key = b1._key

        if b1.clicked:
            s.set_prop_delayed("count", 10, 0.0001)

        b2 = button("Click Me")
        button2_key = b2._key

        if b2.clicked:
            s.reset_prop_delayed("count", 0.0001)

    with MockRunner(my_app) as mr:
        mr.process_updates([(button1_key, "clicked", True)])
        assert mr.get_state(state_key, "count") == 10

        mr.process_updates([(button2_key, "clicked", True)])
        assert mr.get_state(state_key, "count") == 0
