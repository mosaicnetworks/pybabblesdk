from __future__ import print_function

import argparse
import json

import pybabblesdk as babble_sdk


class StateMachine(babble_sdk.AbstractState):

    def __init__(self):
        # initiate parent class
        _ = super(StateMachine, self).__init__()
        # initiate state with default data structure.
        self.state = dict()

    def commit_block(self, block):
        # print block as received by Babble
        babble_sdk.success(json.dumps(block.to_dict_raw(), indent=4, sort_keys=True))


class Service(babble_sdk.AbstractService):
    def __init__(self, node, state_machine, debug):
        # initiate parent class
        _ = super(Service, self).__init__(node=node, state_machine=state_machine, debug=debug)

    def service(self):
        # service demo
        while True:
            # require user to type a message
            message = raw_input('Type a message to send: ')
            # send message to babble node
            if message:
                self.node.send_tx(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple PyBabble SDK Example')
    parser.add_argument('--nodehost', help='node hostname', type=str, default='172.77.5.1')
    parser.add_argument('--nodeport', help='node port number', type=int, default=1338)
    parser.add_argument('--listenhost', help='app listen hostname', type=str, default='172.77.5.5')
    parser.add_argument('--listenport', help='app listen port number', type=int, default=1339)
    args = parser.parse_args()

    babble_node_address = (args.nodehost, args.nodeport)
    app_bind_address = (args.listenhost, args.listenport)

    service = Service(
        node=babble_sdk.Proxy(node_address=babble_node_address, bind_address=app_bind_address),
        state_machine=StateMachine(),
        debug=True
    )
    service.start()
