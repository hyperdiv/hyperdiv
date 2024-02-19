import pytest
from ...test_utils import mock_frame
from ..box_list import box_list
from ..box_list_item import box_list_item
from ..plaintext import plaintext


@mock_frame
def test_box_list():
    b = box_list(collect=False)
    with b:
        with pytest.raises(Exception):
            plaintext()

        box_list_item()
