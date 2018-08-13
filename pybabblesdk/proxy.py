from __future__ import print_function

import base64
import sys
import threading
import time
from Queue import Queue

from pybabblesdk.blockchain.block import Block
from pybabblesdk.rpc.jsonrpctcpclient import JSONRPCTCPClient
from pybabblesdk.rpc.jsonrpctcpserver import JSONRPCTCPServer, Dispatcher

block_queue = Queue()


class BaseHandler(Dispatcher):
    """ Abstract class to be extended or overridden by app developer. """

    # noinspection PyPep8Naming
    @staticmethod
    def CommitBlock(block):
        """ Describes what to do with the block received from Babble node.

        :param block: data sent from the babble node
        :type block: dict
        """
        block_queue.put(Block(block=block))


class State:
    __shutdown_request = False
    __timeout = 1

    def __init__(self):
        pass

    def _parse_block_queue(self):
        try:
            while not self.__shutdown_request:
                time.sleep(self.__timeout)
                while not block_queue.empty():
                    self.commit_block(block_queue.get())
        finally:
            self.__shutdown_request = False

    def commit_block(self, block):
        pass

    def _run(self):
        state_thread = threading.Thread(target=self._parse_block_queue)
        state_thread.daemon = True
        state_thread.start()

    def _shutdown(self):
        self.__shutdown_request = True


class BabbleProxy(object):

    def __init__(self, node_address, bind_address, state):
        """ Proxy to build babble clients in python.

        :param node_address: a tuple representing the socket of the node
        :type node_address: tuple
        :param bind_address: a tuple representing the socket where the application is listening
        :type bind_address: tuple
        :param state: a state class portraying the current state of the node
        :type state: State
        """
        self.__node_address, self.__bind_address = node_address, bind_address  # type: tuple
        self.state = state
        self.__rpc_client = JSONRPCTCPClient(self.__node_address)  # type: JSONRPCTCPClient
        self.__rpc_server = JSONRPCTCPServer(self.__bind_address, BaseHandler)  # type: JSONRPCTCPServer

    def run(self):
        """ Run the RPC server. """
        self.__rpc_server.run()
        self.state._run()

    def send_tx(self, tx):
        """ Send a transaction to the babble node. """
        if sys.version_info >= (3, 0):
            tx = tx.encode('ascii')
        tx_b64 = base64.b64encode(tx)
        self.__rpc_client.call("Babble.SubmitTx", [tx_b64], expect_reply=True)

    def shutdown(self):
        """ Stop the RPC server. """
        print('Stopping JSONRPCTCPServer thread...')
        self.__rpc_server.shutdown()
        print('Stopping State thread...')
        self.state._shutdown()
