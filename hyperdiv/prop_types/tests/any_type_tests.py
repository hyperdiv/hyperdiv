from ..any_type import Any


def test_any_type():
    assert repr(Any) == "Any"
    assert Any.parse(1) == Any.render(1) == 1
    assert Any.parse("Hello") == Any.render("Hello") == "Hello"
    assert Any.parse({"x": 1}) == Any.render({"x": 1}) == {"x": 1}
