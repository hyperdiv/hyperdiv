from ..test_utils import MockRunner
from ..components.state import state
from ..components.button import button


def test_dataframe_assignments():
    try:
        from pandas import DataFrame
    except Exception:
        return

    state_key = None
    a_key = None
    b_key = None

    def my_app():
        nonlocal state_key, a_key, b_key

        df_state = state(df=None)
        state_key = df_state._key

        a_button = button("A")
        a_key = a_button._key
        if a_button.clicked:
            df_state.df = DataFrame(dict(A=[1, 2], B=[3, 4]))

        b_button = button("B")
        b_key = b_button._key
        if b_button.clicked:
            df_state.df = DataFrame(dict(A=[3, 4], B=[5, 6]))

    with MockRunner(my_app) as mr:
        assert mr.get_state(state_key, "df") is None

        mr.process_updates([(a_key, "clicked", True)])

        df = mr.get_state(state_key, "df")
        assert isinstance(df, DataFrame)
        assert df.equals(DataFrame(dict(A=[1, 2], B=[3, 4])))

        mr.process_updates([(b_key, "clicked", True)])
        df = mr.get_state(state_key, "df")
        assert isinstance(df, DataFrame)
        assert df.equals(DataFrame(dict(A=[3, 4], B=[5, 6])))
