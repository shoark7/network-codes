import logging

FILES = ['web_server/web_server_container/htmls/index.html',
         'web_server/web_server_container/htmls/sunghwan.html',
         'web_server/web_server_container/htmls/yeongjin.html',
         'web_server/web_server_container/images/favicon.ico',
         'web_server/web_server_container/css/style.css',
         'web_server/web_server_container/images/sunghwan.jpg',
         'web_server/web_server_container/images/yj.jpg',]
PATHS = ['/', '/sunghwan', '/yeongjin', '/favicon.ico', '/style.css',
         '/images/sunghwan.jpg', '/images/yj.jpg']


class RequestHandler:
    def __init__(self, name=None):
        self.name = name
        self.path = ''
        self.method = ''
        self.html_template = b''
        self.response = b''
        self.agent_string = ''
        self.is_mobile = False

        # Logger initializing
        self.logger = logging.getLogger('Access logger')
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler('web_server/web_server_container/access.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)

    def parse_request(self, request):
        try:
            splited_request = request.split()
            self.method, self.path, *agent_string = splited_request[:4]
            self.agent_string = ''.join(self.agent_string)
        except ValueError:
            return

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
        if 'html' in target_file:
            self.is_mobile = 'Mobile' if 'Android' in self.agent_string else 'Desktop'
            self.logger.info(self.is_mobile)

        with open(target_file, 'rb') as fd:
            text = fd.read()

        self.response = self.html_template + text

    def __call__(self, client_socket):
        request = client_socket.recv(1024).decode()
        self.parse_request(request)
        self.handle_request()
        client_socket.sendall(self.response)
        client_socket.close()
