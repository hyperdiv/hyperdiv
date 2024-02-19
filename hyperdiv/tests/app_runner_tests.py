import pytest
from ..test_utils import MockRunner, MockManualRunner
from ..components.lifecycle import lifecycle
from ..components.plaintext import plaintext
from ..components.local_storage import local_storage
from ..components.state import state
from ..components.button import button
from ..exceptions import Stop


def test_queues():
    mr = MockManualRunner()
    mr.advance()

    mr.app_runner.enqueue_ui_updates([("a", "b", "c")])
    stop, ui_updates, task_mutations = mr.app_runner.process_queue()

    assert ui_updates == [("a", "b", "c")]
    assert task_mutations == []
    assert stop is False

    mr.app_runner.enqueue_task_mutations([("a", "b", "c")])
    stop, ui_updates, task_mutations = mr.app_runner.process_queue()

    assert ui_updates == []
    assert task_mutations == [("a", "b", "c")]
    assert stop is False

    mr.app_runner.stop()
    stop, ui_updates, task_mutations = mr.app_runner.process_queue()

    assert stop is True
    assert ui_updates == [(lifecycle._key, "app_stopped", True)]
    assert task_mutations == []

    mr.app_runner.input_queue.put(("bad_key", []))

    with pytest.raises(Exception):
        mr.app_runner.process_queue()

    stop, ui_updates, task_mutations = mr.app_runner.process_queue()
    assert stop is False
    assert ui_updates == task_mutations == []


def test_storage():
    mr = MockManualRunner()
    ar = mr.app_runner

    storage = ar.get_storage("my_storage")
    storage["foo"] = "bar"

    assert ar.get_storage("my_storage") == {"foo": "bar"}


def test_prop_reset():
    key = None

    def my_app():
        nonlocal key
        t = plaintext(content="Initial")
        # Save the component key
        key = t._key
        t.content = "Updated"

    mr = MockManualRunner(my_app)
    mr.advance()

    assert mr.get_state(key, "content") == "Updated"
    mr.process_updates([(key, "content", "$reset")])

    assert mr.get_state(key, "content") == "Initial"


def test_commands():
    def my_app():
        local_storage.get_item("hello")

    mr = MockManualRunner(my_app)
    mr.advance()

    conn = mr.connection

    msg = conn.msgs[-1]

    assert "commands" in msg
    assert len(msg["commands"]) == 1
    cmd = msg["commands"][0]
    assert cmd["target"] == "localStorage"
    assert cmd["command"] == "getItem"
    assert cmd["args"] == ["hello"]


def test_run_loop():
    # Save component keys in these variables
    state_key = None
    button_key = None
    text_key = None

    def my_app():
        nonlocal button_key, state_key, text_key

        s = state(count=0)
        state_key = s._key

        b = button("Click Me")
        button_key = b._key

        if b.clicked:
            s.count += 1

        t = plaintext(s.count)
        text_key = t._key

    with MockRunner(my_app) as mr:
        # Simulate click
        mr.process_updates([(button_key, "clicked", True)])

        assert mr.get_state(state_key, "count") == 1

    # A diff was generated with the updated plaintext label
    conn = mr.connection
    msg = conn.msgs[-1]

    assert "diff" in msg
    assert text_key in msg["diff"]
    assert msg["diff"][text_key]["props"] == {"content": "1"}


def test_run_limit():
    def my_app():
        s = state(count=0)
        s.count += 1

    mr = MockManualRunner(my_app)
    with pytest.raises(RuntimeError):
        mr.app_runner.run_loop()


def test_task_mutations():
    state_key, text_key = None, None

    def my_app():
        nonlocal state_key, text_key

        s = state(count=0)
        state_key = s._key

        if s.count >= 1:
            t = plaintext("Hello")
            text_key = t._key

    mr = MockManualRunner(my_app)
    mr.advance()
    mr.update_state(state_key, "count", 1)
    mr.process_task_mutations([(state_key, "count")])
    assert mr.get_state(state_key, "count") == 1

    conn = mr.connection
    msg = conn.msgs[-1]

    assert "diff" in msg
    assert len(msg["diff"]) == 1
    root = list(msg["diff"].values())[0]
    assert "children" in root
    assert len(root["children"]) == 1
    cmd = root["children"][0]
    assert len(cmd) == 3
    assert cmd[0] == "insert"
    assert cmd[1] == 0
    assert len(cmd[2]) == 1
    inserted = cmd[2][0]
    assert inserted["key"] == text_key
    assert inserted["props"] == {"content": "Hello"}


def test_stop():
    def my_app():
        s = state(count=0)
        s.count += 1
        raise Stop()

    mr = MockManualRunner(my_app)
    # If stop() wasn't handled correctly, this would loop
    # indefinitely.
    mr.app_runner.run_loop_wrapper()


def test_trigger_event():
    b2_key = None
    text_key = None

    def my_app():
        nonlocal b2_key, text_key

        s = state(count=0)
        b1 = button("Button 1")
        b2 = button("Button 2")
        b2_key = b2._key

        if b1.clicked:
            s.count += 1
        if b2.clicked:
            # Trigger a click on b1, which will cause the count to be
            # incremented in the next frame.
            b1.trigger_event("clicked", True)

            # While we're here: can't trigger event on a non-event
            # prop:
            with pytest.raises(Exception):
                b1.trigger_event("size", "small")

        t = plaintext(s.count)
        text_key = t._key

    with MockRunner(my_app) as mr:
        mr.process_updates([(b2_key, "clicked", True)])

    # Assert that the click on b1 was processed, causing a diff output
    # with an updated text label.
    msg = mr.connection.msgs[-1]
    assert "diff" in msg
    assert text_key in msg["diff"]
    assert msg["diff"][text_key]["props"] == {"content": "1"}


def test_cannot_mutate_event_props():
    def my_app():
        b = button("Click Me")
        with pytest.raises(Exception):
            b.clicked = True

    mr = MockManualRunner(my_app)
    mr.advance()


def test_click_twice():
    """
    Test that an update batch containing updates to the same prop
    schedules those updates in different frames.
    """
    button_key = None
    text_key = None

    def my_app():
        nonlocal button_key, text_key

        s = state(count=0)

        b = button("Click Me")
        button_key = b._key

        if b.clicked:
            s.count += 1

        t = plaintext(s.count)
        text_key = t._key

    with MockRunner(my_app) as mr:
        mr.process_updates(
            [
                (button_key, "clicked", True),
                (button_key, "clicked", True),
            ]
        )
        assert mr.get_state(text_key, "content") == "2"
