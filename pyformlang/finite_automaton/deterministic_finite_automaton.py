"""
Representation of a deterministic finite automaton
"""

from typing import AbstractSet, Iterable

from .state import State
from .symbol import Symbol
from .transition_function import TransitionFunction
from .nondeterministic_finite_automaton import NondeterministicFiniteAutomaton


class DeterministicFiniteAutomaton(NondeterministicFiniteAutomaton):
    """ Represents a deterministic finite automaton

    This class represents a deterministic finite automaton.

    Parameters
    ----------
    states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`, optional
        A finite set of input symbols
    transition_function : :class:`~pyformlang.finite_automaton.TransitionFunction`, optional
        Takes as arguments a state and an input symbol and returns a state.
    start_state : :class:`~pyformlang.finite_automaton.State`, optional
        A start state, element of states
    final_states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A set of final or accepting states. It is a subset of states.

    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 states: AbstractSet[State] = None,
                 input_symbols: AbstractSet[Symbol] = None,
                 transition_function: TransitionFunction = None,
                 start_state: State = None,
                 final_states: AbstractSet[State] = None):
        super().__init__(states, input_symbols, None, start_state, final_states)
        self._transition_function = transition_function or TransitionFunction()

    def accepts(self, word: Iterable[Symbol]) -> bool:
        """ Checks whether the dfa accepts a given word

        Parameters
        ----------
        word : iterable of :class:`~pyformlang.finite_automaton.Symbol`
            A sequence of input symbols

        Returns
        ----------
        is_accepted : bool
            Whether the word is accepted or not
        """
        current_state = self._start_state
        for symbol in word:
            if current_state is None:
                return False
            current_state = self._transition_function(current_state, symbol)
        return current_state is not None and self.is_final_state(current_state)
