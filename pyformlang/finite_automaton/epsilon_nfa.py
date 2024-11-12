"""
Nondeterministic Automaton with epsilon transitions
"""

from typing import Iterable, Set, AbstractSet, Hashable
from networkx import MultiDiGraph

from .state import State
from .symbol import Symbol
from .epsilon import Epsilon
from .nondeterministic_transition_function import \
    NondeterministicTransitionFunction
from .finite_automaton import FiniteAutomaton
from .utils import to_state, to_symbol


class EpsilonNFA(FiniteAutomaton):
    """ Represents an epsilon NFA

    Parameters
    ----------
    states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`, \
     optional
        A finite set of input symbols
    transition_function :  \
    :class:`~pyformlang.finite_automaton.NondeterministicTransitionFunction`\
, optional
        Takes as arguments a state and an input symbol and returns a state.
    start_state : set of :class:`~pyformlang.finite_automaton.State`, optional
        A start state, element of states
    final_states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A set of final or accepting states. It is a subset of states.

    Examples
    --------

    >>> enfa = EpsilonNFA()

    Creates an empty epsilon non-deterministic automaton.

    >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), (0, "epsilon", 2)])

    Adds three transition, one of them being an epsilon transition.

    >>> enfa.add_start_state(0)

    Adds a start state.

    >>> enfa.add_final_state(1)

    Adds a final state.

    >>> enfa.is_deterministic()
    False

    Checks if the automaton is deterministic.

    """

    def __init__(
            self,
            states: AbstractSet[Hashable] = None,
            input_symbols: AbstractSet[Hashable] = None,
            transition_function: NondeterministicTransitionFunction = None,
            start_states: AbstractSet[Hashable] = None,
            final_states: AbstractSet[Hashable] = None) -> None:
        super().__init__()
        if states is not None:
            states = {to_state(x) for x in states}
        self._states = states or set()
        if input_symbols is not None:
            input_symbols = {to_symbol(x) for x in input_symbols}
        self._input_symbols = input_symbols or set()
        self._transition_function = transition_function \
            or NondeterministicTransitionFunction()
        if start_states is not None:
            start_states = {to_state(x) for x in start_states}
        self._start_states = start_states or set()
        if final_states is not None:
            final_states = {to_state(x) for x in final_states}
        self._final_states = final_states or set()
        for state in self._final_states:
            self._states.add(state)
        for state in self._start_states:
            self._states.add(state)

    def _get_next_states_iterable(self,
                                  current_states: Iterable[State],
                                  symbol: Symbol) \
            -> Set[State]:
        """ Gives the set of next states, starting from a set of states

        Parameters
        ----------
        current_states : iterable of \
        :class:`~pyformlang.finite_automaton.State`
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

    def accepts(self, word: Iterable[Hashable]) -> bool:
        """ Checks whether the epsilon nfa accepts a given word

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

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.accepts(["abc", "epsilon"])
        True

        >>> enfa.accepts(["epsilon"])
        False

        """
        word = [to_symbol(x) for x in word]
        current_states = self.eclose_iterable(self._start_states)
        for symbol in word:
            if symbol == Epsilon():
                continue
            next_states = self._get_next_states_iterable(current_states,
                                                         symbol)
            current_states = self.eclose_iterable(next_states)
        return any(self.is_final_state(x) for x in current_states)

    def eclose_iterable(self, states: Iterable[Hashable]) -> Set[State]:
        """ Compute the epsilon closure of a collection of states

        Parameters
        ----------
        states : iterable of :class:`~pyformlang.finite_automaton.State`
            The source states

        Returns
        ---------
        states : set of :class:`~pyformlang.finite_automaton.State`
            The epsilon closure of the source state

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.eclose_iterable([0])
        {2}
        """
        states = [to_state(x) for x in states]
        res = set()
        for state in states:
            res = res.union(self.eclose(state))
        return res

    def eclose(self, state: Hashable) -> Set[State]:
        """ Compute the epsilon closure of a state

        Parameters
        ----------
        state : :class:`~pyformlang.finite_automaton.State`
            The source state

        Returns
        ---------
        states : set of :class:`~pyformlang.finite_automaton.State`
            The epsilon closure of the source state

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.eclose(0)
        {2}

        """
        state = to_state(state)
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

    def is_deterministic(self) -> bool:
        """ Checks whether an automaton is deterministic

        Returns
        ----------
        is_deterministic : bool
           Whether the automaton is deterministic

        Examples
        --------

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.is_deterministic()
        False

        """
        return len(self._start_states) <= 1 \
            and self._transition_function.is_deterministic() \
            and all({x} == self.eclose(x) for x in self._states)

    def copy(self) -> "EpsilonNFA":
        """ Copies the current Epsilon NFA

        Returns
        ----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            A copy of the current Epsilon NFA

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa_copy = enfa.copy()
        >>> enfa.is_equivalent_to(enfa_copy)
        True

        """
        return self._copy_to(EpsilonNFA())

    @classmethod
    def from_networkx(cls, graph: MultiDiGraph) -> "EpsilonNFA":
        """
        Import a networkx graph into an finite state automaton. \
        The imported graph requires to have the good format, i.e. to come \
        from the function to_networkx

        Parameters
        ----------
        graph :
            The graph representation of the automaton

        Returns
        -------
        enfa :
            A epsilon nondeterministic finite automaton read from the graph

        TODO
        -------
        * We lose the type of the node value if going through a dot file
        * Explain the format

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> graph = enfa.to_networkx()
        >>> enfa_from_nx = EpsilonNFA.from_networkx(graph)

        """
        enfa = EpsilonNFA()
        for s_from in graph:
            for s_to in graph[s_from]:
                for transition in graph[s_from][s_to].values():
                    if "label" in transition:
                        enfa.add_transition(s_from,
                                            transition["label"],
                                            s_to)
        for node in graph.nodes:
            if graph.nodes[node].get("is_start", False):
                enfa.add_start_state(node)
            if graph.nodes[node].get("is_final", False):
                enfa.add_final_state(node)
        return enfa

    def get_complement(self) -> "EpsilonNFA":
        """ Get the complement of the current Epsilon NFA

        Equivalent to:

          >>> -automaton

        Returns
        ----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            A complement automaton

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa_complement = enfa.get_complement()
        >>> enfa_complement.accepts(["epsilon"])
        True

        >>> enfa_complement.accepts(["abc"])
        False

        """
        enfa = self.copy()
        trash = self.__get_new_state("Trash")
        enfa.add_final_state(trash)
        for state in self._states:
            if state in self._final_states:
                enfa.remove_final_state(state)
            else:
                enfa.add_final_state(state)
        for state in self._states:
            for symbol in self._input_symbols:
                state_to = []
                eclose = self.eclose(state)
                for state0 in eclose:
                    state_to += self._transition_function(state0, symbol)
                if not state_to:
                    enfa.add_transition(state, symbol, trash)
        for symbol in self._input_symbols:
            enfa.add_transition(trash, symbol, trash)
        return enfa

    def __neg__(self) -> "EpsilonNFA":
        """ Get the complement of the current Epsilon NFA

        Returns
        ----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            A complement automaton
        """
        return self.get_complement()

    def get_intersection(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """ Computes the intersection of two Epsilon NFAs

        Equivalent to:

          >>> automaton0 and automaton1

        Parameters
        ----------
        other : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The other Epsilon NFA

        Returns
        ---------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The intersection of the two Epsilon NFAs

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa2 = EpsilonNFA()
        >>> enfa2.add_transition(0, "d", 1)
        >>> enfa2.add_final_state(1)
        >>> enfa2.add_start_state(0)
        >>> enfa_inter = enfa.get_intersection(enfa2)
        >>> enfa_inter.accepts(["abc"])
        False

        >>> enfa_inter.accepts(["d"])
        True

        """
        enfa = EpsilonNFA()
        symbols = list(self.symbols.intersection(other.symbols))
        to_process = []
        processed = set()
        for st0 in self.eclose_iterable(self.start_states):
            for st1 in other.eclose_iterable(other.start_states):
                enfa.add_start_state(self.__combine_state_pair(st0, st1))
                to_process.append((st0, st1))
                processed.add((st0, st1))
        for st0 in self.final_states:
            for st1 in other.final_states:
                enfa.add_final_state(self.__combine_state_pair(st0, st1))
        while to_process:
            st0, st1 = to_process.pop()
            current_state = self.__combine_state_pair(st0, st1)
            for symb in symbols:
                for new_s0 in self.eclose_iterable(self(st0, symb)):
                    for new_s1 in other.eclose_iterable(other(st1, symb)):
                        state = self.__combine_state_pair(new_s0, new_s1)
                        enfa.add_transition(current_state, symb, state)
                        if (new_s0, new_s1) not in processed:
                            processed.add((new_s0, new_s1))
                            to_process.append((new_s0, new_s1))
        return enfa

    def __and__(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """ Computes the intersection of two Epsilon NFAs

        Parameters
        ----------
        other : :class:`~pyformlang.finite_automaton.EpsilonNFA`
           The other Epsilon NFA

        Returns
        ---------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
           The intersection of the two Epsilon NFAs
        """
        return self.get_intersection(other)

    def get_union(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """ Computes the union with given Epsilon NFA """
        union = other.copy()
        self._copy_to(union)
        return union

    def __or__(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """ Computes the union with given Epsilon NFA """
        return self.get_union(other)

    def concatenate(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """ Computes the concatenation of two Epsilon NFAs """
        concatenation = EpsilonNFA()
        for s_from, symb_by, s_to in self:
            concatenation.add_transition((0, s_from.value),
                                         symb_by,
                                         (0, s_to.value))
            if s_from in self.start_states:
                concatenation.add_start_state((0, s_from.value))
        for s_from, symb_by, s_to in other:
            concatenation.add_transition((1, s_from.value),
                                         symb_by,
                                         (1, s_to.value))
            if other.is_final_state(s_to):
                concatenation.add_final_state((1, s_to.value))
        for self_final in self.final_states:
            for other_start in other.start_states:
                concatenation.add_transition((0, self_final.value),
                                             Epsilon(),
                                             (1, other_start.value))
        return concatenation

    def __add__(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """ Computes the concatenation of two Epsilon NFAs """
        return self.concatenate(other)

    def get_difference(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """ Computes the difference with another Epsilon NFA

        Equivalent to:

          >>> automaton0 - automaton1

        Parameters
        ----------
        other : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The other Epsilon NFA

        Returns
        ---------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The difference with the other epsilon NFA

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa2 = EpsilonNFA()
        >>> enfa2.add_transition(0, "d", 1)
        >>> enfa2.add_final_state(1)
        >>> enfa2.add_start_state(0)
        >>> enfa_diff = enfa.get_difference(enfa2)
        >>> enfa_diff.accepts(["d"])
        False

        >>> enfa_diff.accepts(["abc"])
        True

        """
        other = other.copy()
        for symbol in self._input_symbols:
            other.add_symbol(symbol)
        return self.get_intersection(other.get_complement())

    def __sub__(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """ Compute the difference with another Epsilon NFA

        Equivalent to:
          >> automaton0 - automaton1

        Parameters
        ----------
        other : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The other Epsilon NFA

        Returns
        ---------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The difference with the other epsilon NFA
        """
        return self.get_difference(other)

    def reverse(self) -> "EpsilonNFA":
        """ Compute the reversed EpsilonNFA

        Equivalent to:
          >> ~automaton

        Returns
        ---------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The reversed automaton

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (1, "d", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(2)
        >>> enfa_reverse = enfa.reverse()
        >>> enfa_reverse.accepts(["d", "abc"])
        True

        """
        enfa = EpsilonNFA()
        for state0 in self._states:
            for symbol in self._input_symbols:
                for state1 in self._transition_function(state0, symbol):
                    enfa.add_transition(state1, symbol, state0)
            for state1 in self._transition_function(state0, Epsilon()):
                enfa.add_transition(state1, Epsilon(), state0)
        for start in self._start_states:
            enfa.add_final_state(start)
        for final in self._final_states:
            enfa.add_start_state(final)
        return enfa

    def __invert__(self) -> "EpsilonNFA":
        """ Compute the reversed EpsilonNFA

        Returns
        ---------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The reversed automaton
        """
        return self.reverse()

    def kleene_star(self) -> "EpsilonNFA":
        """ Compute the kleene closure of current EpsilonNFA"""
        kleene_closure = self.copy()
        new_start = self.__get_new_state("Start")
        for old_start in self.start_states:
            kleene_closure.add_transition(new_start, Epsilon(), old_start)
        kleene_closure.start_states.clear()
        kleene_closure.add_start_state(new_start)
        for final_state in self.final_states:
            kleene_closure.add_transition(final_state, Epsilon(), new_start)
        return kleene_closure

    def is_empty(self) -> bool:
        """ Checks if the language represented by the FSM is empty or not

        Returns
        ----------
        is_empty : bool
            Whether the language is empty or not

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.is_empty()
        False

        """
        to_process = []
        processed = set()
        for start in self._start_states:
            to_process.append(start)
            processed.add(start)
        while to_process:
            current = to_process.pop()
            if current in self._final_states:
                return False
            for symbol in self._input_symbols:
                for state in self._transition_function(current, symbol):
                    if state not in processed:
                        to_process.append(state)
                        processed.add(state)
            for state in self._transition_function(current, Epsilon()):
                if state not in processed:
                    to_process.append(state)
                    processed.add(state)
        return True

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __get_new_state(self, prefix: str) -> State:
        """
        Get a state that wasn't previously in automaton
        starting with given string.
        """
        existing_values = set(state.value for state in self.states)
        while prefix in existing_values:
            prefix += '`'
        return State(prefix)

    @staticmethod
    def __combine_state_pair(state0: State, state1: State) -> State:
        """ Combine two states """
        return State(str(state0.value) + "; " + str(state1.value))
