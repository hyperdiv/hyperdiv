from math import ceil
import hyperdiv as hd
from hyperdiv.component_base import BaseState
from hyperdiv.components.box import box


class TableState(BaseState):
    page = hd.Prop(hd.Int, 1)
    selected_rows = hd.Prop(hd.List(hd.Any), ())


class data_table(box):
    """
    `data_table` automatically renders a @component(table) given a
    dictionary of tabular data. The dictionary maps column names to
    column data:

    ```py
    hd.data_table(dict(
       Name=("Mary", "Joe", "Jim"),
       Age=(34, 21, 43)
    ))
    ```

    ## Pagination

    If the length of the data exceeds the value of the `rows_per_page`
    parameter, a pagination component is automatically rendered under
    the table, allowing users to click through the pages of the data.

    ```py
    hd.data_table(
        dict(
            Name=("Mary", "Joe", "Jim", "Bob", "Alice"),
            Age=(34, 21, 43, 61, 48)
        ),
        rows_per_page=3
    )
    ```

    The pagination component can be hidden by passing
    `show_pagination=False`. In that case, you will need to implement
    another way for users to see all the data.

    `data_table` provides methods to programmatically inspect and
    modify the pagination state.

    ## Selected Rows

    You can enable users to select rows, using checkboxes, by passing
    `show_select_column=True`. When `show_select_column` is `True`,
    the `id_column_name` kwarg must specify the name of a column that uniquely
    identifies each row. In a database, this would be the primary key
    column.

    You can access the selected rows using the `selected_rows`
    property, which holds the unique IDs of the selected rows. You can
    reset the selected rows by calling `reset_selected_rows()`.

    ```py
    table = hd.data_table(
        dict(
            Name=("Mary", "Joe", "Jim", "Bob", "Alice"),
            Age=(34, 21, 43, 61, 48)
        ),
        id_column_name="Name",
        rows_per_page=3,
        show_select_column=True
    )

    hd.text(table.selected_rows)

    if hd.button("Reset").clicked:
        table.reset_selected_rows()
    ```

    You can intercept change events when users select or deselect
    rows, using the `row_was_selected`, `row_was_deselected`, and
    `selected_rows_changed` properties.

    ## Row Actions

    Optionally, you can render a `row_actions` column with action
    buttons or indicators corresponding to each row. To do this, you
    pass a Python function into the `row_actions` kwarg. The Python
    function receives the row ID as a parameter.

    ```py
    def actions(name):
        with hd.hbox(padding=0.3, gap=0.3):
            with hd.tooltip(f"Edit {name}"):
                hd.button(
                    prefix_icon="pencil",
                    size="small",
                    outline=True
                )
            with hd.tooltip(f"Delete {name}"):
                hd.button(
                    prefix_icon="trash",
                    size="small",
                    outline=True
                )

    table = hd.data_table(
        dict(
            Name=("Mary", "Joe", "Jim", "Bob", "Alice"),
            Age=(34, 21, 43, 61, 48)
        ),
        id_column_name="Name",
        rows_per_page=3,
        row_actions=actions
    )
    ```

    ## Outer Styling

    `data_table` inherits from @component(box). The box is the outer
    wrapper around the table. You can do some basic styling of the
    outer box by passing style kwargs to `data_table`.

    ```py
    table = hd.data_table(
        dict(
            Name=("Mary", "Joe", "Jim", "Bob", "Alice"),
            Age=(34, 21, 43, 61, 48)
        ),
        border="1 solid neutral-100",
        width=20,
        font_color="yellow",
        font_family="mono",
    )
    ```
    """

    def __init__(
        self,
        data,
        id_column_name=None,
        show_id_column=True,
        rows_per_page=10,
        show_pagination=True,
        row_actions=None,
        show_select_column=False,
        vertical_scroll=False,
        **kwargs,
    ):
        """
        Parameters:

        * `data`: The data dictionary to be rendered in the table. It
          maps column names to the row value of each column.

        * `id_column_name`: Specifies a column name, from `data`,
          which identifies each row uniquely. You need to specify this
          argument if you use the `row_actions` or `show_select_column`
          arguments.

        * `show_id_column`: If `id_column_name` is specified, this controls
          whether the ID column is visible in the table.

        * `rows_per_page`: How many rows per page to show.

        * `show_pagination`: Whether to show or hide the pagination
          component when the length of each row in `data` is longer than
          `rows_per_page`. If you set this to `False`, you will need to
          implement an alternative way for users to paginate through
          the data.

        * `row_actions`: A function, taking the row's ID as a
          parameter, that renders row-specific Hyperdiv
          components. These components will be rendered as the last
          column in the table.

        * `show_select_column`: Whether to render a leading column of
          checkboxes, which enables users to select rows.

        `**kwargs` will be passed to the `box` superclass.
        """

        # The length of the longest rendered column:
        num_rows = max(
            [
                len(c)
                for col_name, c in data.items()
                if col_name != id_column_name or show_id_column
            ]
        )

        # Integrity checks:
        if id_column_name is None:
            if row_actions is not None:
                raise Exception(
                    "Cannot specify row_actions without specifying id_column_name."
                )
            if show_select_column:
                raise Exception(
                    "Cannot specify show_select_column=True without specifying id_column_name."
                )
        else:
            unique_ids = set(data[id_column_name])
            if len(unique_ids) != len(data[id_column_name]):
                raise Exception("The data in the ID column is not unique per row.")
            if len(unique_ids) != num_rows:
                raise Exception("The ID column does not provide IDs for all the rows.")

        self.state = TableState()
        self.selected_row_id = None
        self.deselected_row_id = None

        # If somehow we lost the unique ID column, reset the selected
        # state.
        if not id_column_name and self.state.selected_rows:
            self.state.selected_rows = ()

        # If some selected rows got deleted, update the selected rows state.
        if self.state.selected_rows:
            lost_ids = set(self.state.selected_rows).difference(unique_ids)
            if lost_ids:
                self.state.selected_rows = tuple(
                    row_id
                    for row_id in self.state.selected_rows
                    if row_id not in lost_ids
                )

        self.num_pages = ceil(num_rows / rows_per_page)

        # If some data got deleted such that the page number points
        # beyond the last page, update it to point to the last page.
        if self.state.page > self.num_pages:
            self.state.page = max(self.num_pages, 1)

        super().__init__(vertical_scroll=vertical_scroll, **kwargs)

        with self:
            # Render a 'No Data' box if there is no data to render.
            if num_rows == 0:
                with hd.box(
                    align="center",
                    justify="center",
                    padding=2,
                    border="1px solid neutral-100",
                    height="100%",
                ):
                    hd.text("No Data", font_color="neutral-400")
                    return

            # Otherwise render the data table.

            low = (self.state.page - 1) * rows_per_page
            high = min(num_rows, self.state.page * rows_per_page)

            with hd.box(horizontal_scroll=True):
                with hd.table() as self.table:
                    self._header(
                        data,
                        low,
                        high,
                        id_column_name,
                        show_select_column,
                        show_id_column,
                        row_actions,
                    )
                    self._body(
                        data,
                        low,
                        high,
                        id_column_name,
                        show_select_column,
                        show_id_column,
                        row_actions,
                    )

            if num_rows > rows_per_page and show_pagination:
                self._pagination()

    def _body(
        self,
        data,
        low,
        high,
        id_column_name,
        show_select_column,
        show_id_column,
        row_actions,
    ):
        with hd.tbody():
            for i in range(low, high):
                if id_column_name:
                    scope_id = data[id_column_name][i]
                else:
                    scope_id = i
                with hd.scope(scope_id):
                    with hd.tr():
                        # Leading checkbox select column, if any:
                        if show_select_column:
                            self._select_column_cell(scope_id)

                        # Data columns:
                        for j, (col_name, col) in enumerate(data.items()):
                            if col_name == id_column_name and not show_id_column:
                                continue
                            with hd.scope(j):
                                if i >= len(col):
                                    # Column lengths vary, so we can
                                    # have empty cells.
                                    hd.td()
                                else:
                                    hd.td(col[i])

                        # Trailing row actions column, if any:
                        if row_actions:
                            with hd.td(padding=0, width=0):
                                row_actions(scope_id)

    def _header(
        self,
        data,
        low,
        high,
        id_column_name,
        show_select_column,
        show_id_column,
        row_actions,
    ):
        with hd.thead():
            with hd.tr():
                if show_select_column:
                    # The toggle all checkbox in the header
                    self._toggle_all_cell(data, low, high, id_column_name)

                # The column name cells
                for col_name in data.keys():
                    if col_name == id_column_name and not show_id_column:
                        continue
                    with hd.scope(col_name):
                        hd.td(col_name)

                # If there are row actions, add an empty cell in the header
                if row_actions:
                    hd.td(width=0)

    def _pagination(self):
        with hd.hbox(
            border=(
                None,
                "1px solid neutral-100",
                "1px solid neutral-100",
                "1px solid neutral-100",
            ),
            padding=(0.5, 0.8, 0.5, 0.8),
            justify="space-between",
            align="center",
        ):
            if hd.icon_button("chevron-left", disabled=not self.has_prev_page).clicked:
                self.prev_page()
            hd.text(
                f"{self.state.page}/{self.num_pages}",
                font_family="mono",
                font_color="neutral-400",
            )
            if hd.icon_button("chevron-right", disabled=not self.has_next_page).clicked:
                self.next_page()

    def _toggle_all_cell(self, data, low, high, id_column_name):
        with hd.td(width=1):
            page_ids = set(data[id_column_name][low:high])
            selected_rows_ids = set(self.state.selected_rows)
            all_selected = page_ids.issubset(selected_rows_ids)
            some_selected = bool(page_ids.intersection(selected_rows_ids))
            checkbox = hd.checkbox(
                size="small",
                indeterminate=some_selected,
                checked=all_selected,
            )
            if checkbox.changed:
                if checkbox.checked:
                    self.state.selected_rows = tuple(selected_rows_ids.union(page_ids))
                else:
                    self.state.selected_rows = tuple(
                        selected_rows_ids.difference(page_ids)
                    )
                checkbox.reset_prop("indeterminate")
                checkbox.reset_prop("checked")

    def _select_column_cell(self, scope_id):
        with hd.td():
            with hd.scope(self.state.page):
                checkbox = hd.checkbox(
                    width=1,
                    size="small",
                    checked=(scope_id in self.state.selected_rows),
                )
                if checkbox.changed:
                    if checkbox.checked:
                        self.state.selected_rows = self.state.selected_rows + (
                            scope_id,
                        )
                        self.selected_row_id = scope_id
                    else:
                        self.state.selected_rows = tuple(
                            [
                                row_id
                                for row_id in self.state.selected_rows
                                if row_id != scope_id
                            ]
                        )
                        self.deselected_row_id = scope_id
                    checkbox.reset()

    @property
    def has_next_page(self):
        """`False` if pagination is on the last page, `True` otherwise."""
        return self.state.page < self.num_pages

    @property
    def has_prev_page(self):
        """`False` if pagination is on the first page, `True` otherwise."""
        return self.state.page > 1

    def next_page(self):
        """Navigates to the next page."""
        if self.state.page < self.num_pages:
            self.state.page += 1

    def prev_page(self):
        """Navigates to the previous page."""
        if self.state.page > 1:
            self.state.page -= 1

    @property
    def selected_rows(self):
        """Returns a tuple of the unique IDs of the selected rows."""
        return self.state.selected_rows

    def reset_selected_rows(self):
        """
        Sets `selected_rows` to the empty tuple. Corresponding checkboxes
        will be unchecked.
        """
        self.state.selected_rows = ()

    @property
    def row_was_selected(self):
        """
        Returns the ID of the row that was just selected, or `None`. Works
        like an event prop and resets to `None` at the end of the run.
        """
        return self.selected_row_id

    @property
    def row_was_deselected(self):
        """
        Returns the ID of the row that was just deselected, or
        `None`. Works like an event prop and resets to `None` at the
        end of the run.
        """
        return self.deselected_row_id

    @property
    def selected_rows_changed(self):
        """
        Returns `True` if a row was selected or deselected. Works like an
        event prop and resets to `False` at the end of the run.
        """
        return bool(self.row_was_selected or self.row_was_deselected)

    @property
    def page(self):
        """
        Returns the number of the current page. Page numbering starts at `1`.
        """
        return self.state.page
