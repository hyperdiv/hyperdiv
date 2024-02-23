import socket
import datetime
import os
import sys
import signal
from tornado.web import Application, StaticFileHandler, HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from .debug import logger, PRODUCTION
from .connection import Connection
from .plugin import PluginAssetsCollector
from .frontend import get_frontend_public_path


class Server:
    _instance = None

    def __init__(self, port, app_function, task_runtime, index_page):
        if Server._instance:
            raise Exception("Hyperdiv is already running.")
        Server._instance = self
        self.port = port
        self.app_function = app_function
        self.task_runtime = task_runtime
        self.ioloop = IOLoop.current()
        self.app = self.create_application(index_page)
        self.server = HTTPServer(self.app)
        self.stopping = False

    def listen(self):
        self.server.listen(self.port, address=os.environ.get("HD_HOST", "localhost"))

    def start(self):
        print(f"Running at http://{os.environ.get('HD_HOST', 'localhost')}:{self.port}", file=sys.stderr)
        print("Ctrl-C to exit", file=sys.stderr)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        try:
            self.ioloop.start()
        except Exception:
            logger.exception("Ioloop exited abnormally.")

    def stop(self, sig, frame):
        # In case termination signal is sent repeatedly while the
        # server is shutting down, avoid enqueueing the draining
        # callbacks multiple times.
        if self.stopping:
            return
        self.stopping = True

        logger.info(f"Stopping with signal {sig}.")
        # Stop the server from accepting new connections:
        self.ioloop.add_callback_from_signal(self.server.stop)
        # Close all connections
        self.ioloop.add_callback_from_signal(Connection.close_all_connections)
        # Stop the ioloop, which will cause `self.run()` to return:
        self.ioloop.add_callback_from_signal(self.ioloop.stop)

    def create_application(self, index_page):
        index_bytes = index_page.encode("utf-8")
        modified_time = datetime.datetime.now()

        class HyperdivStaticFileHandler(StaticFileHandler):
            """
            When the UI requests a file that does not exist, this static file
            handler returns the index contents. This allows the app to
            load from any valid Hyperdiv location path, even though
            that path doesn't exist on the filesystem.
            """

            @classmethod
            def get_absolute_path(cls, root, path):
                if not path:
                    return "<index>"
                try:
                    os.stat(os.path.join(root, path))
                    return super().get_absolute_path(root, path)
                except FileNotFoundError:
                    return "<index>"

            def validate_absolute_path(self, root, abspath):
                if abspath == "<index>":
                    return "<index>"
                return super().validate_absolute_path(root, abspath)

            @classmethod
            def get_content(cls, abspath, start=None, end=None):
                if abspath == "<index>":
                    return index_bytes
                return super().get_content(abspath, start=start, end=end)

            def get_modified_time(self):
                if self.absolute_path == "<index>":
                    return modified_time
                return super().get_modified_time()

            def get_content_size(self):
                if self.absolute_path == "<index>":
                    return len(index_bytes)
                return super().get_content_size()

            def get_content_type(self):
                if self.absolute_path == "<index>":
                    return "text/html"
                return super().get_content_type()

        class HyperdivPluginHandler(StaticFileHandler):
            @classmethod
            def get_absolute_path(cls, root, path):
                if path in PluginAssetsCollector.plugin_assets:
                    return PluginAssetsCollector.plugin_assets[path]
                else:
                    raise HTTPError(404)

        public_path = get_frontend_public_path()

        routes = []

        routes.append((r"/plugins/(.*)", HyperdivPluginHandler, dict(path="/")))

        assets_dir = os.path.join(
            os.path.dirname(os.path.abspath(sys.argv[0])), "assets"
        )
        if os.path.isdir(assets_dir):
            routes.append(
                (
                    r"/assets/(.*)",
                    StaticFileHandler,
                    dict(path=assets_dir),
                )
            )

        routes.extend(
            [
                (
                    r"/ws",
                    Connection,
                    dict(
                        app_function=self.app_function,
                        task_runtime=self.task_runtime,
                        ioloop=self.ioloop,
                    ),
                ),
                (
                    r"/(.*)",
                    HyperdivStaticFileHandler,
                    dict(path=public_path),
                ),
            ]
        )
        return Application(routes, debug=not PRODUCTION)
