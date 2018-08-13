from __future__ import print_function

import base64
import sys
import threading
import time
from Queue import Queue

from pybabblesdk.blockchain import Block
from pybabblesdk.rpc.jsonrpctcpclient import JSONRPCTCPClient
from pybabblesdk.rpc.jsonrpctcpserver import Dispatcher
from pybabblesdk.rpc.jsonrpctcpserver import JSONRPCTCPServer

__all__ = ['App', 'Proxy', 'AbstractState', 'AbstractService']
__version__ = '0.1.11'

# Module level variables
DEBUG = False  # type: bool
QUEUE = Queue()  # type: Queue


def _debug_print(message):
    """ Print message if DEBUG is set.

    :param message: the debug message to print
    :type: str
    """
    if DEBUG:
        print(message)


class BaseHandler(Dispatcher):
    """ BaseHandler is initialized and destroyed per request back from the Babble node. """

    # noinspection PyPep8Naming, PyMethodMayBeStatic
    def CommitBlock(self, block):
        """ RPC sent from Babble node.

        :param block: the newly added block with transactions.
        :type block: dict
        """
        QUEUE.put(Block(block=block))


class AbstractState(object):
    __shutdown_request = False  # type: bool
    parse_queue_timeout = 0.5  # type: float

    def __init__(self):
        """ Describes the complete state of the app and all possible state transitions. """
        pass

    def _parse_block_queue(self):
        """ Parses the block queue if thread has not been stopped and queue is not empty. """
        try:
            while not self.__shutdown_request:
                time.sleep(self.parse_queue_timeout)
                _debug_print('Checking QUEUE...')
                while not QUEUE.empty():
                    _debug_print('Block(s) found.')
                    self.commit_block(QUEUE.get())
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
        _debug_print('Stopping State thread...')
        self.__shutdown_request = True


class AbstractService(object):
    def __init__(self, node):
        """ Abstract Service

        :param node: a proxy to the Babble node
        :type node: Proxy
        """
        self.__node = node

    def start(self):
        """ Abstract start method. """
        raise NotImplementedError('start: Implementation of this method is required.')

    def stop(self):
        """ Abstract stop method. """
        raise NotImplementedError('stop: Implementation of this method is required.')

    @property
    def node(self):
        return self.__node


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
        _debug_print('Stopping JSONRPCTCPServer thread...')
        self.__rpc_server.shutdown()


class App(object):
    def __init__(self, service, state, debug=False):
        """ Container for Babble applications.

        :param service: defines all actions the app can take.
        :type service: AbstractService
        :param state: an object describing the state of the app.
        :type state: AbstractState
        :param debug: run app in debug mode
        :type debug: bool
        """
        global DEBUG
        DEBUG = debug

        self.__state = state
        self.__service = service

    def start(self):
        """ Start application. """
        try:
            self.__service.node.run()
            self.__state.start()
            self.__service.start()
            _debug_print('App started.')
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """ Stop application. """
        self.__service.node.shutdown()
        self.__state.shutdown()
        self.__service.stop()
        _debug_print('App stopped.')
