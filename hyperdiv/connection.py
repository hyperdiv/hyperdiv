import uuid
import json
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from .debug import logger
from .app_runner import AppRunner


class Connection(WebSocketHandler):
    """
    The websocket connection corresponding to a client session.

    When the user loads the app, a websocket connection is opened by
    the frontend. On the Python side, the connection object creates an
    AppRunner instance that will manage the running of the
    application.

    As updates are received on the websocket, they are relayed to the
    AppRunner, which will run application frames and reply to the
    frontend with new 'dom'.

    TODO: The websocket connection may disconnect randomly, without
    the user closing the browser tab. When a client disconnects, we
    will need to store the state of their AppRunner, and when it
    reconnects, we will need to retrieve/reify their
    AppRunner. Currently the AppRunner is lost on disconnect, so
    application state resets on reconnect.
    """

    _active_connections: dict[uuid.UUID, "Connection"] = dict()

    def __init__(self, application, request, app_function, task_runtime, ioloop):
        super().__init__(application, request)
        self.ioloop = ioloop
        self.client_id = uuid.uuid4()
        Connection._active_connections[self.client_id] = self

        # client_id = self.get_argument("clientId", None)
        # TODO: sync client_id (client_id) with client and restore
        # AppRunner on reconnect based on client_id.
        updates_arg = self.get_argument("updates", None)
        updates = []
        if updates_arg:
            try:
                updates = json.loads(updates_arg)
            except Exception as e:
                logger.warn(f"Corrupted `updates` argument: {e}")
        self.runner = AppRunner(self, task_runtime, app_function, updates)
        self.runner.start()
        logger.info(
            f"Connection opened. {len(Connection._active_connections)} connections open."
        )

    def open(self):
        pass

    def on_message(self, messages):
        messages = json.loads(messages)
        ui_updates = []
        for m in messages:
            ui_updates.extend(m["updates"])
        self.runner.enqueue_ui_updates(ui_updates)

    def on_close(self):
        self.runner.stop()
        Connection._active_connections.pop(self.client_id)
        logger.info(
            f"Connection closed. {len(Connection._active_connections)} connections open."
        )

    def send(self, message):
        async def _send():
            try:
                await self.write_message(json.dumps(message))
            except WebSocketClosedError:
                logger.exception("Connection closed error.")
            except Exception as e:
                logger.exception(f"Failed to write to client: {e}")

        self.ioloop.add_callback(_send)

    @staticmethod
    def close_all_connections():
        # TODO: Actually call close() on the connections?
        logger.info(f"Closing {len(Connection._active_connections)} connections.")
        for conn in Connection._active_connections.values():
            conn.runner.stop()
