"""
Nondeterminsitic Automaton with epsilon transitions
"""

from typing import Set, Iterable

from .nondeterministic_finite_automaton import NondeterministicFiniteAutomaton
from .epsilon import Epsilon
from .state import State
from .symbol import Symbol


class EpsilonNFA(NondeterministicFiniteAutomaton):
    """ Represents an epsilon NFA


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
        """ Checks whether the epsilon nfa accepts a given word

        Parameters
        ----------
        word : iterable of :class:`~pyformlang.finite_automaton.Symbol`
            A sequence of input symbols

        Returns
        ----------
        is_accepted : bool
            Whether the word is accepted or not
        """
        current_states = self.eclose_iterable(self._start_state)
        for symbol in word:
            if symbol == Epsilon():
                continue
            next_states = self._get_next_states_iterable(current_states, symbol)
            current_states = self.eclose_iterable(next_states)
        return any([self.is_final_state(x) for x in current_states])

    def eclose_iterable(self, states: Iterable[State]) -> Set[State]:
        """ Compute the epsilon closure of a collection of states

        Parameters
        ----------
        state : iterable of :class:`~pyformlang.finite_automaton.State`
            The source states

        Returns
        ---------
        states : set of :class:`~pyformlang.finite_automaton.State`
            The epsilon closure of the source state
        """
        res = set()
        for state in states:
            res = res.union(self.eclose(state))
        return res

    def eclose(self, state: State) -> Set[State]:
        """ Compute the epsilon closure of a state

        Parameters
        ----------
        state : :class:`~pyformlang.finite_automaton.State`
            The source state

        Returns
        ---------
        states : set of :class:`~pyformlang.finite_automaton.State`
            The epsilon closure of the source state
        """
        to_process = [state]
        processed = {state}
        while to_process:
            current = to_process.pop()
            connected = self._transition_function(current, Epsilon())
            for conn_state in connected:
                if conn_state not in processed:
                    processed.add(conn_state)
                    to_process.append(conn_state)
        return processed
