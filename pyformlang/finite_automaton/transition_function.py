"""
Repretation of a transition function
"""

from typing import List

from .state import State
from .symbol import Symbol


class TransitionFunction(object):
    """ A transition function in a finite automaton.

    This is a deterministic transition function.

    Parameters
    ----------

    Attributes
    ----------
    _transitions : dict
        A dictionary which contains the transitions of a finite automaton


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

        Raises
        --------
        DuplicateTransitionError
            If the transition already exists
        """
        if s_from in self._transitions:
            if symb_by in self._transitions[s_from]:
                if self._transitions[s_from][symb_by] != s_to:
                    raise DuplicateTransitionError(s_from,
                                                   symb_by,
                                                   s_to,
                                                   self._transitions[s_from][symb_by])
            else:
                self._transitions[s_from][symb_by] = s_to
        else:
            self._transitions[s_from] = dict()
            self._transitions[s_from][symb_by] = s_to
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
                s_to == self._transitions[s_from][symb_by]:
            del self._transitions[s_from][symb_by]
            return 1
        return 0

    def __call__(self, s_from: State, symb_by: Symbol) -> List[State]:
        """ Calls the transition function as a real function

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        symb_by : :class:`~pyformlang.finite_automaton.Symbol`
            The transition symbol

        Returns
        ----------
        s_from : list of :class:`~pyformlang.finite_automaton.State`
            The destination state, in a list

        """
        if s_from in self._transitions:
            if symb_by in self._transitions[s_from]:
                return [self._transitions[s_from][symb_by]]
        return []

    def get_number_transitions(self) -> int:
        """ Gives the number of transitions describe by the deterministic function

        Returns
        ----------
        n_transitions : int
            The number of deterministic transitions

        """
        counter = 0
        for s_from in self._transitions:
            counter += len(self._transitions[s_from])
        return counter

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
                yield (state, symbol, self._transitions[state][symbol])


class DuplicateTransitionError(Exception):
    """ Signals a duplicated transition

    Parameters
    ----------
    s_from : :class:`~pyformlang.finite_automaton.State`
        The source state
    symb_by : :class:`~pyformlang.finite_automaton.Symbol`
        The transition symbol
    s_to : :class:`~pyformlang.finite_automaton.State`
        The wanted new destination state
    s_to_old : :class:`~pyformlang.finite_automaton.State`
        The old destination state

    Attributes
    ----------
    message : str
        An error message summarising the information

    """

    def __init__(self,
                 s_from: State,
                 symb_by: Symbol,
                 s_to: State,
                 s_to_old: State):
        super().__init__("Transition from " + str(s_from) + \
            " by " + str(symb_by) +\
            " goes to " + str(s_to_old) + " not " + str(s_to))
        self.s_from = s_from
        self.symb_by = symb_by
        self.s_to = s_to
        self.s_to_old = s_to_old
