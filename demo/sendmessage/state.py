import json


class State:
    def __init__(self):
        pass

    def parse(self, block):
        self.print_block(block)

    @staticmethod
    def print_block(block):
        msg = '\033[F\r\033[92m' + 'Received block:\n'
        msg += json.dumps(block.to_dict(), indent=4, sort_keys=True) + '\033[0m\n'
        msg += 'Your message:'
        print(msg)
