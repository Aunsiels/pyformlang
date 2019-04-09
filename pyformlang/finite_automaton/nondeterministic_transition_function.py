"""
A nondeterministic transition function
"""

from typing import Set

from .state import State
from .symbol import Symbol


class NondeterministicTransitionFunction(object):
    """ A nondeterministic transition function in a finite automaton.

    The difference with a deterministic transition is that the return value is
    a set of States
    """

    def __init__(self):
        self._transitions = dict()

    def add_transition(self, s_from: State, symb_by: Symbol, s_to: State) -> int:
        """ Adds a new transition to the function

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        symb_by : :class:`~pyformlang.finite_automaton.Symbol`
            The transition symbol
        s_to : :class:`~pyformlang.finite_automaton.State`
            The destination state


        Returns
        --------
        done : int
            Always 1

        """
        if s_from in self._transitions:
            if symb_by in self._transitions[s_from]:
                self._transitions[s_from][symb_by].add(s_to)
            else:
                self._transitions[s_from][symb_by] = {s_to}
        else:
            self._transitions[s_from] = dict()
            self._transitions[s_from][symb_by] = {s_to}
        return 1

    def remove_transition(self, s_from: State, symb_by: Symbol, s_to: State) -> int:
        """ Removes a transition to the function

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        symb_by : :class:`~pyformlang.finite_automaton.Symbol`
            The transition symbol
        s_to : :class:`~pyformlang.finite_automaton.State`
            The destination state


        Returns
        --------
        done : int
            1 is the transition was found, 0 otherwise

        """
        if s_from in self._transitions and \
                symb_by in self._transitions[s_from] and \
                s_to in self._transitions[s_from][symb_by]:
            self._transitions[s_from][symb_by].remove(s_to)
            return 1
        return 0

    def get_number_transitions(self) -> int:
        """ Gives the number of transitions describe by the function

        Returns
        ----------
        n_transitions : int
            The number of transitions

        """
        counter = 0
        for s_from in self._transitions:
            for symb_by in self._transitions[s_from]:
                counter += len(self._transitions[s_from][symb_by])
        return counter

    def __call__(self, s_from: State, symb_by: Symbol) -> Set[State]:
        """ Calls the transition function as a real function

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        symb_by : :class:`~pyformlang.finite_automaton.Symbol`
            The transition symbol

        Returns
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State` or None
            The destination state or None if it does not exists

        """
        if s_from in self._transitions:
            if symb_by in self._transitions[s_from]:
                return self._transitions[s_from][symb_by]
        return set()

    def is_deterministic(self):
        """ Whether the transition function is deterministic

        Returns
        ----------
        is_deterministic : bool
            Whether the function is deterministic

        """
        for s_from in self._transitions:
            for symb in self._transitions[s_from]:
                if len(self._transitions[s_from][symb]) > 1:
                    return False
        return True

    def get_edges(self):
        """ Gets the edges

        Returns
        ----------
        edges : generator of (:class:`~pyformlang.finite_automaton.State`, \
            :class:`~pyformlang.finite_automaton.Symbol`,\
            :class:`~pyformlang.finite_automaton.State`)
            A generator of edges
        """
        for state in self._transitions:
            for symbol in self._transitions[state]:
                for next_state in self._transitions[state][symbol]:
                    yield (state, symbol, next_state)
