""" We represent here a pushdown automaton """

from typing import AbstractSet, List

from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon
from .transition_function import TransitionFunction

class PDA(object):
    """ Representation of a pushdown automaton

    Parameters
    ----------
    states : set of :class:`~pyformlang.pda.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.pda.Symbol`, optional
        A finite set of input symbols
    stack_alphabet : set of :class:`~pyformlang.pda.StackSymbol`, optional
        A finite stack alphabet
    transition_function : :class:`~pyformlang.pda.TransitionFunction`, optional
        Takes as arguments a state, an input symbol and a stack symbol and returns \
            a state and a string of stack symbols push on the stacked to replace X
    start_state : :class:`~pyformlang.pda.State`, optional
        A start state, element of states
    start_stack_symbol : :class:`~pyformlang.pda.StackSymbol`, optional
        The stack is initialized with this stack symbol
    final_states : set of :class:`~pyformlang.pda.State`, optional
        A set of final or accepting states. It is a subset of states.
    """

    def __init__(self,
                 states: AbstractSet[State] = None,
                 input_symbols: AbstractSet[Symbol] = None,
                 stack_alphabet: AbstractSet[StackSymbol] = None,
                 transition_function: TransitionFunction = None,
                 start_state: State = None,
                 start_stack_symbol: StackSymbol = None,
                 final_states: AbstractSet[State] = None):
        self._states = states or set()
        self._input_symbols = input_symbols or set()
        self._stack_alphabet = stack_alphabet or set()
        self._transition_function = transition_function or TransitionFunction()
        self._start_state = start_state
        if start_state is not None:
            self._states.add(start_state)
        self._start_stack_symbol = start_stack_symbol
        if start_stack_symbol is not None:
            self._stack_alphabet.add(start_stack_symbol)
        self._final_states = final_states or set()
        for state in self._final_states:
            self._states.add(state)

    def get_number_states(self):
        """ Gets the number of states

        Returns
        ----------
        n_states : int
            The number of states
        """
        return len(self._states)

    def get_number_input_symbols(self):
        """ Gets the number of input symbols

        Returns
        ----------
        n_input_symbols : int
            The number of input symbols
        """
        return len(self._input_symbols)

    def get_number_stack_symbols(self):
        """ Gets the number of stack symbols

        Returns
        ----------
        n_stack_symbols : int
            The number of stack symbols
        """
        return len(self._stack_alphabet)

    def get_number_transitions(self):
        """ Gets the number of transitions in the PDA

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        return self._transition_function.get_number_transitions()

    def add_transition(self,
                       s_from: State,
                       input_symbol: Symbol,
                       stack_from: StackSymbol,
                       s_to: State,
                       stack_to: List[StackSymbol]):
        """ Add a transition to the PDA

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
        self._states.add(s_from)
        self._states.add(s_to)
        if input_symbol != Epsilon():
            self._input_symbols.add(input_symbol)
        self._stack_alphabet.add(stack_from)
        for stack_symbol in stack_to:
            self._stack_alphabet.add(stack_symbol)
        self._transition_function.add_transition(s_from,
                                                 input_symbol,
                                                 stack_from,
                                                 s_to,
                                                 stack_to)
