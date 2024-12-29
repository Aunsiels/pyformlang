"""
A nondeterministic transition function
"""

from typing import Dict, Set, Iterable, Tuple
from copy import deepcopy

from .state import State
from .symbol import Symbol
from .transition_function import TransitionFunction


class NondeterministicTransitionFunction(TransitionFunction):
    """ A nondeterministic transition function in a finite automaton.

    The difference with a deterministic transition is that the return value is
    a set of States

    Examples
    --------

    >>> transition = NondeterministicTransitionFunction()
    >>> transition.add_transition(State(0), Symbol("a"), State(1))

    Creates a transition function and adds a transition.

    """

    def __init__(self) -> None:
        self._transitions: Dict[State, Dict[Symbol, Set[State]]] = {}

    def add_transition(self,
                       s_from: State,
                       symb_by: Symbol,
                       s_to: State) -> int:
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

        Examples
        --------

        >>> transition = NondeterministicTransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))

        """
        if s_from in self._transitions:
            if symb_by in self._transitions[s_from]:
                self._transitions[s_from][symb_by].add(s_to)
            else:
                self._transitions[s_from][symb_by] = {s_to}
        else:
            self._transitions[s_from] = {}
            self._transitions[s_from][symb_by] = {s_to}
        return 1

    def remove_transition(self,
                          s_from: State,
                          symb_by: Symbol,
                          s_to: State) -> int:
        """ Removes a transition from the function

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

        Examples
        --------

        >>> transition = NondeterministicTransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))
        >>> transition.remove_transition(State(0), Symbol("a"), State(1))

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

        Examples
        --------

        >>> transition = NondeterministicTransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))
        >>> transition.get_number_transitions()
        1

        """
        counter = 0
        for transitions in self._transitions.values():
            for s_to in transitions.values():
                counter += len(s_to)
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
        s_from : set :class:`~pyformlang.finite_automaton.State`
            Set of destination states

        """
        if s_from in self._transitions:
            if symb_by in self._transitions[s_from]:
                return self._transitions[s_from][symb_by]
        return set()

    def get_transitions_from(self, s_from: State) \
            -> Iterable[Tuple[Symbol, State]]:
        """ Gets transitions from the given state """
        if s_from in self._transitions:
            for symb_by, states_to in self._transitions[s_from].items():
                for state_to in states_to:
                    yield symb_by, state_to

    def get_edges(self) -> Iterable[Tuple[State, Symbol, State]]:
        """ Gets the edges

        Returns
        ----------
        edges : generator of (:class:`~pyformlang.finite_automaton.State`, \
            :class:`~pyformlang.finite_automaton.Symbol`,\
            :class:`~pyformlang.finite_automaton.State`)
            A generator of edges
        """
        for s_from in self._transitions:
            for symb_by, s_to in self.get_transitions_from(s_from):
                yield s_from, symb_by, s_to

    def to_dict(self) -> Dict[State, Dict[Symbol, Set[State]]]:
        """
        Get the dictionary representation of the transition function. The keys
        of the dictionary are the source nodes. The items are dictionaries
        where the keys are the symbols of the transitions and the items are
        the set of target nodes.

        Returns
        -------
        transition_dict : dict
            The transitions as a dictionary.
        """
        return deepcopy(self._transitions)

    def is_deterministic(self) -> bool:
        """ Whether the transition function is deterministic

        Returns
        ----------
        is_deterministic : bool
            Whether the function is deterministic

        Examples
        --------

        >>> transition = NondeterministicTransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))
        >>> transition.is_deterministic()
        True

        """
        for transitions in self._transitions.values():
            for s_to in transitions.values():
                if len(s_to) > 1:
                    return False
        return True
