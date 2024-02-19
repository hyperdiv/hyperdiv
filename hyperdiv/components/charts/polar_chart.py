from ...prop_types import Color
from .chart import chart
from .common.radial_chart_utils import get_radial_chart_config


def polar_chart(
    dataset,
    labels=None,
    colors=None,
    grid_color="neutral-100",
    hide_legend=False,
    **kwargs,
):
    """
    A polar chart component. This works like @component(pie_chart) but
    unlike a pie chart, which shows dataset differences in the
    *angles* of the slices, the polar chart keeps the angles identical
    and emphasizes difference in the slice "lengths".

    The `labels` argument specifies the name of each slice, and the
    `dataset` specifies the value of each slice.

    ```py
    hd.polar_chart(
        (4, 6, 4, 8, 2),
        labels=("Oats", "Milk", "Cheese", "Garlic", "Onions")
    )
    ```

    The slice colors can be customized using the `colors` argument,
    and the legend can be hidden:

    ```py
    hd.polar_chart(
        (4, 6, 4, 8, 2),
        colors=("red-200", "orange-200", "blue-100", "green-300", "yellow"),
        labels=("Oats", "Milk", "Cheese", "Garlic", "Onions"),
        hide_legend=True
    )
    ```

    """
    grid_color = Color.render(Color.parse(grid_color))

    config = get_radial_chart_config("polarArea", dataset, labels, colors, hide_legend)
    config["options"]["scales"] = dict(
        r=dict(
            grid=dict(color=grid_color),
            ticks=dict(showLabelBackdrop=False),
        ),
    )

    return chart(config=config, **kwargs)
