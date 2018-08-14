from __future__ import print_function

import base64
import sys
import threading

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

__all__ = ['Proxy', 'AbstractState', 'AbstractService', 'Colours', 'debug_print', 'error', 'success']
__version__ = '0.2.1'

# Module level variables
DEBUG = False  # type: bool
QUEUE = Queue()  # type: Queue
print_lock = threading.Lock()


# noinspection PyClassHasNoInit
class Colours:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_COLOUR = '\033[0m'


def debug_print(message):
    """ Print message if DEBUG is set.

    :param message: the debug message to print
    :type: str
    """
    if DEBUG:
        with print_lock:
            print((Colours.HEADER + 'DEBUG: ' + Colours.END_COLOUR + message).strip())


def error(message):
    """ Error message if DEBUG is set.

    :param message: the debug message to print
    :type: str
    """
    if DEBUG:
        with print_lock:
            print((Colours.FAIL + 'ERROR: ' + Colours.END_COLOUR + message).strip())


def success(message):
    """ Success message if DEBUG is set.

    :param message: the debug message to print
    :type: str
    """
    if DEBUG:
        with print_lock:
            print((Colours.OK_GREEN + 'SUCCESS: ' + Colours.END_COLOUR + message).strip())


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
    __state = None

    def __init__(self):
        """ Describes the complete state of the app and all possible state transitions. """
        pass

    def _parse_block_queue(self):
        """ Parses the block queue if thread has not been stopped and queue is not empty. """
        try:
            while not self.__shutdown_request:
                try:
                    block = QUEUE.get(timeout=self.parse_queue_timeout)
                    debug_print('Block(s) found.')
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
        debug_print('Stopping State thread...')
        self.__shutdown_request = True

    @property
    def state(self):
        if type(self.__state) is None:
            raise TypeError('Must set default type of `state` in class initialisation.')
        return self.__state

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
        debug_print('Stopping JSONRPCTCPServer thread...')
        self.__rpc_server.shutdown()

    @property
    def stats(self):
        return self.__rpc_client.get_stats()

    def get_block(self):
        return self.__rpc_client.get_block(id)


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
        global DEBUG
        DEBUG = debug

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
        debug_print('Service started.')

    def stop(self):
        """ Stop application. """
        self.__node.shutdown()
        self.__state.shutdown()
        debug_print('Service stopped.')

    @property
    def node(self):
        return self.__node

    @property
    def state_machine(self):
        return self.__state
