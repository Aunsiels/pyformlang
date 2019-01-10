"""
Representation of a nondeterministic finite automaton
"""

from typing import AbstractSet, Iterable

from .state import State
from .symbol import Symbol
from .nondeterministic_transition_function import NondeterministicTransitionFunction


class NondeterministicFiniteAutomaton(object):
    """ Represents a nondeterministic finite automaton

    This class represents a nondeterministic finite automaton.

    Parameters
    ----------
    states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`, optional
        A finite set of input symbols
    transition_function : :class:`~pyformlang.finite_automaton.NondeterministicTransitionFunction`, optional
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
                 transition_function: NondeterministicTransitionFunction = None,
                 start_state: State = None,
                 final_states: AbstractSet[State] = None):
        self._states = states or set()
        self._input_symbols = input_symbols or set()
        self._transition_function = transition_function or \
            NondeterministicTransitionFunction()
        self._start_state = start_state
        self._final_states = final_states or set()
        if start_state is not None and start_state not in self._states:
            self._states.add(start_state)
        for state in self._final_states:
            if state is not None and state not in self._states:
                self._states.add(start_state)

    def add_transition(self, s_from: State, symb_by: Symbol, s_to: State) -> int:
        """ Adds a transition to the nfa

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
        self._states.add(s_from)
        self._states.add(s_to)
        self._input_symbols.add(symb_by)
        return self._transition_function.add_transition(s_from, symb_by, s_to)

    def get_number_states(self) -> int:
        """ Gives the total number of states

        Returns
        ----------
        number_states : int
            The number of states
        """
        return len(self._states)

    def get_number_symbols(self) -> int:
        """ Gives the total number of symbols

        Returns
        ----------
        number_symbols : int
            The number of symbols
        """
        return len(self._input_symbols)

    def set_initial_state(self, state: State) -> int:
        """ Set the initial state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The new initial state

        Returns
        ----------
        done : int
            1 is correctly added
        """
        self._start_state = state
        self._states.add(state)
        return 1

    def add_final_state(self, state: State) -> int:
        """ Adds a new final state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            A new final state

        Returns
        ----------
        done : int
            1 is correctly added
        """
        self._final_states.add(state)
        self._states.add(state)
        return 1

    def remove_final_state(self, state: State) -> int:
        """ Remove a final state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            A final state to remove

        Returns
        ----------
        done : int
            0 if it was not a final state, 1 otherwise
        """
        if self.is_final_state(state):
            self._final_states.remove(state)
            return 1
        return 0

    def is_final_state(self, state: State) -> bool:
        """ Checks if a state is final

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The state to check

        Returns
        ----------
        is_final : bool
            Whether the state is final or not
        """
        return state in self._final_states

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
        current_states = {self._start_state}
        for symbol in word:
            next_states = set()
            for current_state in current_states:
                next_states_temp = self._transition_function(current_state,
                                                             symbol)
                next_states = next_states.union(next_states_temp)
            current_states = next_states
        return any([self.is_final_state(x) for x in current_states])
