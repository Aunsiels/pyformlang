"""
Tests for nondeterministic finite automata
"""
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton,\
    Epsilon
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton.transition_function import \
    InvalidEpsilonTransition
import pytest


class TestNondeterministicFiniteAutomaton:
    """
    Tests for nondeterministic finite automata
    """

    # pylint: disable=missing-function-docstring, protected-access

    def test_creation(self):
        """ Test the creation of nfa
        """
        nfa = NondeterministicFiniteAutomaton()
        assert nfa is not None
        states = [State(x) for x in range(10)]
        nfa = NondeterministicFiniteAutomaton(start_state=set(states))
        assert nfa is not None

    def test_remove_initial(self):
        """ Test the remove of initial state
        """
        nfa = NondeterministicFiniteAutomaton()
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("a")
        nfa.add_transition(state0, symb_a, state1)
        nfa.add_start_state(state0)
        nfa.add_final_state(state1)
        assert nfa.is_deterministic()
        assert nfa.accepts([symb_a])
        assert nfa.remove_start_state(state1) == 0
        assert nfa.accepts([symb_a])
        assert nfa.remove_start_state(state0) == 1
        assert not nfa.accepts([symb_a])

    def test_accepts(self):
        """ Tests the acceptance of nfa
        """
        nfa = NondeterministicFiniteAutomaton()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        symb_d = Symbol("d")
        nfa.add_start_state(state0)
        nfa.add_final_state(state4)
        nfa.add_final_state(state3)
        nfa.add_transition(state0, symb_a, state1)
        nfa.add_transition(state1, symb_b, state1)
        nfa.add_transition(state1, symb_c, state2)
        nfa.add_transition(state1, symb_d, state3)
        nfa.add_transition(state1, symb_c, state4)
        nfa.add_transition(state1, symb_b, state4)
        assert not nfa.is_deterministic()
        assert nfa.accepts([symb_a, symb_b, symb_c])
        assert nfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_c])
        assert nfa.accepts([symb_a, symb_b, symb_d])
        assert nfa.accepts([symb_a, symb_d])
        assert nfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_b])
        assert not nfa.accepts([symb_a, symb_c, symb_d])
        assert not nfa.accepts([symb_d, symb_c, symb_d])
        assert not nfa.accepts([])
        assert not nfa.accepts([symb_c])
        nfa.add_start_state(state1)
        assert not nfa.is_deterministic()
        assert nfa.accepts([symb_c])
        nfa.remove_start_state(state1)
        dfa = nfa.to_deterministic()
        assert dfa.is_deterministic()
        assert dfa.accepts([symb_a, symb_b, symb_c])
        assert dfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_c])
        assert dfa.accepts([symb_a, symb_b, symb_d])
        assert dfa.accepts([symb_a, symb_d])
        assert dfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_b])
        assert not dfa.accepts([symb_a, symb_c, symb_d])
        assert not dfa.accepts([symb_d, symb_c, symb_d])
        assert not dfa.accepts([])
        assert not dfa.accepts([symb_c])

    def test_deterministic(self):
        """ Tests the deterministic transformation """
        nfa = NondeterministicFiniteAutomaton()
        state0 = State("q0")
        state1 = State("q1")
        state2 = State("q2")
        symb0 = Symbol(0)
        symb1 = Symbol(1)
        nfa.add_start_state(state0)
        nfa.add_final_state(state1)
        nfa.add_transition(state0, symb0, state0)
        nfa.add_transition(state0, symb0, state1)
        nfa.add_transition(state0, symb1, state0)
        nfa.add_transition(state1, symb1, state2)
        dfa = nfa.to_deterministic()
        assert len(dfa.states) == 3
        assert dfa.get_number_transitions() == 6

    def test_epsilon_refused(self):
        dfa = NondeterministicFiniteAutomaton()
        state0 = State(0)
        state1 = State(1)
        with pytest.raises(InvalidEpsilonTransition):
            dfa.add_transition(state0, Epsilon(), state1)
