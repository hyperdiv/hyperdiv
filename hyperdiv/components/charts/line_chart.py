from .cartesian_chart import cartesian_chart


def line_chart(
    *datasets,
    labels=None,
    colors=None,
    grid_color="neutral-100",
    x_axis="linear",
    y_axis="linear",
    hide_legend=False,
    show_x_tick_labels=True,
    show_y_tick_labels=True,
    y_min=None,
    y_max=None,
    **kwargs,
):
    """
    A @component(cartesian_chart) that renders datasets as points
    connected by lines.

    ```py
    hd.line_chart(
        (1, 18, 4),
        (4, 2, 28),
        labels=("Jim", "Mary")
    )
    ```
    """
    return cartesian_chart(
        "line",
        *datasets,
        labels=labels,
        colors=colors,
        grid_color=grid_color,
        x_axis=x_axis,
        y_axis=y_axis,
        hide_legend=hide_legend,
        show_x_tick_labels=show_x_tick_labels,
        show_y_tick_labels=show_y_tick_labels,
        y_min=y_min,
        y_max=y_max,
        **kwargs,
    )
