"""
Representation of a deterministic finite automaton
"""

from typing import Dict, List, Iterable, AbstractSet, Optional, Hashable, Any
from numpy import empty

from .state import State
from .symbol import Symbol
from .deterministic_transition_function import DeterministicTransitionFunction
from .epsilon_nfa import EpsilonNFA
from .nondeterministic_finite_automaton import NondeterministicFiniteAutomaton
from .hopcroft_processing_list import HopcroftProcessingList
from .partition import Partition
from .utils import to_state, to_symbol, to_single_state


class PreviousTransitions:
    """For internal usage"""

    def __init__(self,
                 states: AbstractSet[State],
                 symbols: AbstractSet[Symbol]) -> None:
        self._to_index_state: Dict[Optional[State], int] = {}
        self._to_index_state[None] = 0
        for i, state in enumerate(states):
            self._to_index_state[state] = i + 1
        self._to_index_symbol: Dict[Optional[Symbol], int] = {}
        for i, symbol in enumerate(symbols):
            self._to_index_symbol[symbol] = i
        self._conversion = empty((len(states) + 1, len(symbols)),
                                 dtype=object)

    def add(self,
            next0: Optional[State],
            symbol: Symbol,
            state: Optional[State]) -> None:
        """ Internal """
        i_next0 = self._to_index_state[next0]
        i_symbol = self._to_index_symbol[symbol]
        if self._conversion[i_next0, i_symbol] is None:
            self._conversion[i_next0, i_symbol] = [state]
        else:
            self._conversion[i_next0, i_symbol].append(state)

    def get(self, next0: State, symbol: Symbol) -> List[object]:
        """ Internal """
        i_next0 = self._to_index_state[next0]
        i_symbol = self._to_index_symbol[symbol]
        return self._conversion[i_next0, i_symbol] or []


