import base64

from rpc.jsonrpctcpclient import JSONRPCTCPClient
from rpc.jsonrpctcpserver import JSONRPCTCPServer, Dispatcher


class StateMachine(Dispatcher):

    def CommitBlock(self, block):
        self.commit_block(block)

    def commit_block(self, block):
        pass


class BabbleProxy(object):

    def __init__(self, node_address, bind_address, state_machine):
        self.__node_address = node_address
        self.__bind_address = bind_address
        self.__state_machine = state_machine

        self.__rpc_client = JSONRPCTCPClient(self.__node_address)
        self.__rpc_server = JSONRPCTCPServer(self.__bind_address, self.__state_machine)

    def run(self):
        self.__rpc_server.run()

    def send_tx(self, tx):
        tx_b64 = base64.b64encode(tx)
        self.__rpc_client.call("Babble.SubmitTx", [tx_b64], expect_reply=True)

    def shutdown(self):
        self.__rpc_server.shutdown()
