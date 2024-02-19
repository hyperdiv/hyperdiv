from ...test_utils import MockRunner
from ..checkbox import checkbox


def test_checkbox():
    key = None

    def my_app():
        nonlocal key
        c = checkbox("Hello", "World", checked=False)
        key = c._key

    with MockRunner(my_app) as mr:
        assert mr.get_state(key, "checked") is False

        mr.process_updates([(key, "checked", True)])
        assert mr.get_state(key, "checked") is True

        mr.process_updates([(key, "checked", "$reset")])
        assert mr.get_state(key, "checked") is False
