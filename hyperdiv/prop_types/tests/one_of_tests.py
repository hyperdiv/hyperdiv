import pytest
from ..one_of import OneOf


def test_one_of():
    o = OneOf("foo", "bar")

    assert repr(o) == "OneOf"

    assert o.parse("foo") == "foo"
    assert o.parse("bar") == "bar"

    with pytest.raises(ValueError):
        assert o.parse("baz")
