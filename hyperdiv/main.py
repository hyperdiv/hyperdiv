from termcolor import colored
import webbrowser
import threading
import socket
import time
import sys
import os
from .server import Server
from .task_runtime import TaskRuntime
from .index_page import index_page as create_index_page
from .debug import PRODUCTION_LOCAL


def find_open_port(start=8988):
    for port in range(start, 65536):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("0.0.0.0", port))
            return port
        except OSError:
            continue
        finally:
            sock.close()
    raise Exception("Could not find an open port.")


def is_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    try:
        sock.connect((os.environ.get("HD_HOST", "localhost"), port))
    except (socket.timeout, ConnectionRefusedError):
        return False
    finally:
        sock.close()
    return True


def get_port():
    port = 8888

    port_env_var = os.getenv("HD_PORT")
    if port_env_var:
        try:
            port = int(os.getenv("HD_PORT"))
        except Exception as e:
            print(f"Invalid port: {port_env_var}. Error: {e}")
            sys.exit(1)
    elif PRODUCTION_LOCAL:
        # PRODUCTION_LOCAL indicates an app meant to be run locally by
        # users. In this case we dynamically find an open port instead
        # of failing with an "Adress is already in use" error in case
        # 8888 is occupied and HD_PORT is unspecified.
        port = find_open_port()

    return port


def wait_for_port(port):
    while not is_port_open(port):
        time.sleep(0.05)


def open_browser(port):
    def run():
        wait_for_port(port)
        webbrowser.open(f"http://{os.environ.get('HD_HOST', 'localhost')}:{port}")

    thread = threading.Thread(target=run)
    thread.start()


def run(app_function, task_threads=10, executor=None, index_page=None):
    """
    The entrypoint into Hyperdiv.

    When calling `run(app_function)`, Hyperdiv will start a web server
    ready to serve the app defined by `app_function`, on a local
    port. A user can connect a web browser to this port to interact
    with the app. The call to `run` will block until Hyperdiv exits.

    Hyperdiv listens for signals SIGINT and SIGTERM and will cleanly
    exit the web server when receiving one of those signals. For
    example, pressing Ctrl-C in the terminal where Hyperdiv is running
    will cause Hyperdiv to exit.

    Parameters:
    * `app_function`: The function implementing the Hyperdiv app.

    * `task_threads`: The number of threads to run in the internal
      [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html)
      used for running asynchronous @component(task) functions.

    * `executor`: A
      [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html)
      in which to run @component(task) functions. If this argument is
      non-`None`, `task_threads` will be ignored.

    * `index_page`: An index page generated with @component(index_page).

    * `port`: The port on which to start the web server. By default,
      the port is `8888`. Alternatively, the port can be set with the
      `HD_PORT` environment variable.

    """
    port = get_port()

    task_runtime = TaskRuntime(task_threads, executor=executor)
    server = Server(
        port,
        app_function,
        task_runtime,
        index_page=index_page or create_index_page(),
    )
    try:
        server.listen()
    except Exception as e:
        print(f"Failed to start on port {server.port}. {e}")
        print(
            "Try using a different port:",
            colored(f"HD_PORT=[port] python {sys.argv[0]}", "blue"),
        )
        task_runtime.shutdown()
        sys.exit(1)

    if PRODUCTION_LOCAL:
        open_browser(server.port)

    server.start()

    # At this point, the server has shut down.
    task_runtime.shutdown()
