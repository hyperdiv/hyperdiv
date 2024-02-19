from .cartesian_chart import cartesian_chart


def bar_chart(
    *datasets,
    labels=None,
    colors=None,
    grid_color="neutral-100",
    x_axis="linear",
    y_axis="linear",
    hide_legend=False,
    **kwargs,
):
    """
    A @component(cartesian_chart) that renders datasets as bars.

    ```py
    hd.bar_chart(
        (1, 18, 4),
        (4, 2, 28),
        labels=("Jim", "Mary")
    )
    ```
    """
    return cartesian_chart(
        "bar",
        *datasets,
        labels=labels,
        colors=colors,
        grid_color=grid_color,
        x_axis=x_axis,
        y_axis=y_axis,
        hide_legend=hide_legend,
        **kwargs,
    )
