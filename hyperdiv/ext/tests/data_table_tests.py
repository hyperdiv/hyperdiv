import pytest
from ...test_utils import mock_frame, MockRunner
from ..data_table import data_table


@mock_frame
def test_data_table():
    with pytest.raises(Exception):
        data_table(dict(Age=(20, 30)), row_actions=lambda _: None)

    with pytest.raises(Exception):
        data_table(dict(Age=(20, 30)), show_select_column=True)

    with pytest.raises(Exception):
        data_table(dict(ID=(1,), Age=(20, 30)), id_column_name="ID")

    with pytest.raises(Exception):
        data_table(dict(ID=(1, 1), Age=(20, 30)), id_column_name="ID")

    data_table(dict(Age=()))

    data_table(dict(Age=(20, 30), Name=("Jim", "Mary")))

    data_table(dict(Age=(20, 30), Name=("Jim", "Mary")), rows_per_page=1)

    data_table(
        dict(ID=(1, 2), Age=(20, 30), Name=("Jim", "Mary")),
        rows_per_page=1,
        id_column_name="ID",
        show_select_column=True,
    )


def test_select_all_rows():
    toggle_all_checkbox_key = None
    table_state_key = None

    def my_app():
        nonlocal toggle_all_checkbox_key, table_state_key

        t = data_table(
            dict(
                ID=(0, 1, 2, 3, 4),
                Age=(20, 42, 41, 50, 32),
                Name=("Joe", "Mary", "Bob", "Alicia", "Steve"),
            ),
            id_column_name="ID",
            show_select_column=True,
            rows_per_page=2,
        )
        table_state_key = t.state._key
        toggle_all_checkbox_key = (
            t.children[0]  # Wrapper box
            .children[0]  # table
            .children[0]  # thead
            .children[0]  # tr
            .children[0]  # td
            .children[0]  # checkbox
            ._key
        )

    with MockRunner(my_app) as mr:
        assert mr.get_state(table_state_key, "selected_rows") == ()

        mr.process_updates(
            [
                (toggle_all_checkbox_key, "checked", True),
                (toggle_all_checkbox_key, "changed", True),
            ]
        )

        assert mr.get_state(table_state_key, "selected_rows") == (0, 1)

        mr.process_updates([(table_state_key, "page", 2)])
        mr.process_updates(
            [
                (toggle_all_checkbox_key, "checked", True),
                (toggle_all_checkbox_key, "changed", True),
            ]
        )

        assert mr.get_state(table_state_key, "selected_rows") == (0, 1, 2, 3)

        mr.process_updates([(table_state_key, "page", 3)])
        mr.process_updates(
            [
                (toggle_all_checkbox_key, "checked", True),
                (toggle_all_checkbox_key, "changed", True),
            ]
        )

        assert mr.get_state(table_state_key, "selected_rows") == (0, 1, 2, 3, 4)

        mr.process_updates([(table_state_key, "page", 2)])
        mr.process_updates(
            [
                (toggle_all_checkbox_key, "checked", False),
                (toggle_all_checkbox_key, "changed", True),
            ]
        )

        assert mr.get_state(table_state_key, "selected_rows") == (0, 1, 4)
