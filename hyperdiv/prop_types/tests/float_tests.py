from ..float_type import Float


def test_float():
    assert repr(Float) == "Float"
    assert Float.parse(145.5) == 145.5
    assert Float.parse(10) == 10

    assert Float.render(10) == 10
    assert Float.render(float("inf")) == "+Infinity"
    assert Float.render(float("-inf")) == "-Infinity"
