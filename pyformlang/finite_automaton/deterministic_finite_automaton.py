"""
Representation of a deterministic finite automaton
"""

from typing import AbstractSet, Iterable
from collections import deque
from itertools import product

from .state import State
from .symbol import Symbol
from .transition_function import TransitionFunction
from .nondeterministic_finite_automaton import NondeterministicFiniteAutomaton
from .epsilon_nfa import to_single_state
from .finite_automaton import to_state, to_symbol
from .distinguishable_states import DistinguishableStates


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
        super().__init__(states, input_symbols, None, None, final_states)
        start_state = to_state(start_state)
        self._transition_function = transition_function or TransitionFunction()
        if start_state is not None:
            self._start_state = {start_state}
        else:
            self._start_state = {}
        if start_state is not None:
            self._states.add(start_state)

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
        state = to_state(state)
        self._start_state = {state}
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
        state = to_state(state)
        if {state} == self._start_state:
            self._start_state = {}
            return 1
        return 0

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
        word = [to_symbol(x) for x in word]
        current_state = None
        if self._start_state:
            current_state = list(self._start_state)[0]
        for symbol in word:
            if current_state is None:
                return False
            current_state = self._transition_function(current_state, symbol)
            if current_state:
                current_state = current_state[0]
            else:
                current_state = None
        return current_state is not None and self.is_final_state(current_state)

    def is_deterministic(self) -> bool:
        """ Checks whether an automaton is deterministic

        Returns
        ----------
        is_deterministic : bool
           Whether the automaton is deterministic
        """
        return True

    def to_deterministic(self) -> "DeterministicFiniteAutomaton":
        """ Transforms the nfa into a dfa

        Returns
        ----------
        dfa : :class:`~pyformlang.deterministic_finite_automaton.DeterministicFiniteAutomaton`
            A dfa equivalent to the current nfa
        """
        return self

    def copy(self) -> "DeterministicFiniteAutomaton":
        """ Copies the current DFA

        Returns
        ----------
        enfa : :class:`~pyformlang.finite_automaton.DeterministicFiniteAutomaton`
            A copy of the current DFA
        """
        dfa = DeterministicFiniteAutomaton()
        if self._start_state:
            dfa.add_start_state(list(self._start_state)[0])
        for final in self._final_states:
            dfa.add_final_state(final)
        for state in self._states:
            for symbol in self._input_symbols:
                state_to = self._transition_function(state, symbol)
                if state_to:
                    state_to = state_to[0]
                else:
                    state_to = None
                if state_to is not None:
                    dfa.add_transition(state, symbol, state_to)
        return dfa

    def _get_distinguishable_states(self):
        """ Get all the pair of states which are distinguishable

        Returns
        ----------
        states : set of (:class:`~pyformlang.finite_automaton.State`,\
                :class:`~pyformlang.finite_automaton.State`)
            The pair of distinguishable
        """
        disting = DistinguishableStates(len(self._states))
        to_process = self._initialize_distinguishable_states_to_process(disting)
        previous_d = self._get_previous_transitions()
        append = to_process.append
        not_contains_and_add = disting.not_contains_and_add
        get = previous_d.get
        symbols = self._input_symbols
        pop = to_process.pop
        emptylist = []
        while to_process:
            next0, next1 = pop()
            for symbol in symbols:
                next_states0 = get((next0, symbol), emptylist)
                next_states1 = get((next1, symbol), emptylist)
                for state0 in next_states0:
                    for state1 in next_states1:
                        state_combined = (state0, state1)
                        if not_contains_and_add(state_combined):
                            append(state_combined)
        return disting

    def _initialize_distinguishable_states_to_process(self, disting):
        to_process = deque()
        for final in self._final_states:
            for state in self._states:
                if state not in self._final_states:
                    disting.add((final, state))
                    to_process.append((final, state))
            disting.add((None, final))
            to_process.append((None, final))
        return to_process

    def _get_previous_transitions(self):
        previous_d = dict()
        for state in self._states:
            for symbol in self._input_symbols:
                next0 = self._transition_function(state, symbol)
                if next0:
                    next0 = next0[0]
                else:
                    next0 = None
                key = (next0, symbol)
                if key in previous_d:
                    previous_d[key].append(state)
                else:
                    previous_d[key] = [state]
        for symbol in self._input_symbols:
            key = (None, symbol)
            if key in previous_d:
                previous_d[key].append(None)
            else:
                previous_d[key] = [None]
        return previous_d

    def _get_reachable_states(self) -> AbstractSet[State]:
        """ Get all states which are reachable """
        to_process = []
        processed = set()
        for state in self._start_state:
            to_process.append(state)
            processed.add(state)
        while to_process:
            current = to_process.pop()
            for symbol in self._input_symbols:
                next_state = self._transition_function(current, symbol)
                if not next_state or next_state[0] in processed:
                    continue
                to_process.append(next_state[0])
                processed.add(next_state[0])
        return processed

    def minimize(self) -> "DeterministicFiniteAutomaton":
        """ Minimize the current DFA

        Returns
        ----------
        dfa : :class:`~pyformlang.deterministic_finite_automaton.DeterministicFiniteAutomaton`
            The minimal DFA
        """
        if not self._start_state or not self._final_states:
            return DeterministicFiniteAutomaton()
        # Remove unreachable
        reachables = self._get_reachable_states()
        states = self._states.intersection(reachables)
        # Group the equivalent states
        distinguishable = self._get_distinguishable_states()
        groups, were_grouped = get_groups(states, distinguishable)
        # Create a state for this
        to_new_states = dict()
        for group in groups:
            new_state = to_single_state(group)
            for state in group:
                to_new_states[state] = new_state
        for state in states:
            if state not in were_grouped:
                to_new_states[state] = state
        # Build the DFA
        dfa = DeterministicFiniteAutomaton()
        for state in self._start_state:
            dfa.add_start_state(to_new_states[state])
        for state in states:
            if state in self._final_states:
                dfa.add_final_state(to_new_states[state])
            done = set()
            new_state = to_new_states[state]
            for symbol in self._input_symbols:
                for next_node in self._transition_function(state, symbol):
                    if next_node in states:
                        next_node = to_new_states[next_node]
                        if (next_node, symbol) not in done:
                            dfa.add_transition(new_state, symbol, next_node)
                            done.add((next_node, symbol))
        return dfa


def get_groups(states, distinguishable) -> Iterable[AbstractSet[State]]:
    """ Get the groups in the minimization """
    groups = []
    were_grouped = set()
    states = list(states)
    for state0, state1 in distinguishable.get_non_distinguishable():
        were_grouped.add(state0)
        were_grouped.add(state1)
        new_groups = [{state0, state1}]
        for group in groups:
            if state0 in group or state1 in group:
                new_groups[0] = new_groups[0].union(group)
            else:
                new_groups.append(group)
        groups = new_groups
    return (groups, were_grouped)
