from ...prop_types import Color
from .chart import chart
from .common.color_utils import pad_colors


def radar_chart(
    *datasets,
    labels=None,
    axis=None,
    colors=None,
    grid_color="neutral-100",
    hide_legend=False,
    show_tick_labels=True,
    r_min=None,
    r_max=None,
    **kwargs,
):
    """A radar chart component.

    ```py
    hd.radar_chart(
        (8, 6, 4, 8),
        axis=("Commits", "PRs", "Issues", "Discussions")
    )
    ```

    The `axis` specifies the "axis" of the radar, and each dataset
    gives values to each of the components on the axis.

    The optional `labels` specifies the names of the datasets, in
    order. Multiple datasets can be overlaid:

    ```py
    hd.radar_chart(
        (1, 4, 2, 4),
        (8, 6, 4, 8),
        labels=("Jim", "Alice"),
        axis=("Commits", "PRs", "Issues", "Discussions")
    )
    ```

    `colors` can be a list of Hyperdiv colors, overriding the
    automatically generated colors, and `hide_legend` can hide the
    clickable dataset legend. You can show or hide the tick labels
    using the `show_tick_labels` parameter. They are shown by default.

    ```py
    hd.radar_chart(
        (1, 4, 2, 4),
        (8, 6, 4, 8),
        labels=("Jim", "Alice"),
        colors=("fuchsia", "yellow"),
        axis=("Commits", "PRs", "Issues", "Discussions"),
        hide_legend=True,
        show_tick_labels=False
    )
    ```

    You can set the minimum and maximum values for the radar chart
    using the `r_min` and `r_max` parameters. These are overridden if
    the dataset values exceed the scale.
    ```py
    hd.radar_chart(
        (1, 4, 2, 11), # 11 exceeds the r_max
        axis=("Commits", "PRs", "Issues", "Discussions"),
        r_min=-10,
        r_max=10
    )
    ```


    """
    if not datasets:
        raise ValueError("Nothing to render in a chart.")

    if labels and len(labels) != len(datasets):
        raise ValueError("Length of `dataset` differs from length of `labels`")

    grid_color = Color.render(Color.parse(grid_color))
    colors = pad_colors(colors, len(datasets))

    datasets = [
        dict(
            data=d,
            label=(labels[i] if labels else None),
            backgroundColor=colors[i],
            borderColor=colors[i],
            borderWidth=1,
        )
        for i, d in enumerate(datasets)
    ]

    plugins_config = dict(colors=False)
    if not labels or hide_legend:
        plugins_config["legend"] = dict(display=False)

    return chart(
        config=dict(
            type="radar",
            data=dict(
                labels=axis,
                datasets=datasets,
            ),
            options=dict(
                plugins=plugins_config,
                maintainAspectRatio=False,
                responsive=True,
                scales=dict(
                    r=dict(
                        grid=dict(color=grid_color),
                        suggestedMin=r_min,
                        suggestedMax=r_max,
                        ticks=dict(
                            showLabelBackdrop=False, 
                            display=show_tick_labels,
                        ),
                    ),
                ),
            ),
        ),
        **kwargs,
    )
