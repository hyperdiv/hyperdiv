from ...test_utils import mock_frame, MockRunner
from ..form import form
from ..box import box


@mock_frame
def test_form():
    with box(collect=False):
        with form() as f:
            f.checkbox(name="checkbox")
            f.text_input(name="text_input")
            f.color_picker(name="picker")
            f.textarea(name="textarea")
            f.slider(name="slider")
            f.radio_group(name="radio_group")
            f.select(name="select")
            f.switch(name="switch")
            f.submit_button()
            f.reset_button()


def test_submit():
    t0_key = None
    t1_key = None
    t2_key = None
    form_key = None
    result = None
    failed = 0

    def my_app():
        nonlocal t0_key, t1_key, t2_key, form_key, result, failed

        def validate1(v):
            if v != "Hello World":
                return "Should be Hello World"

        async def validate2(v):
            if v != "Hello World":
                return "Should be Hello World"

        with form() as f:
            form_key = f._key

            t0 = f.text_input(name="hello", required=True)
            t0_key = t0._key

            t1 = f.text_input("hello1", validation=validate1)
            t1_key = t1._key

            t2 = f.text_input("hello2", validation=validate2)
            t2_key = t2._key

        if f.submitted:
            result = f.form_data
            f.reset()

        if f.submit_failed:
            failed += 1

    with MockRunner(my_app) as mr:
        # This submit will fail since required fields are not filled in
        mr.process_updates(
            [(t0_key, "value", "Hello"), (form_key, "_submit_clicked", True)]
        )

        assert result is None
        assert failed == 1

        # Fill in required fields and submit again
        mr.process_updates(
            [
                (t1_key, "value", "Hello World"),
                (t2_key, "value", "Hello World"),
                (form_key, "_submit_clicked", True),
            ]
        )

    assert result == {
        "hello": "Hello",
        "hello1": "Hello World",
        "hello2": "Hello World",
    }

    assert failed == 1
