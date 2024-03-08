import pytest
from ....test_utils import mock_frame
from ....prop_types import Color
from ...box import box
from ...scope import scope
from ..cartesian_chart import cartesian_chart
from ..bar_chart import bar_chart
from ..line_chart import line_chart
from ..scatter_chart import scatter_chart
from ..bubble_chart import bubble_chart
from ..polar_chart import polar_chart
from ..radar_chart import radar_chart
from ..pie_chart import pie_chart
from ..common.color_utils import auto_color_generator, auto_colors


@mock_frame
def test_cartesian_chart():
    with box(collect=False):
        # Invalid chart type
        with pytest.raises(Exception):
            cartesian_chart("hello", (1, 2, 3))

        # No data
        with pytest.raises(Exception):
            cartesian_chart("bar")

        # Wrong number of labels
        with pytest.raises(Exception):
            cartesian_chart("bar", (1, 2, 3), labels=("A", "B"))

        # Chart with inferred x-axis
        c = cartesian_chart("bar", (1, 2, 3))
        assert c.config["type"] == "bar"
        assert c.config["data"]["datasets"][0]["data"] == [
            dict(x=0, y=1),
            dict(x=1, y=2),
            dict(x=2, y=3),
        ]

        # Specified y-axis
        c = cartesian_chart("line", (1, 2, 3), y_axis=(1, 2, 3))
        y_config = c.config["options"]["scales"]["y"]
        assert y_config["type"] == "category"
        assert y_config["labels"] == (1, 2, 3)

        # Specified x-axis
        c = cartesian_chart("bar", (1, 2, 3), x_axis=("A", "B", "C"))
        x_config = c.config["options"]["scales"]["x"]
        assert x_config["type"] == "category"
        assert x_config["labels"] == ("A", "B", "C")

        # Explicit x-values
        c = cartesian_chart("scatter", ((0, 1), (1, 2), (2, 3)))
        assert c.config["type"] == "scatter"
        assert c.config["data"]["datasets"][0]["data"] == [
            dict(x=0, y=1),
            dict(x=1, y=2),
            dict(x=2, y=3),
        ]

        # Explicitly (y, r) values
        c = cartesian_chart("bubble", ((1, 2), (2, 3), (3, 4)))
        assert c.config["type"] == "bubble"
        assert c.config["data"]["datasets"][0]["data"] == [
            dict(x=0, y=1, r=2),
            dict(x=1, y=2, r=3),
            dict(x=2, y=3, r=4),
        ]

        # Specified x-axis
        c = cartesian_chart("bubble", ((0, 1), (1, 2), (2, 3)), x_axis=("A", "B", "C"))
        assert c.config["type"] == "bubble"
        assert c.config["data"]["datasets"][0]["data"] == [
            dict(x="A", y=0, r=1),
            dict(x="B", y=1, r=2),
            dict(x="C", y=2, r=3),
        ]

        # Explicit (x, y, r) values
        c = cartesian_chart("bubble", ((1, 2, 3), (2, 3, 4), (3, 4, 5)))
        assert c.config["type"] == "bubble"
        assert c.config["data"]["datasets"][0]["data"] == [
            dict(x=1, y=2, r=3),
            dict(x=2, y=3, r=4),
            dict(x=3, y=4, r=5),
        ]

        # Dataset as a dict
        c = cartesian_chart(
            "bar",
            dict(chart_type="line", color="red", data=(1, 2, 3), label="A"),
        )
        assert c.config["type"] == "bar"
        assert c.config["data"]["datasets"][0]["data"] == [
            dict(x=0, y=1),
            dict(x=1, y=2),
            dict(x=2, y=3),
        ]
        assert (
            c.config["data"]["datasets"][0]["backgroundColor"]
            == "var(--sl-color-red-600)"
        )
        assert (
            c.config["data"]["datasets"][0]["borderColor"] == "var(--sl-color-red-600)"
        )
        assert c.config["data"]["datasets"][0]["label"] == "A"

        # Mixed dataset with partially inferred colors
        colorgen = auto_color_generator()
        c = cartesian_chart(
            "bar",
            (1, 2, 3),
            dict(chart_type="line", data=(1, 2, 3)),
            colors=("green",),
            labels=("A", "B"),
        )
        assert c.config["type"] == "bar"
        d0 = c.config["data"]["datasets"][0]
        assert d0["data"] == [dict(x=0, y=1), dict(x=1, y=2), dict(x=2, y=3)]
        assert d0["borderColor"] == d0["backgroundColor"] == "var(--sl-color-green-600)"
        d1 = c.config["data"]["datasets"][1]
        assert d1["data"] == [dict(x=0, y=1), dict(x=1, y=2), dict(x=2, y=3)]
        # Skip 1 color
        next(colorgen)
        c = Color.render(Color.parse(next(colorgen)))
        assert d1["borderColor"] == d1["backgroundColor"] == c

        # Specified (x, y) points as dicts
        c = cartesian_chart("bar", (dict(x=1, y=2), dict(x=2, y=3)))
        assert c.config["data"]["datasets"][0]["data"] == [
            dict(x=1, y=2),
            dict(x=2, y=3),
        ]

        # Specified (x, y, r) points as dicts
        c = cartesian_chart("bubble", (dict(x=1, y=2, r=1), dict(x=2, y=3, r=5)))
        assert c.config["data"]["datasets"][0]["data"] == [
            dict(x=1, y=2, r=1),
            dict(x=2, y=3, r=5),
        ]

        # Need to specify at least (y,r) for bubble
        with pytest.raises(Exception):
            cartesian_chart("bubble", (1, 2, 3))

        # Not all datasets have labels
        with pytest.raises(Exception):
            cartesian_chart(
                "bar", dict(label="A", data=(1, 2, 3)), dict(data=(4, 5, 6))
            )

        # Hide x tick labels
        c = cartesian_chart(
            "bar", 
            (1, 2, 3), 
            show_x_tick_labels=False,
            show_y_tick_labels=False,
        )
        assert c.config["options"]["scales"]["x"]["ticks"]["display"] is False
        assert c.config["options"]["scales"]["y"]["ticks"]["display"] is False

        # Set y-axis scale
        c = cartesian_chart("bar", (1, 2, 3), y_min=-10, y_max=10)
        assert c.config["options"]["scales"]["y"]["suggestedMin"] == -10
        assert c.config["options"]["scales"]["y"]["suggestedMax"] == 10


