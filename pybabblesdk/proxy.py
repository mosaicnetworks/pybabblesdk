import base64

from .rpc.jsonrpctcpclient import JSONRPCTCPClient
from .rpc.jsonrpctcpserver import JSONRPCTCPServer, Dispatcher


class StateMachine(Dispatcher):

    def commit_block(self, block):
        pass


class BabbleProxy(object):

    def __init__(self, node_address, bind_address, state_machine):
        self.node_address = node_address
        self.bind_address = bind_address
        self.state_machine = state_machine

        self.rpc_client = JSONRPCTCPClient(self.node_address)
        self.rpc_server = JSONRPCTCPServer(self.bind_address, self.state_machine)

    def run(self):
        self.rpc_server.run()

    def send_tx(self, tx):
        tx_b64 = base64.b64encode(tx)
        self.rpc_client.call("Babble.SubmitTx", [tx_b64], True)

    def shutdown(self):
        self.rpc_server.shutdown()