class DeterministicFiniteAutomaton(NondeterministicFiniteAutomaton):
    """ Represents a deterministic finite automaton

    This class represents a deterministic finite automaton.

    Parameters
    ----------
    states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`, optional
        A finite set of input symbols
    transition_function : \
    :class:`~pyformlang.finite_automaton.TransitionFunction`, optional
        Takes as arguments a state and an input symbol and returns a state.
    start_state : :class:`~pyformlang.finite_automaton.State`, optional
        A start state, element of states
    final_states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A set of final or accepting states. It is a subset of states.

    Examples
    --------

    >>> dfa = DeterministicFiniteAutomaton()

    Creates an empty deterministic finite automaton.

    >>> dfa.add_transitions([(0, "abc", 1), (0, "d", 1)])

    Adds two transitions to the deterministic finite automaton. One goes from \
    the state 0 to the state 1 when reading the string "abc". The other also \
    goes from the state 0 to the state 1 when reading the string "d".

    >>> dfa.add_start_state(0)

    Adds the start state, 0 here.

    >>> dfa.add_final_state(1)

    Adds a final state, 1 here.

    >>> dfa.is_deterministic()
    True

    Checks if the automaton is deterministic. True here.

    >>> dfa.accepts(["abc"])
    True

    Checks if the automaton recognize the word composed of a single letter, \
    "abc".

    """

    def __init__(self,
                 states: AbstractSet[Hashable] = None,
                 input_symbols: AbstractSet[Hashable] = None,
                 transition_function: DeterministicTransitionFunction = None,
                 start_state: Hashable = None,
                 final_states: AbstractSet[Hashable] = None) -> None:
        start_states = {start_state} if start_state is not None else None
        super().__init__(states,
                         input_symbols,
                         None,
                         start_states,
                         final_states)
        self._transition_function: DeterministicTransitionFunction = \
            transition_function or DeterministicTransitionFunction()

    @property
    def start_state(self) -> Optional[State]:
        """ Gets the start state """
        return list(self._start_states)[0] if self._start_states else None

    def add_start_state(self, state: Hashable) -> int:
        """ Set an initial state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The new initial state

        Returns
        ----------
        done : int
            1 is correctly added

        Examples
        --------

        >>> dfa = DeterministicFiniteAutomaton()
        >>> dfa.add_start_state(0)

        """
        state = to_state(state)
        self._start_states = {state}
        self._states.add(state)
        return 1

    def remove_start_state(self, state: Hashable) -> int:
        """ remove an initial state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The new initial state

        Returns
        ----------
        done : int
            1 is correctly added

        Examples
        --------

        >>> dfa = DeterministicFiniteAutomaton()
        >>> dfa.add_start_state(0)
        >>> dfa.remove_start_state(0)

        """
        state = to_state(state)
        if self._start_states == {state}:
            self._start_states = set()
            return 1
        return 0

    def accepts(self, word: Iterable[Hashable]) -> bool:
        """ Checks whether the dfa accepts a given word

        Parameters
        ----------
        word : iterable of :class:`~pyformlang.finite_automaton.Symbol`
            A sequence of input symbols

        Returns
        ----------
        is_accepted : bool
            Whether the word is accepted or not

        Examples
        --------

        >>> dfa = DeterministicFiniteAutomaton()
        >>> dfa.add_transitions([(0, "abc", 1), (0, "d", 1)])
        >>> dfa.add_start_state(0)
        >>> dfa.add_final_state(1)
        >>> dfa.accepts(["abc"])
        True

        """
        word = [to_symbol(x) for x in word]
        current_state = self.start_state
        for symbol in word:
            if current_state is None:
                return False
            current_state = self._transition_function.get_next_state(
                current_state, symbol)
        return current_state is not None and self.is_final_state(current_state)

    def is_deterministic(self) -> bool:
        """ Checks whether an automaton is deterministic

        Returns
        ----------
        is_deterministic : bool
           Whether the automaton is deterministic

        Examples
        --------

        >>> dfa = DeterministicFiniteAutomaton()
        >>> dfa.is_deterministic()
        True

        """
        return True

    def copy(self) -> "DeterministicFiniteAutomaton":
        """ Copies the current DFA

        Returns
        ----------
        enfa :  :class:`~pyformlang.finite_automaton\
        .DeterministicFiniteAutomaton`
            A copy of the current DFA

        Examples
        --------

        >>> dfa = DeterministicFiniteAutomaton()
        >>> dfa.add_transitions([(0, "abc", 1), (0, "d", 1)])
        >>> dfa.add_start_state(0)
        >>> dfa.add_final_state(1)
        >>> dfa_copy = dfa.copy()
        >>> dfa.is_equivalent_to(dfa_copy)
        True

        """
        return self._copy_to(DeterministicFiniteAutomaton())

    def get_next_state(self, s_from: Hashable, symb_by: Hashable) \
            -> Optional[State]:
        """ Make a call of deterministic transition function """
        s_from = to_state(s_from)
        symb_by = to_symbol(symb_by)
        return self._transition_function.get_next_state(s_from, symb_by)

    def _get_previous_transitions(self) -> PreviousTransitions:
        previous_transitions = PreviousTransitions(self._states,
                                                   self._input_symbols)
        for state in self._states:
            for symbol in self._input_symbols:
                next0 = self._transition_function.get_next_state(state, symbol)
                previous_transitions.add(next0, symbol, state)
        for symbol in self._input_symbols:
            previous_transitions.add(None, symbol, None)
        return previous_transitions

    def minimize(self) -> "DeterministicFiniteAutomaton":
        """ Minimize the current DFA

        Returns
        ----------
        dfa :  :class:`~pyformlang.deterministic_finite_automaton\
        .DeterministicFiniteAutomaton`
            The minimal DFA

        Examples
        --------

        >>> dfa = DeterministicFiniteAutomaton()
        >>> dfa.add_transitions([(0, "abc", 1), (0, "d", 1)])
        >>> dfa.add_start_state(0)
        >>> dfa.add_final_state(1)
        >>> dfa_minimal = dfa.minimize()
        >>> dfa.is_equivalent_to(dfa_minimal)
        True

        """
        if not self._start_states or not self._final_states:
            res = DeterministicFiniteAutomaton()
            res.add_start_state(State("Empty"))
            return res
        # Remove unreachable
        reachables = self._get_reachable_states()
        states = self._states.intersection(reachables)
        # Group the equivalent states
        partition = self._get_partition()
        groups = partition.get_groups()
        # Create a state for this
        to_new_states = {}
        for group in groups:
            new_state = to_single_state(group)
            for state in group:
                to_new_states[state] = new_state
        # Build the DFA
        dfa = DeterministicFiniteAutomaton()
        for state in self._start_states:
            dfa.add_start_state(to_new_states[state])
        for state in states:
            if state in self._final_states:
                dfa.add_final_state(to_new_states[state])
            done = set()
            new_state = to_new_states[state]
            for symbol in self._input_symbols:
                next_node = self._transition_function.get_next_state(
                    state, symbol)
                if next_node and next_node in states:
                    next_node = to_new_states[next_node]
                    if (next_node, symbol) not in done:
                        dfa.add_transition(new_state, symbol, next_node)
                        done.add((next_node, symbol))
        return dfa

    @classmethod
    def from_epsilon_nfa(cls, enfa: EpsilonNFA) \
            -> "DeterministicFiniteAutomaton":
        """ Builds dfa equivalent to the given enfa """
        return cls._from_epsilon_nfa_internal(enfa, True)

    @classmethod
    def from_nfa(cls, nfa: NondeterministicFiniteAutomaton) \
            -> "DeterministicFiniteAutomaton":
        """ Builds dfa equivalent to the given nfa """
        return cls._from_epsilon_nfa_internal(nfa, False)

    @classmethod
    def _from_epsilon_nfa_internal(cls, enfa: EpsilonNFA, eclose: bool) \
            -> "DeterministicFiniteAutomaton":
        """ Builds dfa equivalent to the given automaton

        Parameters
        ----------
        eclose : bool
            Whether to use the epsilon closure or not

        Returns
        ----------
        dfa :  :class:`~pyformlang.finite_automaton\
        .DeterministicFiniteAutomaton`
            A dfa equivalent to the current nfa
        """
        dfa = DeterministicFiniteAutomaton()
        # Add Eclose
        if eclose:
            start_eclose = enfa.eclose_iterable(enfa.start_states)
        else:
            start_eclose = enfa.start_states
        start_state = to_single_state(start_eclose)
        dfa.add_start_state(start_state)
        to_process = [start_eclose]
        processed = {start_state}
        while to_process:
            current = to_process.pop()
            s_from = to_single_state(current)
            for symbol in enfa.symbols:
                all_trans = [enfa(x, symbol) for x in current]
                state = set()
                for trans in all_trans:
                    state = state.union(trans)
                if not state:
                    continue
                # Eclose added
                if eclose:
                    state = enfa.eclose_iterable(state)
                state_merged = to_single_state(state)
                dfa.add_transition(s_from, symbol, state_merged)
                if state_merged not in processed:
                    processed.add(state_merged)
                    to_process.append(state)
            for state in current:
                if state in enfa.final_states:
                    dfa.add_final_state(s_from)
        return dfa

    def _get_partition(self) -> Partition:
        previous_transitions = self._get_previous_transitions()
        finals = []
        non_finals = []
        for state in self._states:
            if state in self._final_states:
                finals.append(state)
            else:
                non_finals.append(state)
        # None is the trash node
        non_finals.append(None)
        # + 1 for trash node
        partition = Partition(len(self._states) + 1)
        partition.add_class(finals)
        partition.add_class(non_finals)
        # + 1 for trash node
        processing_list = HopcroftProcessingList(len(self._states) + 1,
                                                 self._input_symbols)
        to_add = 0  # 0 is the index of finals, 1 of non_finals
        if len(non_finals) < len(finals):
            to_add = 1
        for symbol in self._input_symbols:
            processing_list.insert(to_add, symbol)
        while not processing_list.is_empty():
            current_class, current_symbol = processing_list.pop()
            inverse = []
            for element in partition.part[current_class]:
                inverse += previous_transitions.get(element.value,
                                                    current_symbol)
            for valid_set in partition.get_valid_sets(inverse):
                new_class = partition.split(valid_set, inverse)
                for symbol in self._input_symbols:
                    if processing_list.contains(valid_set, symbol):
                        processing_list.insert(new_class, symbol)
                    elif (len(partition.part[valid_set]) <
                          len(partition.part[new_class])):
                        processing_list.insert(valid_set, symbol)
                    else:
                        processing_list.insert(new_class, symbol)
        return partition

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DeterministicFiniteAutomaton):
            return False
        return self.is_equivalent_to(other)

    def is_equivalent_to(self, other: "DeterministicFiniteAutomaton") -> bool:
        """ Check whether two automata are equivalent

        Parameters
        ----------
        other :  :class:`~pyformlang.deterministic_finite_automaton\
        .FiniteAutomaton`
            A sequence of input symbols

        Returns
        ----------
        are_equivalent : bool
            Whether the two automata are equivalent or not

        Examples
        --------

        >>> dfa = DeterministicFiniteAutomaton()
        >>> dfa.add_transitions([(0, "abc", 1), (0, "d", 1)])
        >>> dfa.add_start_state(0)
        >>> dfa.add_final_state(1)
        >>> dfa_minimal = dfa.minimize()
        >>> dfa.is_equivalent_to(dfa_minimal)
        True

        """
        self_minimal = self.minimize()
        other_minimal = other.minimize()
        return self._is_equivalent_to_minimal(self_minimal, other_minimal)

    @staticmethod
    def _is_equivalent_to_minimal(
            self_minimal: "DeterministicFiniteAutomaton",
            other_minimal: "DeterministicFiniteAutomaton") -> bool:
        to_process = [(self_minimal.start_state,
                       other_minimal.start_state)]
        matches = {self_minimal.start_state: other_minimal.start_state}
        while to_process:
            current_self, current_other = to_process.pop()
            if (self_minimal.is_final_state(current_self)
                    and not other_minimal.is_final_state(current_other)) or \
                    (not self_minimal.is_final_state(current_self)
                     and other_minimal.is_final_state(current_other)):
                return False
            next_self = list(self_minimal.get_transitions_from(current_self))
            next_other = list(other_minimal.get_transitions_from(current_other))
            if len(next_self) != len(next_other):
                return False
            if len(next_self) == 0:
                continue
            for next_temp, other_temp in zip(sorted(next_self,
                                                    key=lambda x: hash(x[0])),
                                             sorted(next_other,
                                                    key=lambda x: hash(x[0]))):
                next_symbol_self, next_state_self = next_temp
                next_symbol_other, next_state_other = other_temp
                if next_symbol_other != next_symbol_self:
                    return False
                if next_state_self in matches:
                    if matches[next_state_self] != next_state_other:
                        return False
                else:
                    matches[next_state_self] = next_state_other
                    to_process.append((next_state_self, next_state_other))
        return True
