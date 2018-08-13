from __future__ import print_function

import argparse
import json
import sys

from pybabblesdk import BabbleProxy, State


class StateMachine(object, State):
    # The interval to check for new blocks in Queue
    __timeout = 0.5

    def __init__(self):
        _ = super(StateMachine, self).__init__()

    # Handles logic of parsing a block (REQUIRED)
    def commit_block(self, block):
        msg = '\033[F\r\033[92m' + 'Received block:\n'
        msg += json.dumps(block.to_dict(), indent=4, sort_keys=True) + '\033[0m\n'
        msg += 'Your message:'
        print(msg)


class Service(object):
    def __init__(self, node):
        self.babble_node = node

    def run(self):
        try:
            while True:
                message = raw_input('Your message: \n')
                if message:
                    self.babble_node.send_tx(message)
        except KeyboardInterrupt as e:
            print(e)
            self.babble_node.shutdown()
            sys.exit(0)


def app(node_address, bind_address):
    babble_node = BabbleProxy(node_address=node_address, bind_address=bind_address, state=StateMachine())
    service = Service(babble_node)

    babble_node.run()
    service.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple PyBabble SDK Example')
    parser.add_argument('--nodehost', help='node hostname', type=str, default='172.77.5.1')
    parser.add_argument('--nodeport', help='node port number', type=int, default=1338)
    parser.add_argument('--listenhost', help='app listen hostname', type=str, default='172.77.5.5')
    parser.add_argument('--listenport', help='app listen port number', type=int, default=1339)
    args = parser.parse_args()

    babble_node_address = (args.nodehost, args.nodeport)
    app_bind_address = (args.listenhost, args.listenport)

    app(babble_node_address, app_bind_address)
