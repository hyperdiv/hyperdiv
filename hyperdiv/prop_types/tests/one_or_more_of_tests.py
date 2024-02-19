import pytest
from ..one_or_more_of import OneOrMoreOf


def test_one_or_more_of():
    o = OneOrMoreOf("foo", "bar")

    assert repr(o) == "OneOrMoreOf"

    assert o.parse(("foo",)) == ("foo",)
    assert o.parse(("bar",)) == ("bar",)
    assert o.parse(("foo", "bar",)) == (
        "foo",
        "bar",
    )

    with pytest.raises(ValueError):
        o.parse("baz")

    with pytest.raises(ValueError):
        o.parse(("foo", "baz"))

    with pytest.raises(ValueError):
        OneOrMoreOf()
