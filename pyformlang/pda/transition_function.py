""" A transition function in a pushdown automaton """

from typing import AbstractSet, List

from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol

class TransitionFunction(object):
    """ A transition function in a pushdown automaton """

    def __init__(self):
        self._transitions = dict()

    def get_number_transitions(self):
        """ Gets the number of transitions

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        res = 0
        for transition in self._transitions:
            res += len(self._transitions[transition])
        return res

    def add_transition(self,
                       s_from: State,
                       input_symbol: Symbol,
                       stack_from: StackSymbol,
                       s_to: State,
                       stack_to: List[StackSymbol]):
        """ Add a transition to the function

        Parameters
        ----------
        s_from : :class:`~pyformlang.pda.State`
            The starting symbol
        input_symbol : :class:`~pyformlang.pda.Symbol`
            The input symbol
        stack_from : :class:`~pyformlang.pda.StackSymbol`
            The stack symbol of the transition
        s_to : :class:`~pyformlang.pda.State`
            The new state
        stack_to : list of :class:`~pyformlang.pda.StackSymbol`
            The string of stack symbol which replace the stack_from
        """
        temp_in = (s_from, input_symbol, stack_from)
        temp_out = (s_to, tuple(stack_to))
        if temp_in in self._transitions:
            self._transitions[temp_in].add(temp_out)
        else:
            self._transitions[temp_in] = {temp_out}
