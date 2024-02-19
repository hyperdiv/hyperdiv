from .color_utils import pad_colors


def get_radial_chart_config(chart_type, dataset, labels, colors, hide_legend):
    if not dataset:
        raise ValueError("Nothing to render in a chart.")

    if labels and len(labels) != len(dataset):
        raise ValueError("Length of `dataset` differs from length of `labels`")

    colors = pad_colors(colors, len(dataset))

    plugins_config = dict(colors=False)
    if not labels or hide_legend:
        plugins_config["legend"] = dict(display=False)

    return dict(
        type=chart_type,
        data=dict(
            labels=labels,
            datasets=[
                dict(
                    data=dataset,
                    backgroundColor=colors,
                    borderColor=colors,
                    borderWidth=1,
                )
            ],
        ),
        options=dict(
            plugins=plugins_config,
            maintainAspectRatio=False,
            responsive=True,
        ),
    )
