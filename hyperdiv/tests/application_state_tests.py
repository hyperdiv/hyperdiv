import pytest
from ..test_utils import MockManualRunner
from ..frame import UIUpdatesFrame, ResetUIEventsFrame, AppRunnerFrame
from ..component_base import Component
from ..prop import Prop
from ..prop_types import Int, Bool, Event


class MyComponent(Component):
    x = Prop(Int, 0)
    z = Prop(Event(Bool), False)


def test_application_state():
    props = MyComponent._get_static_props()
    props_with_values = {(prop, prop.default_value) for prop in props}

    mr = MockManualRunner()

    state = mr.app_runner.state

    with AppRunnerFrame(mr.app_runner) as frame:
        state.init_props("my-key", props_with_values)

        assert frame.get_state("my-key", "x") == 0
        assert frame.get_state("my-key", "z") is False

        # Reads got registered:
        assert ("my-key", "x") in frame.deps
        assert ("my-key", "z") in frame.deps

        frame.update_state("my-key", "x", 20)

        # The update/mutation got registered:
        assert ("my-key", "x") in frame.mutations

        assert frame.get_state("my-key", "x") == 20

        # Reset to default value
        frame.reset_state("my-key", "x")
        assert frame.get_state("my-key", "x") == 0

        assert state.has_prop("my-key", "x")
        assert state.has_prop("my-key", "z")

        assert len(state.get_props("my-key")) == 2

    with ResetUIEventsFrame(mr.app_runner) as frame:
        frame.reset_state("my-key", "z")

    with AppRunnerFrame(mr.app_runner) as frame:
        # Cannot update event props when running user code:
        with pytest.raises(Exception):
            frame.update_state("my-key", "z", True)

    with UIUpdatesFrame(mr.app_runner) as frame:
        # Can update event props when Applying UI Updates:
        frame.update_state("my-key", "z", True)
        assert ("my-key", "z") in frame.event_mutations

    with ResetUIEventsFrame(mr.app_runner) as frame:
        # Can also update event props when resetting events:
        frame.reset_state("my-key", "z")

        # Cannot update non-event props while resetting events:
        with pytest.raises(Exception):
            frame.update_state("my-key", "x", 1)
