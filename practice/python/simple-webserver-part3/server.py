import errno
import os
import signal
import socket


SERVER_ADDRESS = HOST, PORT = '', 8888
REQUEST_QUEUE_SIZE = 5


def grim_reaper(signum, frame):
    # If SIGCHLD signal happens
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
        except OSError:
            return

        if pid == 0:
            return


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print('Child PID: {pid}, Parent PID{ppid}'.format(
        pid=os.getpid(),
        ppid=os.getppid(),
    ))
    print(request.decode())
    http_response = """\
HTTP/1.1 200 OK

Hello world!
"""
    client_connection.sendall(http_response)


def server_forever():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(REQUEST_QUEUE_SIZE)
    print("Serving HTTP on port {port}".format(port=PORT))

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            client_conn, client_address = server_socket.accept()
        except IOError as e:
            code, msg = e.args
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()
        if pid == 0:
            server_socket.close()
            handle_request(client_conn)
            client_conn.close()
            os._exit(0)
        else:
            client_conn.close()


if __name__ == '__main__':
    server_forever()
