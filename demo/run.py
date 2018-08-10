from __future__ import print_function

import argparse

import demoproject.settings as settings
from pybabblesdk import BabbleProxy
from sendmessage.service import Service
from sendmessage.state import State

if __name__ == '__main__':
    state = State()

    parser = argparse.ArgumentParser(description='Simple PyBabble SDK Example')
    parser.add_argument('--nodehost', help='node hostname', type=str, default='172.77.5.1')
    parser.add_argument('--nodeport', help='node port number', type=int, default=1338)
    parser.add_argument('--listenhost', help='app listen hostname', type=str, default='172.77.5.5')
    parser.add_argument('--listenport', help='app listen port number', type=int, default=1339)
    args = parser.parse_args()

    babble_node_address = (args.nodehost, args.nodeport)
    bind_address = (args.listenhost, args.listenport)

    babble_node = BabbleProxy(babble_node_address, bind_address, state_machine=settings.Handler)
    service = Service(babble_node)
    babble_node.run()
    service.run()
