from .cartesian_chart import cartesian_chart


def bubble_chart(
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
    A @component(cartesian_chart) that renders datasets as bubble
    points. It works like @component(scatter_chart), but you can
    specify the visual size of the points by providing an extra `r`
    component for each point, which specifies the radius of the
    bubble in pixels.

    ```py
    hd.bubble_chart(
        ((1, 8), (8, 20), (3, 12)),
        ((10, 7), (5, 30), (10, 12)),
        labels=("Jim", "Mary")
    )
    ```

    In this dataset specification, each point is specified as `(y, r)`
    where `y` is the `y`-value and `r` is the size of the bubble, in
    pixels. The `x` is automatically inferred as `1`, `2`, `3`, ...,
    on the linear axis, since it is not specified. You can specify the
    `x` in each point, too, by passing 3-tuples, each specifying `(x, y, r)`.

    ```py
    hd.bubble_chart(
        ((0, 1, 8), (3, 8, 20), (7, 3, 12)),
        ((2, 10, 7), (8, 5, 30), (21, 10, 12)),
        labels=("Jim", "Mary")
    )
    ```

    Bubble points can be specified in the following ways:

    * A 2-tuple, specifying `(y, r)`. In this case, `x` is inferred
      from the `x_axis` argument, like above.

    * A 3-tuple, representing `(x, y, r)`.

    * A dict, like `dict(x=1, y=2, r=10)`. Equivalent to the above,
      but in dict form.

    See @component(cartesian_chart) for more.
    """
    return cartesian_chart(
        "bubble",
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
