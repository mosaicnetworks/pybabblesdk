from __future__ import print_function

__all__ = ['Proxy', 'AbstractState', 'AbstractService', 'Colours']
__version__ = '0.2.1'

import base64
import json
import sys
import threading

import requests

from pybabblesdk.blockchain import Block
from pybabblesdk.rpc.jsonrpctcpclient import JSONRPCTCPClient
from pybabblesdk.rpc.jsonrpctcpserver import Dispatcher
from pybabblesdk.rpc.jsonrpctcpserver import JSONRPCTCPServer

if sys.version_info < (3, 0):
    # noinspection PyUnresolvedReferences, PyCompatibility
    from Queue import Queue, Empty
else:
    # noinspection PyUnresolvedReferences, PyCompatibility
    from queue import Queue, Empty


# Module level variables
_queue = Queue()  # type: Queue
_print_lock = threading.Lock()


# noinspection PyClassHasNoInit
class Colours:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_COLOUR = '\033[0m'


class BaseHandler(Dispatcher):
    """ BaseHandler is initialized and destroyed per request back from the Babble node. """

    # noinspection PyPep8Naming, PyMethodMayBeStatic
    def CommitBlock(self, block):
        """ RPC sent from Babble node.

        :param block: the newly added block with transactions.
        :type block: dict
        """
        _queue.put(Block(block=block))


class AbstractState(object):
    __shutdown_request = False  # type: bool
    parse_queue_timeout = 0.5  # type: float
    __state = None

    def __init__(self):
        """ Describes the complete state of the app and all possible state transitions. """
        pass

    def _parse_block_queue(self):
        """ Parses the block queue if thread has not been stopped and queue is not empty. """
        try:
            while not self.__shutdown_request:
                try:
                    block = _queue.get(timeout=self.parse_queue_timeout)
                    self.commit_block(block)
                except Empty:
                    continue
        finally:
            self.__shutdown_request = False

    def commit_block(self, block):
        """ Abstract commit block method.

        :param block: block object from Babble node
        :type block: Block
        """
        raise NotImplementedError('commit_block: Implementation of this method is required.')

    def start(self):
        """ Run a separate thread to parse the block queue and update state. """
        state_thread = threading.Thread(target=self._parse_block_queue)
        state_thread.daemon = True
        state_thread.start()

    def shutdown(self):
        """ Shutdown state threading. """
        self.__shutdown_request = True

    @property
    def state(self):
        if type(self.__state) is None:
            raise TypeError('Must set default type of `state` in class initialisation.')
        return self.__state

    if type(__state) is None:
        @state.setter
        def state(self, value):
            self.__state = value


class Proxy(object):
    def __init__(self, node_address, bind_address):
        """ Proxy to build babble clients in python.

        :param node_address: the socket of the node
        :type node_address: tuple
        :param bind_address: the socket of the app
        :type bind_address: tuple
        """
        self.__node_address, self.__bind_address = node_address, bind_address  # type: tuple
        self.__rpc_client = JSONRPCTCPClient(self.__node_address)
        self.__rpc_server = JSONRPCTCPServer(self.__bind_address, BaseHandler)

    def run(self):
        """ Run the RPC server. """
        self.__rpc_server.run()

    def send_tx(self, tx):
        """ Send a transaction to the babble node. """
        if sys.version_info >= (3, 0):
            tx = tx.encode('ascii')
        tx_b64 = base64.b64encode(tx)
        self.__rpc_client.call("Babble.SubmitTx", [tx_b64], expect_reply=True)

    def shutdown(self):
        """ Stop the RPC server. """
        self.__rpc_server.shutdown()

    @property
    def stats(self):
        """ Returns node stats as python dictionary. """
        return json.loads((requests.get('http://{ip}:80/stats'.format(ip=self.__node_address[0]))).content)

    def get_block(self, block_uid):
        """ Gets block with unique id as python dictionary. """
        request = requests.get('http://{ip}:80/block/{uid}'.format(ip=self.__node_address[0], uid=block_uid))
        return Block(block=json.loads(request.content))


class AbstractService(object):
    def __init__(self, node, state_machine, debug=False):
        """ Abstract Service

        :param node: a proxy to the Babble node
        :type node: Proxy
        :param state_machine: an object describing the state of the app.
        :type state_machine: AbstractState
        :param debug: run app in debug mode
        :type debug: bool
        """
        self.__debug = debug
        self.__node = node
        self.__state = state_machine

    def service(self):
        raise NotImplementedError('service: Implementation of this method is required.')

    def start(self):
        """ Start application. """
        try:
            self._pre_start()
            self.service()
        except KeyboardInterrupt:
            self.stop()

    def _pre_start(self):
        self.__node.run()
        self.__state.start()
        self.debug_info('Service started.')

    def stop(self):
        """ Stop application. """
        self.__node.shutdown()
        self.__state.shutdown()
        self.debug_info('Service stopped.')

    def debug_info(self, message):
        """ Print message if DEBUG is set.

        :param message: the debug info message to print
        :type: str
        """
        if self.__debug:
            with _print_lock:
                print((Colours.HEADER + 'INFO: ' + Colours.END_COLOUR + message).strip())

    def debug_error(self, message):
        """ Error message if DEBUG is set.

        :param message: the debug error message to print
        :type: str
        """
        if self.__debug:
            with _print_lock:
                print((Colours.FAIL + 'ERROR: ' + Colours.END_COLOUR + message).strip())

    def debug_success(self, message):
        """ Success message if DEBUG is set.

        :param message: the debug success message to print
        :type: str
        """
        if self.__debug:
            with _print_lock:
                print((Colours.OK_GREEN + 'SUCCESS: ' + Colours.END_COLOUR + message).strip())

    @property
    def node(self):
        return self.__node

    @property
    def state_machine(self):
        return self.__state
