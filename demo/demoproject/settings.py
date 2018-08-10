import pybabblesdk

from sendmessage.state import State


# Request Handler
class Handler(pybabblesdk.StateMachine):

    # noinspection PyMethodMayBeStatic
    def commit_block(self, block):
        STATE.parse(block)


# Project level state variable
STATE = State()
