"""
Representation of a nondeterministic finite automaton
"""

from typing import Iterable, Hashable

from .epsilon import Epsilon
from .epsilon_nfa import EpsilonNFA
from .utils import to_symbol


class NondeterministicFiniteAutomaton(EpsilonNFA):
    """ Represents a nondeterministic finite automaton

    This class represents a nondeterministic finite automaton, where epsilon \
    transition are forbidden.

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
    start_state : :class:`~pyformlang.finite_automaton.State`, optional
        A start state, element of states
    final_states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A set of final or accepting states. It is a subset of states.

    Examples
    --------

    >>> nfa = NondeterministicFiniteAutomaton()

    Creates the NFA.

    >>> nfa.add_transitions([(0, "a", 1), (0, "a", 2)])

    Adds two transitions.

    >>> nfa.add_start_state(0)

    Adds a start state.

    >>> nfa.add_final_state(1)

    Adds a final state.

    >>> nfa.accepts(["a"])
    True

    >>> nfa.is_deterministic()
    False

    """

    def accepts(self, word: Iterable[Hashable]) -> bool:
        """ Checks whether the nfa accepts a given word

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

        >>> nfa = NondeterministicFiniteAutomaton()
        >>> nfa.add_transitions([(0, "a", 1), (0, "a", 2)])
        >>> nfa.add_start_state(0)
        >>> nfa.add_final_state(1)
        >>> nfa.accepts(["a"])
        True

        """
        word = [to_symbol(x) for x in word]
        current_states = self._start_states
        for symbol in word:
            current_states = self._get_next_states_iterable(current_states,
                                                            symbol)
        return any(self.is_final_state(x) for x in current_states)

    def is_deterministic(self) -> bool:
        """ Checks whether an automaton is deterministic

        Returns
        ----------
        is_deterministic : bool
           Whether the automaton is deterministic

        Examples
        --------

        >>> nfa = NondeterministicFiniteAutomaton()
        >>> nfa.add_transitions([(0, "a", 1), (0, "a", 2)])
        >>> nfa.add_start_state(0)
        >>> nfa.add_final_state(1)
        >>> nfa.is_deterministic()
        False

        """
        return len(self._start_states) <= 1 and \
            self._transition_function.is_deterministic()

    def add_transition(self,
                       s_from: Hashable,
                       symb_by: Hashable,
                       s_to: Hashable) -> int:
        symb_by = to_symbol(symb_by)
        if symb_by == Epsilon():
            raise InvalidEpsilonTransition
        return super().add_transition(s_from, symb_by, s_to)

    def copy(self) -> "NondeterministicFiniteAutomaton":
        """ Copies the current NFA instance """
        return self._copy_to(NondeterministicFiniteAutomaton())

    @classmethod
    def from_epsilon_nfa(cls, enfa: EpsilonNFA) \
            -> "NondeterministicFiniteAutomaton":
        """ Builds nfa equivalent to the given enfa

        Returns
        ----------
        dfa :  :class:`~pyformlang.finite_automaton. \
            NondeterministicFiniteAutomaton`
            A non-deterministic finite automaton equivalent to the current \
            nfa, with no epsilon transition
        """
        nfa = NondeterministicFiniteAutomaton()
        for state in enfa.start_states:
            nfa.add_start_state(state)
        for state in enfa.final_states:
            nfa.add_final_state(state)
        start_eclose = enfa.eclose_iterable(enfa.start_states)
        for state in start_eclose:
            nfa.add_start_state(state)
        for state in enfa.states:
            eclose = enfa.eclose(state)
            for e_state in eclose:
                if e_state in enfa.final_states:
                    nfa.add_final_state(state)
                for symb in enfa.symbols:
                    for next_state in enfa(e_state, symb):
                        nfa.add_transition(state, symb, next_state)
        return nfa


class InvalidEpsilonTransition(Exception):
    """Exception raised when an epsilon transition is created in
    nondeterministic automaton"""
