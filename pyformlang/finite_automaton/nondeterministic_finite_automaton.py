"""
Representation of a nondeterministic finite automaton
"""

from typing import Iterable

from .symbol import Symbol
from .epsilon_nfa import EpsilonNFA
from .finite_automaton import to_state, to_symbol


class NondeterministicFiniteAutomaton(EpsilonNFA):
    """ Represents a nondeterministic finite automaton

    This class represents a nondeterministic finite automaton.

    Parameters
    ----------
    states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`, optional
        A finite set of input symbols
    transition_function : :class:`~pyformlang.finite_automaton.NondeterministicTransitionFunction`\
        , optional
        Takes as arguments a state and an input symbol and returns a state.
    start_state : :class:`~pyformlang.finite_automaton.State`, optional
        A start state, element of states
    final_states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A set of final or accepting states. It is a subset of states.
    """

    def accepts(self, word: Iterable[Symbol]) -> bool:
        """ Checks whether the nfa accepts a given word

        Parameters
        ----------
        word : iterable of :class:`~pyformlang.finite_automaton.Symbol`
            A sequence of input symbols

        Returns
        ----------
        is_accepted : bool
            Whether the word is accepted or not
        """
        word = [to_symbol(x) for x in word]
        current_states = self._start_state
        for symbol in word:
            current_states = self._get_next_states_iterable(current_states,
                                                            symbol)
        return any([self.is_final_state(x) for x in current_states])

    def is_deterministic(self) -> bool:
        """ Checks whether an automaton is deterministic

        Returns
        ----------
        is_deterministic : bool
           Whether the automaton is deterministic
        """
        return len(self._start_state) <= 1 and \
            self._transition_function.is_deterministic()

    def to_deterministic(self) -> "DeterministicFiniteAutomaton":
        """ Transforms the nfa into a dfa

        Returns
        ----------
        dfa : :class:`~pyformlang.deterministic_finite_automaton.DeterministicFiniteAutomaton`
            A dfa equivalent to the current nfa
        """
        return self._to_deterministic_internal(False)
