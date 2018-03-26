import six
import socket
import json

class JSONRPCTCPClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.id_counter = 0

    def call(self, method, args, expect_reply=False):
        message = self._create_message(method, args)
        reply = self._send_message(message, True)
        
        if expect_reply:
            self._parse_reply(reply)
            return 0
        else:
            return 0

    def _create_message(self, method, args):

        jdata = {"method": method, "params": args, "unique_id":self._get_uid()}

        return json.dumps(jdata)

    def _get_uid(self):
        self.id_counter += 1
        return self.id_counter

    def _parse_reply(self, reply):
        return 0

    def _send_message(self, message, expect_reply=False):
        if not isinstance(message, six.binary_type):
            raise TypeError('bytes expected')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect(self.endpoint)

        s.sendall(message)
        data = s.recv(1024)
        s.close()

        if expect_reply:
            return data
        else:
            return 0