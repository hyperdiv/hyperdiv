import pytest
from ...test_utils import MockRunner, mock_frame
from ...slot import Slot
from ..tab_group import tab_group
from ..tab import tab


@mock_frame
def test_tab_group():
    with tab_group() as group:
        tab("One")
        tab("Two")

    assert group.active == "One"
    assert group.closed is None


@mock_frame
def test_tab_group_shorthand():
    group = tab_group("One", "Two")
    assert group.active == "One"
    assert group.closed is None


def test_select_tab():
    t1_key = None
    t2_key = None
    group_key = None

    def app():
        nonlocal t1_key, t2_key, group_key

        with tab_group() as group:
            t1 = tab("One")
            t1_key = t1._key

            t2 = tab("Two")
            t2_key = t2._key

        group_key = group._key

    with MockRunner(app) as mr:
        assert mr.get_state(t1_key, "active") is True
        assert mr.get_state(t2_key, "active") is False

        mr.process_updates([(group_key, "_active_tab_key", t2_key)])

        assert mr.get_state(t1_key, "active") is False
        assert mr.get_state(t2_key, "active") is True


@mock_frame
def test_bad_slot():
    with tab_group():
        with pytest.raises(Exception):
            tab("One", slot=Slot("Hello"))
