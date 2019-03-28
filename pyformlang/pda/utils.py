""" Useful functions for a PDA """

from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon

def to_state(given):
    """ Convert to a state """
    if isinstance(given, State):
        return given
    return State(given)

def to_symbol(given):
    """ Convert to a symbol """
    if isinstance(given, Symbol):
        return given
    if given == "epsilon":
        return Epsilon()
    return Symbol(given)

def to_stack_symbol(given):
    """ Convert to a stack symbol """
    if isinstance(given, StackSymbol):
        return given
    if isinstance(given, Epsilon):
        return given
    return StackSymbol(given)
