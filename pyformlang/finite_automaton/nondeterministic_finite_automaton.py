"""
Representation of a nondeterministic finite automaton
"""

from typing import AbstractSet, Iterable, Set

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
    transition_function : :class:`~pyformlang.finite_automaton.NondeterministicTransitionFunction`
, optional
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
                 start_state: AbstractSet[State] = None,
                 final_states: AbstractSet[State] = None):
        self._states = states or set()
        self._input_symbols = input_symbols or set()
        self._transition_function = transition_function or \
            NondeterministicTransitionFunction()
        self._start_state = start_state or set()
        self._final_states = final_states or set()
        for state in self._final_states:
            if state is not None and state not in self._states:
                self._states.add(start_state)
        for state in self._start_state:
            if state is not None and state not in self._states:
                self._states.add(state)

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

    def get_number_transitions(self) -> int:
        """ Gives the number of transitions

        Returns
        ----------
        n_transitions : int
            The number of deterministic transitions

        """
        return self._transition_function.get_number_transitions()

    def get_number_symbols(self) -> int:
        """ Gives the total number of symbols

        Returns
        ----------
        number_symbols : int
            The number of symbols
        """
        return len(self._input_symbols)

    def add_start_state(self, state: State) -> int:
        """ Set an initial state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The new initial state

        Returns
        ----------
        done : int
            1 is correctly added
        """
        self._start_state.add(state)
        self._states.add(state)
        return 1

    def remove_start_state(self, state: State) -> int:
        """ remove an initial state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The new initial state

        Returns
        ----------
        done : int
            1 is correctly added
        """
        if state in self._start_state:
            self._start_state.remove(state)
            return 1
        return 0

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

    def _get_next_states_iterable(self,
                                  current_states: Iterable[State],
                                  symbol: Symbol) \
            -> Set[State]:
        """ Gives the set of next states, starting from a set of states

        Parameters
        ----------
        current_states : iterable of :class:`~pyformlang.finite_automaton.State`
            The considered list of states
        symbol : Symbol
            The symbol of the link

        Returns
        ----------
        next_states : set of :class:`~pyformlang.finite_automaton.State`
            The next of resulting states
        """
        next_states = set()
        for current_state in current_states:
            next_states_temp = self._transition_function(current_state,
                                                         symbol)
            next_states = next_states.union(next_states_temp)
        return next_states

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
        # pylint: disable=cyclic-import
        from .deterministic_finite_automaton import DeterministicFiniteAutomaton
        dfa = DeterministicFiniteAutomaton()
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
