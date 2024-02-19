from .chart import chart
from .common.radial_chart_utils import get_radial_chart_config


def pie_chart(
    dataset,
    labels=None,
    colors=None,
    hide_legend=False,
    doughnut=True,
    **kwargs,
):
    """
    A good ol pie chart. `dataset` holds the numeric sizes of the
    slices.

    ```py
    hd.pie_chart((1, 3, 12, 8))
    ```

    `labels` gives names to the pie slices, order. And `colors`
    specifies custom colors, in the same order. When you set `labels`,
    the clickable legend will automatically be rendered unless you pass
    `show_legend=False`

    ```py
    hd.pie_chart(
        (1, 3, 12, 8),
        labels=("Oats", "Corn", "Garlic", "Onions"),
        colors=("yellow-300", "emerald", "fuchsia-400", "orange")
    )
    ```

    You can pass `doughnut=False` to close the doughnut hole.

    ```py
    hd.pie_chart(
        (1, 3, 12, 8),
        labels=("Oats", "Corn", "Garlic", "Onions"),
        colors=("yellow-300", "emerald", "fuchsia-400", "orange"),
        doughnut=False
    )
    ```

    """
    config = get_radial_chart_config(
        "doughnut" if doughnut else "pie", dataset, labels, colors, hide_legend
    )
    return chart(config=config, **kwargs)
