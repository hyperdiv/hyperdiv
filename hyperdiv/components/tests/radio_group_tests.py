from ...test_utils import MockRunner, mock_frame
from ..radio_group import radio_group, radios, radio_buttons
from ..radio import radio
from ..radio_button import radio_button


@mock_frame
def test_radio_group():
    with radio_group():
        radio("One")
        radio("Two")

    with radio_group():
        radio_button("One")
        radio_button("Two")

    radio_group("My Group", options=("One", "Two"))

    radio_group("My", "Group", button_options=("One", "Two"))

    radios("One", "Two")
    radio_buttons("One", "Two")
