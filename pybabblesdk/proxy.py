import base64
import sys

from pybabblesdk.blockchain.block import Block
from pybabblesdk.rpc.jsonrpctcpclient import JSONRPCTCPClient
from pybabblesdk.rpc.jsonrpctcpserver import JSONRPCTCPServer, Dispatcher


class StateMachine(Dispatcher):
    """ Abstract class to be extended or overridden by app developer. """

    def CommitBlock(self, block):
        """ Describes what to do with the block received from Babble node.

        :param block: data sent from the babble node
        :type block: dict
        """
        block_obj = Block(block=block)  # type: Block
        self.commit_block(block_obj)

    def commit_block(self, block):
        """ Describes what to do with the block received from Babble node.

        :param block: data sent from the babble node
        :type block: Block
        """
        pass


class BabbleProxy(object):

    def __init__(self, node_address, bind_address, state_machine):
        """ Proxy to build babble clients in python.

        :param node_address: a tuple representing the socket of the node
        :type node_address: tuple(ip:str, port:int)
        :param bind_address: a tuple representing the socket where the application is listening
        :type bind_address: tuple(ip:str, port:int)
        :param state_machine: a class describing the app
        :type: Dispatcher
        """
        self.__node_address, self.__bind_address = node_address, bind_address  # type: tuple
        self.__state_machine = state_machine  # type: Dispatcher

        self.__rpc_client = JSONRPCTCPClient(self.__node_address)  # type: JSONRPCTCPClient
        self.__rpc_server = JSONRPCTCPServer(self.__bind_address, self.__state_machine)  # type: JSONRPCTCPServer

    def run(self):
        """ Run the RPC server. """
        self.__rpc_server.run()

    def send_tx(self, tx):
        """ Send a transaction to the babble node. """
        if sys.version_info < (3, 0):
            tx_b64 = base64.b64encode(tx)
        else:
            tx_b64 = base64.b64encode(tx.encode('ascii'))
        self.__rpc_client.call("Babble.SubmitTx", [tx_b64], expect_reply=True)

    def shutdown(self):
        """ Stop the RPC server. """
        self.__rpc_server.shutdown()
