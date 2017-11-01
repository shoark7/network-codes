import socket


HOST, PORT = 'localhost', 8888
# Host is the server host and we'll use localhost here. Port is 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET means 'Address Family: IP version 4'.
# SOCK_STREAM means 'TCP socket that uses data called stream'

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 'SOL_SOCKET' refers to one of socket levels 
# SO_REUSEADDR an option meaning I'll use this address and ports even after server process is dead.
# 1 means... sorry.

server_socket.bind((HOST, PORT))  # Remeber that bind method only takes 'tuple', not even a list

server_socket.listen(1)  # 1 means max number of queue in a server socket

print('Serving HTTP on port %s ...' % PORT)

while True:
    conn, client_address = server_socket.accept()
    request = conn.recv(1024)
    print(request)

    http_response = b"""\
HTTP/1.1 200 OK

Hello world!
"""

    conn.sendall(http_response)
    conn.close()
