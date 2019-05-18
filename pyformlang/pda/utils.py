""" Useful functions for a PDA """

from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon

class PDAObjectCreator(object):

    def __init__(self):
        self._state_creator = dict()
        self._symbol_creator = dict()
        self._stack_symbol_creator = dict()

    def to_state(self, given):
        """ Convert to a state """
        if isinstance(given, State):
            return get_object_from_known(given, self._state_creator)
        return get_object_from_raw(given, self._state_creator, State)

    def to_symbol(self, given):
        """ Convert to a symbol """
        if isinstance(given, Symbol):
            return get_object_from_known(given, self._symbol_creator)
        if given == "epsilon":
            return Epsilon()
        return get_object_from_raw(given, self._symbol_creator, Symbol)

    def to_stack_symbol(self, given):
        """ Convert to a stack symbol """
        if isinstance(given, StackSymbol):
            return get_object_from_known(given,
                                         self._stack_symbol_creator)
        if isinstance(given, Epsilon):
            return given
        return get_object_from_raw(given,
                                   self._stack_symbol_creator,
                                   StackSymbol)

def get_object_from_known(given, obj_converter):
    if given.get_value() in obj_converter:
        return obj_converter[given.get_value()]
    obj_converter[given.get_value()] = given
    return given

def get_object_from_raw(given, obj_converter, to_type):
    if given in obj_converter:
        return obj_converter[given]
    temp = to_type(given)
    obj_converter[given] = temp
    return temp
