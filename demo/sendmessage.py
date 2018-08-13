from __future__ import print_function

import argparse
import json

from pybabblesdk import *


class State(AbstractState):

    def __init__(self):
        _ = super(State, self).__init__()

    def commit_block(self, block):
        msg = '\033[F\r\033[92m' + 'Received block:\n'
        msg += json.dumps(block.to_dict_raw(), indent=4, sort_keys=True) + '\033[0m\n'
        msg += 'Your message:'
        print(msg)


class Service(AbstractService):
    def __init__(self, node):
        _ = super(Service, self).__init__(node=node)

    def start(self):
        while True:
            message = raw_input('Your message: \n')
            if message:
                self.node.send_tx(message)

    def stop(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple PyBabble SDK Example')
    parser.add_argument('--nodehost', help='node hostname', type=str, default='172.77.5.1')
    parser.add_argument('--nodeport', help='node port number', type=int, default=1338)
    parser.add_argument('--listenhost', help='app listen hostname', type=str, default='172.77.5.5')
    parser.add_argument('--listenport', help='app listen port number', type=int, default=1339)
    args = parser.parse_args()

    babble_node_address = (args.nodehost, args.nodeport)
    app_bind_address = (args.listenhost, args.listenport)

    app = App(
        service=Service(Proxy(node_address=babble_node_address, bind_address=app_bind_address)),
        state=State(),
        debug=True
    )
    app.start()
