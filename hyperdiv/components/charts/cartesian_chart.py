from ...prop_types import Color
from .chart import chart
from .common.color_utils import auto_color_generator

cartesian_chart_types = ("line", "bar", "scatter", "bubble")


def check_chart_type(chart_type):
    if chart_type not in cartesian_chart_types:
        raise ValueError(f"Invalid cartesian chart type: {chart_type}.")


def cartesian_chart(
    chart_type,
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
    ## Introduction

    `cartesian_chart` is the base chart constructor used by
    @component(line_chart), @component(bar_chart),
    @component(scatter_chart), and @component(bubble_chart). All these
    charts work fundamentally similarly in that they render `x`/`y`
    data on a grid. They only differ in how the rendered data looks
    visually. There is a slight exception for
    @component(bubble_chart), which in addition to `x` and `y`, it
    renders `r`-data, which is the radius of each bubble.

    Because they work similarly, multiple datasets of different types
    can be overlaid on the same chart.

    Parameters:
    * `chart_type`: One of `"bar"`, `"line"`, `"scatter"`, or `"bubble"`.
    * `*datasets`: The data to be rendered.
    * `labels`: The names of the datasets.
    * `colors`: The colors of the datasets.
    * `grid_color`: The color of the chart's grid lines.
    * `x_axis`: Can be a list of names, specifying that the axis is a
      fixed category of items. The default is `"linear"`, specifying a
      linear axis. It can also be `"logarithmic"`, specifying a log
      axis, or `"timeseries"` specifying time values.
    * `y_axis`: Same as above, but for the y-axis.
    * `hide_legend`: Hides the clickable legend at the top of the
      chart. This legend is rendered automatically when `labels` is
      specified, unless this parameter is set to `False`.
    * `show_x_tick_labels`: Hides the tick labels on the x-axis. Tick labels are shown by default.
    * `show_y_tick_labels`: As above, but for the y-axis.
    * `y_min`: The minimum value of the y-axis. This is overridden if a data value is less than this value.
    * `y_max`: As above, but for the maximum value of the y-axis.
    * `**kwargs`: Component style and slot props that are passed
      upward to @component(chart).

    Each of `line_chart`, `bar_chart`, `scatter_chart`, and
    `bubble_chart` simply invoke `cartesian_chart(chart_type, ...)`
    where `chart_type` is `"line"`, `"bar"`, `"scatter"`, and
    `"bubble"`, respectively.

    These functions return a @component(chart) object.

    ```py
    hd.bar_chart((1, 8, 4))
    # is equivalent to
    hd.cartesian_chart("bar", (1, 8, 4))
    ```

    ## Multiple Datasets

    Each chart type can accept multiple datasets:

    ```py
    hd.line_chart(
        (1, 8, 4),
        (2, 6, 9),
        (18, 4, 12)
    )
    ```

    ## Category Axis, Dataset Names, and Colors

    Each axis can be set to a fixed category of items by setting the
    axis to a tuple containing the items in the category. Then, each
    point in each dataset corresponds to a category item, in
    order.

    The datasets can be given names using the `labels` argument, which
    are rendered as a clickable legend at the top of the chart, unless
    `hide_legend` is set to `True`.

    The datasets can also be given custom colors using the `colors`
    argument.

    ```py
    hd.line_chart(
        (1, 8, 4),
        (2, 6, 9),
        (18, 4, 12),
        labels=("Jim", "Mary", "Joe"),
        colors=("yellow", "blue", "fuchsia"),
        x_axis=("Oats", "Corn", "Milk")
    )
    ```

    ## Log and Time Axes

    The `x_axis` and `y_axis` can also be set to `"logarithmic"` for
    log data, or `"timeseries"` for time data.

    A log axis de-emphasizes large differences among data:

    ```py
    hd.line_chart(
        (1, 18000, 20, 240241, 17),
        y_axis="logarithmic",
    )
    # Versus linear (the default):
    hd.line_chart(
        (1, 18000, 20, 240241, 17),
    )
    ```

    A timeseries axis can intelligently render time labels. You can
    pass millisecond Unix timestamps as time values:

    ```py
    import time
    now = int(time.time()*1000)
    day = 24 * 60 * 60 * 1000

    hd.line_chart(
        ((now, 20), (now+(2 * day), 100), (now+(18 * day), 80)),
        x_axis="timeseries",
    )
    ```

    ## Scale and Ticks
    You can choose to show or hide the tick labels on the x- and
    y-axis using the `show_x_tick_labels` and `show_y_tick_labels`
    parameters. Tick labels are shown by default.

    ```py
    hd.bar_chart(
        (2, 6, 10),
        show_x_tick_labels=False,
        show_y_tick_labels=False
    )
    ```
    You can control the y-axis scale using the `y_min` and `y_max`
    parameters. These are overridden if the data exceeds the defined
    scale.
    ```py
    hd.bar_chart(
        (2, 6, 11), # 11 exceeds the max value
        y_min=-10,
        y_max=10
    )
    ```    


    ## Mixed Datasets

    Cartesian datasets of different types can be mixed on the same
    chart. For any dataset, we can override the default chart type by
    passing a dictionary that specifies `chart_type`, and includes the
    data points in `data`.

    `chart_type` can be any of `"line"`, `"bar"`, `"scatter"`, and
    `"bubble"`.

    ```py
    hd.line_chart(
        (1, 4, 5), # defaults to "line"
        dict(
            # Override the default to "bar"
            # for this dataset:
            chart_type="bar",
            # The point data:
            data=(1, 4, 5)
        )
    )
    ```

    ## Dataset Specification

    Each dataset specifies a series of "points" to be rendered on the
    chart. Each point must specify the `(x, y)` values: the x-axis
    value, and y-axis value.

    ### Point Specification

    Each point in a `"line"`, `"bar"`, or `"scatter"` dataset can be
    specified in the following ways:

    * A single value, like `5`. This represents the `y`-value of the
      point, and its `x`-value is inferred from the `x_axis` argument.

    * A tuple, like `(1, 5)`. This represents `(x, y)`.

    * A dict, like `dict(x=1, y=2)`. This is equivalent to the above,
      but in dict form.

    Bubble points also take an `r` value in addition to `x` and `y`,
    specifying the radius of the bubble. Bubble points can be
    specified in the following ways:

    * A 2-tuple, like `(1, 10)`, specifying `(y, r)`. In this case,
      `x` is inferred from the `x_axis` argument, like above.

    * A 3-tuple, representing `(x, y, r)`.

    * A dict, like `(dict(x=1, y=2, r=10)`. Equivalent to the above,
      but in dict form.

    ### Dataset Options

    A dataset can be passed to a chart constructor either as a tuple
    of points (where each point is specified according to the spec
    above), or as a dictionary that allows further customization of
    the dataset.

    When passing the dataset as a dictionary, the dataset's tuple of
    points is provided in the dictionary's `data` property:

    ```py-nodemo
    dict(data=((1, 2), (3, 4)))
    ```

    In addition to `data`, the dictionary can provide `chart_type`,
    `color`, and `label` properties. `chart_type` allows mixing and
    matching multiple chart types in the same chart. `color` and
    `label` allow setting the dataset's color and label. These will
    override whatever is specified in the `colors` and `labels`
    top-level arguments.

    ```py
    hd.bar_chart(
        dict(
            data=(1, 18, 10),
            chart_type="line",
            label="Trend",
            color="green",
        ),
        dict(
            data=(1, 18, 10),
            label="Harvest",
            color="yellow"
        )
    )
    ```

    """

    check_chart_type(chart_type)

    if not datasets:
        raise ValueError("Nothing to render in a chart.")

    if labels and len(labels) != len(datasets):
        raise ValueError("Length of `datasets` differs from length of `labels`")

    grid_color = Color.render(Color.parse(grid_color))
    auto_color_gen = auto_color_generator()

    out_datasets = []

    for i, dataset in enumerate(datasets):
        out_dataset = dict(data=[], borderWidth=1)
        dataset_type = chart_type
        auto_color = next(auto_color_gen)

        if isinstance(dataset, dict):
            if "color" in dataset:
                color = Color.render(Color.parse(dataset["color"]))
                out_dataset["borderColor"] = color
                out_dataset["backgroundColor"] = color
            if "chart_type" in dataset:
                check_chart_type(dataset["chart_type"])
                out_dataset["type"] = dataset["chart_type"]
                dataset_type = out_dataset["type"]
            if "label" in dataset:
                out_dataset["label"] = dataset["label"]
            dataset_data = dataset["data"]
        else:
            dataset_data = dataset

        if "borderColor" not in out_dataset:
            if colors and len(colors) > i:
                color = Color.render(Color.parse(colors[i]))
            else:
                color = Color.render(Color.parse(auto_color))
            out_dataset["borderColor"] = color
            out_dataset["backgroundColor"] = color

        if "label" not in out_dataset:
            if labels:
                out_dataset["label"] = labels[i]

        for j, point in enumerate(dataset_data):
            # `r` the radius of bubble charts, if the current dataset
            # is a bubble dataset.
            r = None
            if isinstance(point, dict):
                # If a point is a dict, it should look like
                # dict(x=..., y=...), or dict(x=..., y=..., r=...) in
                # the case of bubble charts.
                x = point["x"]
                y = point["y"]
                if dataset_type == "bubble":
                    r = point["r"]
            elif isinstance(point, (tuple, list)):
                # If the point is a tuple:
                #
                # In a bubble chart, we accept
                # - a 2-tuple (y, r) with x being implied by the
                #   axis, or inferred.
                # - a 3-tuple (x, y, r)
                #
                # In a non-bubble chart we accept
                # - a 2-tuple (x, y)
                if dataset_type == "bubble":
                    if len(point) == 3:
                        x, y, r = point
                    elif len(point) == 2:
                        y, r = point
                        if isinstance(x_axis, (list, tuple)):
                            x = x_axis[j]
                        else:
                            x = j
                else:
                    x, y = point
            else:
                # If the point is a single value:
                # - This is an error if we're in a bubble chart, since
                #   bubble points should specify at least `y` and `r`
                # - Otherwise the value is `y`, and `x` is implied by
                #   the axis, or inferred.
                if dataset_type == "bubble":
                    raise ValueError(f"{point} is not a valid bubble value.")
                y = point
                if isinstance(x_axis, (list, tuple)):
                    x = x_axis[j]
                else:
                    x = j

            out_point = dict(x=x, y=y)
            if dataset_type == "bubble":
                out_point["r"] = r

            out_dataset["data"].append(out_point)

        out_datasets.append(out_dataset)

    # Labels check
    has_labels = ["label" in ds for ds in out_datasets]
    if any(has_labels) and not all(has_labels):
        raise ValueError("Either all datasets or no datasets should have labels.")

    # Set up axes. If `x_axis` and `y_axis` are a list/tuple, the axis
    # type is assumed to be "category", and the list items are the
    # members of the category.
    if isinstance(x_axis, (tuple, list)):
        x_axis_config = dict(type="category", labels=x_axis)
    else:
        x_axis_config = dict(type=x_axis)

    if isinstance(y_axis, (tuple, list)):
        y_axis_config = dict(type="category", labels=y_axis, reverse=True)
    else:
        y_axis_config = dict(type=y_axis)

    x_axis_config["grid"] = dict(color=grid_color)
    y_axis_config["grid"] = dict(color=grid_color)

    x_axis_config["ticks"] = dict(display=show_x_tick_labels)
    y_axis_config["ticks"] = dict(display=show_y_tick_labels)

    y_axis_config["suggestedMin"] = y_min
    y_axis_config["suggestedMax"] = y_max

    # Hide the legend if (a) there are no dataset labels specified, or
    # (b) `hide_legend` is True.
    plugins_config = dict(colors=False)
    if not any(has_labels) or hide_legend:
        plugins_config["legend"] = dict(display=False)

    return chart(
        config=dict(
            type=chart_type,
            data=dict(datasets=out_datasets),
            options=dict(
                plugins=plugins_config,
                maintainAspectRatio=False,
                responsive=True,
                scales=dict(
                    x=x_axis_config,
                    y=y_axis_config,
                ),
            ),
        ),
        **kwargs,
    )
