import os
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from .request_handle import RequestHandler


request_handler = RequestHandler("HTML handler")
LISTEN_QUEUE_SIZE = 1024


def serve():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # host, port = gethostname(), 8888
    host, port = 'localhost', 8888

    server_socket.bind((host, port))
    server_socket.listen(LISTEN_QUEUE_SIZE)
    print("Server is serving on port:", port)

    while True:
        connect_socket, client_address = server_socket.accept()
        pid = os.fork()

        if pid == 0:
            server_socket.close()
            request_handler(connect_socket)
            os._exit(0)
        else:
            connect_socket.close()
