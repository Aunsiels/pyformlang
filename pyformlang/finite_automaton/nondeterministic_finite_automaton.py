"""
Representation of a nondeterministic finite automaton
"""

from typing import Iterable

from pyformlang import finite_automaton

from .state import State
from .symbol import Symbol
from .epsilon_nfa import EpsilonNFA


class NondeterministicFiniteAutomaton(EpsilonNFA):
    """ Represents a nondeterministic finite automaton

    This class represents a nondeterministic finite automaton.

    Parameters
    ----------
    states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`, optional
        A finite set of input symbols
    transition_function : :class:`~pyformlang.finite_automaton.NondeterministicTransitionFunction`
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

    def to_deterministic(self):
        """ Transforms the nfa into a dfa

        Returns
        ----------
        dfa : :class:`~pyformlang.deterministic_finite_automaton.DeterministicFiniteAutomaton`
            A dfa equivalent to the current nfa
        """
        dfa = finite_automaton.DeterministicFiniteAutomaton()
        start_state = to_single_state(self._start_state)
        dfa.add_start_state(start_state)
        to_process = [self._start_state]
        processed = {start_state}
        while to_process:
            current = to_process.pop()
            s_from = to_single_state(current)
            print("Process", s_from)
            for symb in self._input_symbols:
                print("SYMB", symb)
                all_trans = [self._transition_function(x, symb) for x in current]
                state = set()
                for trans in all_trans:
                    state = state.union(trans)
                state_merged = to_single_state(state)
                print("Merged", state_merged)
                dfa.add_transition(s_from, symb, state_merged)
                if state_merged not in processed:
                    processed.add(state_merged)
                    to_process.append(state)
            for state in current:
                if state in self._final_states:
                    dfa.add_final_state(s_from)
        return dfa

def to_single_state(l_states: Iterable[State]) -> State:
    """ Merge a list of states

    Parameters
    ----------
    l_states : list of :class:`~pyformlang.finite_automaton.State`
        A list of states

    Returns
    ----------
    state : :class:`~pyformlang.finite_automaton.State`
        The merged state
    """
    values = []
    for state in l_states:
        values.append(str(state.get_value()))
    values = sorted(values)
    return State("; ".join(values))
