import json
import socket

import six


class JSONRPCTCPClient(object):

    def __init__(self, endpoint):
        self.__endpoint = endpoint  # type: str
        self.__id_counter = 0  # type: int

    def call(self, method, args, expect_reply=False):
        message = self._create_message(method, args)
        reply = self._send_message(message, True)

        if expect_reply:
            self._parse_reply(reply)
            return 0
        else:
            return 0

    def _create_message(self, method, args):
        json_data = dict(method=method, params=args, unique_id=self._uid().next())
        return json.dumps(json_data)

    def _uid(self):
        while True:
            self.__id_counter += 1
            yield self.__id_counter

    def _parse_reply(self, reply):
        pass

    def _send_message(self, message, expect_reply=False):
        if not isinstance(message, six.binary_type):
            raise TypeError('Bytes expected')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.__endpoint)

        s.sendall(message)
        data = s.recv(1024)

        s.close()

        if expect_reply:
            return data
        else:
            return 0
