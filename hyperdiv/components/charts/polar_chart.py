from ...prop_types import Color
from .chart import chart
from .common.radial_chart_utils import get_radial_chart_config


def polar_chart(
    dataset,
    labels=None,
    colors=None,
    grid_color="neutral-100",
    hide_legend=False,
    show_tick_labels=True,
    r_min=None,
    r_max=None,
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
    and the legend and tick labels can be hidden.

    ```py
    hd.polar_chart(
        (4, 6, 4, 8, 2),
        colors=("red-200", "orange-200", "blue-100", "green-300", "yellow"),
        labels=("Oats", "Milk", "Cheese", "Garlic", "Onions"),
        hide_legend=True,
        show_tick_labels=False
    )
    ```

    You can set the minimum and maximum values for the radar chart
    using the `r_min` and `r_max` parameters. These are overridden if
    the dataset values exceed the scale.
    ```py
    hd.polar_chart(
        (4, 6, 4, 11, 2), # 11 exceeds the r_max
        colors=("red-200", "orange-200", "blue-100", "green-300", "yellow"),
        labels=("Oats", "Milk", "Cheese", "Garlic", "Onions"),
        r_min=-10,
        r_max=10
    )
    ```

    """
    grid_color = Color.render(Color.parse(grid_color))

    config = get_radial_chart_config("polarArea", dataset, labels, colors, hide_legend)
    config["options"]["scales"] = dict(
        r=dict(
            grid=dict(color=grid_color),
            suggestedMin=r_min,
            suggestedMax=r_max,
            ticks=dict(
                showLabelBackdrop=False, 
                display=show_tick_labels,
            ),
        ),
    )

    return chart(config=config, **kwargs)
