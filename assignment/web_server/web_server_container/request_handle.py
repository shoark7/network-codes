FILES = ['web_server/web_server_container/htmls/index.html',
         'web_server/web_server_container/htmls/sunghwan.html',
         'web_server/web_server_container/htmls/yeongjin.html',
         'web_server/web_server_container/images/favicon.ico']
PATHS = ['/', '/sunghwan', '/yeongjin', '/favicon.ico']


class RequestHandler:
    def __init__(self):
        self.path = ''
        self.method = ''
        self.html_template = b''
        self.response = b''

    def parse_request(self, request):
        splited_request = request.split()
        self.method, self.path = splited_request[:2]
        print(splited_request)

    def handle_request(self):
        if self.path not in PATHS:
            self.html_template = b"""\
HTTP/1.1 404 NOT FOUND\n\n<h1>Page you're looking for is not here!!</h1>"""
            self.response = self.html_template
            return
        else:
            self.html_template = b"""\
HTTP/1.1 200 OK\n\n"""

        file_index = PATHS.index(self.path)
        target_file = FILES[file_index]

        with open(target_file, 'rb') as fd:
            text = fd.read()

        self.response = self.html_template + text

    def __call__(self, client_socket):
        request = client_socket.recv(1024).decode()
        self.parse_request(request)
        self.handle_request()
        client_socket.sendall(self.response)
        client_socket.close()
