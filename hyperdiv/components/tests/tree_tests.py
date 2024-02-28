from ...test_utils import mock_frame, MockRunner
from ..tree import tree
from ..tree_item import tree_item
from ..plaintext import plaintext
from ..icon import icon


@mock_frame
def test_tree():
    with tree(expand_icon_name="chevron-left", collapse_icon_name="chevron-right") as t:
        ti = tree_item("One")
        assert ti.label == "One"

        ti = tree_item("Two", disabled=True)
        assert ti.label == "Two"
        assert isinstance(ti.children[0], plaintext) and ti.children[0].content == "Two"
        assert ti.disabled

        ti = tree_item("Three", expand_icon_name="robot", collapse_icon_name="table")
        assert ti.label == "Three"
        assert isinstance(ti.children[1], icon)
        assert ti.children[1].name == "robot"
        assert ti.children[1].slot == t.expand_icon

        assert isinstance(ti.children[2], icon)
        assert ti.children[2].name == "table"
        assert ti.children[2].slot == t.collapse_icon

    assert isinstance(t.children[0], icon)
    assert t.children[0].name == "chevron-left"
    assert isinstance(t.children[1], icon)
    assert t.children[1].name == "chevron-right"

    assert len(t.selected_items) == 0


def test_selected_and_expanded():
    key = None
    one_key = None
    two_key = None
    three_key = None
    selected = None
    two_was_expanded = False
    two_was_collapsed = False

    def my_app():
        nonlocal key, one_key, two_key, three_key, selected, two_was_expanded, two_was_collapsed

        with tree(selection="multiple") as t:
            one = tree_item("One")
            with tree_item("Two") as two:
                three = tree_item("Three")

        key = t._key
        one_key = one._key
        two_key = two._key
        three_key = three._key

        selected = [item._key for item in t.selected_items]

        two_was_expanded = two.was_expanded
        two_was_collapsed = two.was_collapsed

    with MockRunner(my_app) as mr:
        assert selected == []

        mr.process_updates([(key, "_selected_keys", [one_key])])

        assert selected == [one_key]

        mr.process_updates([(key, "_selected_keys", [one_key, two_key, three_key])])

        assert selected == [one_key, two_key, three_key]

        mr.process_updates([(two_key, "expanded", True), (two_key, "changed", True)])

        assert two_was_expanded
        assert not two_was_collapsed

        mr.process_updates([(two_key, "expanded", False), (two_key, "changed", True)])

        assert not two_was_expanded
        assert two_was_collapsed
