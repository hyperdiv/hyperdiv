from ...test_utils import mock_frame
from ..button import button
from ..icon import icon
from ..box import box


@mock_frame
def test_button():
    with box(collect=False):
        b = button("Click Me")
        assert b.label == "Click Me"

        b = button(prefix_icon="chevron-left", suffix_icon="chevron-right")
        assert len(b.children) == 2

        assert isinstance(b.children[0], icon) and b.children[0].name == "chevron-left"
        assert isinstance(b.children[1], icon) and b.children[1].name == "chevron-right"
