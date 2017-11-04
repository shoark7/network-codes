import errno
import os
import signal
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from .request_handle import RequestHandler


request_handler = RequestHandler("HTML handler")
LISTEN_QUEUE_SIZE = 1024


def child_exit_handler(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
        except OSError:
            return

        if pid == 0:
            return


def serve():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # host, port = gethostname(), 8888
    host, port = 'localhost', 8888

    server_socket.bind((host, port))
    server_socket.listen(LISTEN_QUEUE_SIZE)
    print("Server is serving on port:", port)

    signal.signal(signal.SIGCHLD, child_exit_handler)

    while True:
        try:
            connect_socket, client_address = server_socket.accept()
        except IOError as e:
            code, msg = e.args
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()

        if pid == 0:
            server_socket.close()
            request_handler(connect_socket)
            os._exit(0)
        else:
            connect_socket.close()
