import os
import json
import signal
import multiprocessing
import requests
import websocket
import hyperdiv as hd
from ..main import wait_for_port


def empty_app():
    def main():
        pass

    hd.run(main)


class MockServer:
    def __init__(self, fn=empty_app, port=9070):
        self.fn = fn
        self.port = port
        self.process = None
        self.prev_port = os.environ.get("HD_PORT")
        self.prev_debug = os.environ.get("HD_DEBUG")

    def __enter__(self):
        os.environ["HD_PORT"] = str(self.port)
        os.environ["HD_DEBUG"] = "1"
        self.process = multiprocessing.Process(target=self.fn)
        self.process.start()
        wait_for_port(self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.kill(self.process.pid, signal.SIGINT)
        self.process.join()

        if self.prev_port is None:
            del os.environ["HD_PORT"]
        else:
            os.environ["HD_PORT"] = self.prev_port

        if self.prev_debug is None:
            del os.environ["HD_DEBUG"]
        else:
            os.environ["HD_DEBUG"] = self.prev_debug

    def open_websocket(self):
        return websocket.create_connection(f"ws://{os.environ.get('HD_HOST', 'localhost')}:{self.port}/ws")

    def request_path(self, path):
        return requests.get(f"http://{os.environ.get('HD_HOST', 'localhost')}:{self.port}{path}").text


def checkbox_app():
    def my_fun():
        b = hd.checkbox("Hello", key="my-checkbox")

        if b.checked:
            hd.text("checked")

    hd.run(my_fun)


def test_websocket():
    """TODO"""

    with MockServer(checkbox_app) as s:
        ws = s.open_websocket()
        dom = json.loads(ws.recv())
        root = dom["dom"]
        root_key = root["key"]
        assert len(root["children"]) == 1
        assert root["children"][0]["key"] == "my-checkbox"

        ws.send(
            json.dumps(
                [{"type": "update", "updates": [["my-checkbox", "checked", True]]}]
            )
        )
        response = json.loads(ws.recv())
        assert "diff" in response
        assert root_key in response["diff"]
        assert "children" in response["diff"][root_key]
        assert len(response["diff"][root_key]["children"]) == 1
        cmd = response["diff"][root_key]["children"][0]
        assert cmd[0] == "insert"
        assert cmd[1] == 1
        assert len(cmd[2]) == 1
        txt = cmd[2][0]
        assert txt["props"] == {"content": "checked"}
        ws.close()


def test_server():
    with MockServer() as s:
        t1 = s.request_path("/")
        t2 = s.request_path("/foo")
        t3 = s.request_path("/foo/bar")

        assert t1 == t2 == t3

        s.request_path("/build/bundle.js")
