import json
import threading
import sys

if sys.version_info < (3, 0):
    from SocketServer import TCPServer, BaseRequestHandler
else:
    from socketserver import TCPServer, BaseRequestHandler


class Dispatcher(BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()

        decoded = json.loads(data)
        method = decoded['method'].split('.')[1]
        params = decoded['params'][0]

        try:
            getattr(self, method)(params)
        except AttributeError:
            print('Unrecognized RPC Method... ')


class JSONRPCTCPServer(object):
    __slots__ = ['bind_address', 'tcp_server']

    def __init__(self, bind_address, dispatcher):
        self.bind_address = bind_address
        self.tcp_server = TCPServer(self.bind_address, dispatcher)

    def run(self):
        server_thread = threading.Thread(target=self.tcp_server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def shutdown(self):
        self.tcp_server.shutdown()
        self.tcp_server.server_close()
