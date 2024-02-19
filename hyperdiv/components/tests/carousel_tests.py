from ...test_utils import mock_frame
from ..box import box
from ..carousel import carousel
from ..carousel_item import carousel_item


@mock_frame
def test_carousel():
    with box(collect=False):
        c = carousel()
        with c:
            item1 = carousel_item()
            box()
            carousel_item()

        assert len(c.children) == 3
        assert c.selected_item == item1

        c.selected_item
