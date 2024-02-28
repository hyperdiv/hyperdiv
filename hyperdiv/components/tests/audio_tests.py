from ...test_utils import mock_frame, MockRunner
from ..audio import audio
from ..media_source import media_source
from ..button import button


@mock_frame
def test_button():
    a = audio("/assets/test.mp3")
    assert isinstance(a.children[0], media_source)
    assert a.children[0].src == "/assets/test.mp3"

    with audio() as a:
        media_source(src="/assets/test.mp3")
        media_source(src="/assets/test.ogg")

    assert isinstance(a.children[0], media_source)
    assert a.children[0].src == "/assets/test.mp3"

    assert isinstance(a.children[1], media_source)
    assert a.children[1].src == "/assets/test.ogg"


def test_play_pause():
    key = None
    play_key = None
    pause_key = None

    def my_app():
        nonlocal key, play_key, pause_key

        a = audio("/assets/test.mp3")
        key = a._key

        pause = button("Pause")
        pause_key = pause._key
        if pause.clicked:
            a.pause()

        play = button("Play")
        play_key = play._key
        if play.clicked:
            a.play()

    with MockRunner(my_app) as mr:
        mr.process_updates([(play_key, "clicked", True)])

        assert mr.get_state(key, "playing")

        mr.process_updates([(pause_key, "clicked", True)])

        assert not mr.get_state(key, "playing")
