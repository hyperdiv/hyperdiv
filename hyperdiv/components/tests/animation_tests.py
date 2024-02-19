import pytest
from ...test_utils import mock_frame
from ..animation import Keyframe, keyframe


@mock_frame
def test_keyframe():
    assert repr(Keyframe) == "Keyframe"

    k = keyframe(width=10, height=1)

    with pytest.raises(Exception):
        Keyframe.parse("foo")

    assert Keyframe.parse(None) is None
    assert Keyframe.parse(k) == k

    assert Keyframe.render(None) is None
    assert Keyframe.render(k) == {"width": "10rem", "height": "1rem"}