@mock_frame
def test_cartesian_constructors():
    with box(collect=False):
        mapping = dict(bar=bar_chart, line=line_chart, scatter=scatter_chart)
        for typ in ("bar", "line", "scatter"):
            with scope(typ):
                assert (
                    cartesian_chart(
                        typ,
                        (1, 2, 3),
                        (2, 3, 4),
                        labels=("A", "B"),
                        x_axis=(0, 1, 2),
                    ).config
                    == mapping[typ](
                        (1, 2, 3), (2, 3, 4), labels=("A", "B"), x_axis=(0, 1, 2)
                    ).config
                )

        assert (
            cartesian_chart(
                "bubble",
                ((1, 2), (2, 3), (3, 4)),
                ((2, 3), (3, 4), (4, 5)),
                labels=("A", "B"),
                x_axis=(0, 1, 2),
            ).config
            == bubble_chart(
                ((1, 2), (2, 3), (3, 4)),
                ((2, 3), (3, 4), (4, 5)),
                labels=("A", "B"),
                x_axis=(0, 1, 2),
            ).config
        )


@mock_frame
def test_pie_chart():
    with box(collect=False):
        with pytest.raises(Exception):
            pie_chart(None)
        with pytest.raises(Exception):
            pie_chart((1, 2, 3), labels=("A", "B"))
        # TODO
        pie_chart((1, 2, 3))


@mock_frame
def test_polar_chart():
    with box(collect=False):
        with pytest.raises(Exception):
            polar_chart(None)
        with pytest.raises(Exception):
            polar_chart((1, 2, 3), labels=("A", "B"))
        # TODO
        polar_chart((1, 2, 3))

        c = polar_chart((1, 2, 3), labels=("A", "B", "C"), show_tick_labels=False, r_min=-10, r_max=10)
        assert c.config["options"]["scales"]["r"]["ticks"]["display"] is False
        assert c.config["options"]["scales"]["r"]["suggestedMin"] == -10
        assert c.config["options"]["scales"]["r"]["suggestedMax"] == 10


@mock_frame
def test_radar_chart():
    with box(collect=False):
        with pytest.raises(Exception):
            radar_chart()
        with pytest.raises(Exception):
            radar_chart((1, 2, 3), (2, 3, 4), labels=("A", "B", "C"))
        # TODO
        radar_chart((1, 2, 3), (2, 3, 4))

        c = radar_chart(
            (1, 2, 3), (2, 3, 4), (3, 4, 5), 
            labels=("A", "B", "C"), 
            show_tick_labels=False, 
            r_min=-10, 
            r_max=10
        )
        assert c.config["options"]["scales"]["r"]["ticks"]["display"] is False
        assert c.config["options"]["scales"]["r"]["suggestedMin"] == -10
        assert c.config["options"]["scales"]["r"]["suggestedMax"] == 10

def test_color_wraparound():
    gen = auto_color_generator()

    i = len(auto_colors)
    while i > 1:
        next(gen)
        i -= 1

    assert next(gen) == auto_colors[-1]
    assert next(gen) == auto_colors[0]
    assert next(gen) == auto_colors[1]
