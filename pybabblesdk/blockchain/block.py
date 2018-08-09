import base64


class Block(object):
    __slots__ = ['__index', '__round_received', '__state_hash', '__transactions', '__raw_transactions', '__signatures']

    def __init__(self, block):
        try:
            self.__index = block['Body']['Index']
            self.__round_received = block['Body']['RoundReceived']
            self.__state_hash = block['Body']['StateHash']
            self.__raw_transactions = block['Body']['Transactions']
            self.__transactions = [base64.b64decode(tx_b64) for tx_b64 in self.__raw_transactions]
            self.__signatures = block['Signatures']
        except IndexError as e:
            print(e)

    def to_dict(self):
        return dict(
            Body=dict(
                Index=self.index,
                RoundReceived=self.round_received,
                StateHash=self.state_hash,
                Transactions=self.raw_transactions
            ),
            Signatures=self.signatures
        )

    @property
    def index(self):
        return self.__index

    @property
    def round_received(self):
        return self.__round_received

    @property
    def state_hash(self):
        return self.__state_hash

    @property
    def transactions(self):
        return self.__transactions

    @property
    def raw_transactions(self):
        return self.__raw_transactions

    @property
    def signatures(self):
        return self.__signatures
