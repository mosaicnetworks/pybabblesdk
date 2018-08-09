import json
import socket
import sys

import six


class JSONRPCTCPClient(object):
    __id_counter = 0  # type: int

    def __init__(self, endpoint):
        """ Provides the connection to the Babble node.

        :param endpoint: the babble node's ip and port
        :type endpoint: tuple(ip:str, port:int)
        """
        self.__endpoint = endpoint  # type: tuple

    def call(self, method, args, expect_reply=False):
        """ Call a function on the Babble node.

        :param method: method to call on the babble node
        :type method: str
        :param args: list of arguments to be passed into the remote procedure `method`
        :type args: list
        :param expect_reply: whether reply is required
        :type expect_reply: bool
        :return: success or failure
        :rtype: int
        """
        message = self._create_message(method, args)

        if sys.version_info >= (3, 0):
            message = bytes(message, encoding='ascii')

        reply = self._send_message(message, True)

        if expect_reply:
            self._parse_reply(reply)
            return 0
        else:
            return 0

    def _create_message(self, method, args):
        """ Creates a dictionary with the method, arguments and an id in the format Babble accepts.

        :param method: name of the remote procedure
        :type method: str
        :param args: list of arguments for the remote procedure
        :type args: list
        :return: str version of json
        :rtype: str
        """
        if sys.version_info >= (3, 0):
            args = [str(arg, encoding='ascii') for arg in args]

        return json.dumps(dict(method=method,
                               params=args,
                               unique_id=six.next(self._uid())))

    def _uid(self):
        """ Generates a unique ID for each tx. """
        while True:
            self.__id_counter += 1
            yield self.__id_counter

    def _parse_reply(self, reply):
        pass

    def _send_message(self, message, expect_reply=False):
        """ Send message to Babble node and get reply.

        :param message: the tx details.
        :type message: bytes
        :param expect_reply: whether reply is required
        :type expect_reply: bool
        :return: data
        """
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
