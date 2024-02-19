from ...test_utils import mock_frame
from ..alert import alert
from ..scope import scope
from ..icon import icon
from ..plaintext import plaintext


@mock_frame
def test_alert():
    a = alert("Hello", "World", icon_name="activity", closable=False, duration=12.5)
    assert a.label == "Hello World"
    assert a.closable is False
    assert a.duration == 12.5

    assert (
        isinstance(a.children[0], plaintext) and a.children[0].content == "Hello World"
    )
    assert isinstance(a.children[1], icon) and a.children[1].name == "activity"

    for variant in ("primary", "neutral", "success", "warning", "danger"):
        with scope(variant):
            a = alert("Hello", variant=variant)
            assert a.variant == variant
            assert isinstance(a.children[1], icon)
