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
    automatically generated colors. And `hide_legend` can hide the
    clickable dataset legend.

    ```py
    hd.radar_chart(
        (1, 4, 2, 4),
        (8, 6, 4, 8),
        labels=("Jim", "Alice"),
        colors=("fuchsia", "yellow"),
        axis=("Commits", "PRs", "Issues", "Discussions"),
        hide_legend=True,
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
                        ticks=dict(showLabelBackdrop=False),
                    ),
                ),
            ),
        ),
        **kwargs,
    )
