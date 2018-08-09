import json
import sys
import threading

if sys.version_info < (3, 0):
    from SocketServer import TCPServer, BaseRequestHandler
else:
    from socketserver import TCPServer, BaseRequestHandler


class Dispatcher(BaseRequestHandler):

    def handle(self):
        """ Handles the data sent back from the Babble node. """
        data = self.request.recv(1024).strip()

        decoded = json.loads(data)
        method = decoded['method'].split('.')[1]
        params = decoded['params'][0]

        try:
            getattr(self, method)(params)
        except AttributeError:
            print('Unrecognized RPC Method... ')


class JSONRPCTCPServer(object):
    # Makes sure multiple instances of `self` with the same `bind_address` are not initialised
    __slots__ = ['bind_address', 'tcp_server']

    def __init__(self, bind_address, dispatcher):
        """ Creates a TCP server to listen for messages from the Babble node.

        :param bind_address: tuple consisting of ip and port where the application is listening
        :type bind_address: tuple(ip:str, port:int)
        :param dispatcher:
        """
        self.bind_address = bind_address  # type: tuple
        self.tcp_server = TCPServer(self.bind_address, dispatcher)  # type: TCPServer

    def run(self):
        """ Runs the TCP server. """
        server_thread = threading.Thread(target=self.tcp_server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def shutdown(self):
        """ Stops the TCP server. """
        self.tcp_server.shutdown()
        self.tcp_server.server_close()
