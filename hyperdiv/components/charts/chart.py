from ...component_base import Component
from ...component_mixins import Styled
from ...prop_types import Any
from ...prop import Prop


class chart(Component, Styled):
    """
    The base chart component. This component exposes a single prop
    containing the entire chart config that is ultimately passed to
    [Chart.js](https://www.chartjs.org/) on the frontend.

    This component is not meaningfully useful on its own. Instead, use
    @component(line_chart), @component(bar_chart),
    @component(scatter_chart), @component(bubble_chart),
    @component(pie_chart), @component(polar_chart),
    @component(radar_chart) to create charts.

    ## Updating Data

    Unlike many Hyperdiv components, the chart component does not
    expose mutable props. To mutate chart data, store it in
    @component(state), pass the state data to the chart, and mutate
    the state data.

    ```py
    state = hd.state(data=(1, 10, 3))
    hd.line_chart(state.data)

    if hd.button("Update").clicked:
        state.data = (2, 4, 30)
    ```

    Charts may expose mutable props in the future.

    ## Style

    The `chart` outer container can be styled with Hyperdiv style
    props. The chart constructor functions listed above pass
    `**kwargs` up to `chart`, so you can pass style props to those
    functions.

    ```py
    hd.line_chart(
        (1, 3, 4, 5),
        (2, 8, 1, 9),
        grid_color="neutral-200",
        background_color="neutral-50",
        border_radius="large",
        padding=1
    )
    ```
    """

    # The chart configuration
    config = Prop(Any, backend_immutable=True)
