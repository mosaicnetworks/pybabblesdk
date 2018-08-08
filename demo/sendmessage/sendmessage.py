from __future__ import print_function

import argparse
import json
import sys

import pybabblesdk


class StateMachine(pybabblesdk.StateMachine):

    def commit_block(self, block):
        msg = '\033[F\r\033[92m' + 'Received block:\n'
        msg += json.dumps(block, indent=4, sort_keys=True) + '\033[0m\n'
        msg += 'Your message:'
        print(msg)


class Service(object):
    def __init__(self, babble_node):
        self.babble_node = babble_node

    def run(self):
        try:
            while True:
                message = raw_input('Your message: \n')
                if message:
                    self.babble_node.send_tx(message)
        except KeyboardInterrupt:
            self.babble_node.shutdown()
            sys.exit(0)


def app(babble_node_addr, bind_addr):
    babble_node = pybabblesdk.BabbleProxy(babble_node_addr, bind_addr, StateMachine)
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
    bind_address = (args.listenhost, args.listenport)

    app(babble_node_address, bind_address)
