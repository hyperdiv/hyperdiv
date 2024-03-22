from ...test_utils import mock_frame
from ...prop_types import Size
from ..style import style


@mock_frame
def test_style():
    s = style(direction="horizontal")
    assert s.direction == "horizontal"

    s = style(direction="vertical")
    assert s.direction == "vertical"

    d = s.props_as_dict()
    assert d["direction"] == "vertical"

    s = style(width=10)
    assert s.direction is None

    d = s.props_as_dict()
    for prop_name, value in d.items():
        if prop_name == "width":
            exp_value = Size.parse(10)
        else:
            exp_value = None

        assert value == exp_value
        assert getattr(s, prop_name) == exp_value
