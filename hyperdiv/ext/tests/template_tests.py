import hyperdiv as hd
from ...test_utils import mock_frame
from ..template import template


@mock_frame
def test_template():
    t = template(title="My App", logo="/assets/logo.svg")
    with t.body:
        hd.text("hello")
    t.add_sidebar_menu({"Foo": {"href": "/bar", "icon": "x"}})
    t.add_topbar_links({"Foo": {"href": "/bar", "icon": "x"}})
