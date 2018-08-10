import sys


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
