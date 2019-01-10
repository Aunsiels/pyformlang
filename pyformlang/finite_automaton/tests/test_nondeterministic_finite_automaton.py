"""
Tests for nondeterministic finite automata
"""

import unittest

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol


class TestNondeterministicFiniteAutomaton(unittest.TestCase):
    """
    Tests for nondeterministic finite automata
    """

    def test_creation(self):
        """ Test the creation of nfa
        """
        nfa = NondeterministicFiniteAutomaton()
        self.assertIsNotNone(nfa)
        states = [State(x) for x in range(10)]
        nfa = NondeterministicFiniteAutomaton(start_state=states)
        self.assertIsNotNone(nfa)

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
        self.assertTrue(nfa.is_deterministic())
        self.assertTrue(nfa.accepts([symb_a]))
        self.assertEqual(nfa.remove_start_state(state1), 0)
        self.assertTrue(nfa.accepts([symb_a]))
        self.assertEqual(nfa.remove_start_state(state0), 1)
        self.assertFalse(nfa.accepts([symb_a]))


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
        self.assertFalse(nfa.is_deterministic())
        self.assertTrue(nfa.accepts([symb_a, symb_b, symb_c]))
        self.assertTrue(nfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_c]))
        self.assertTrue(nfa.accepts([symb_a, symb_b, symb_d]))
        self.assertTrue(nfa.accepts([symb_a, symb_d]))
        self.assertTrue(nfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_b]))
        self.assertFalse(nfa.accepts([symb_a, symb_c, symb_d]))
        self.assertFalse(nfa.accepts([symb_d, symb_c, symb_d]))
        self.assertFalse(nfa.accepts([]))
        self.assertFalse(nfa.accepts([symb_c]))
        nfa.add_start_state(state1)
        self.assertFalse(nfa.is_deterministic())
        self.assertTrue(nfa.accepts([symb_c]))
        nfa.remove_start_state(state1)
        dfa = nfa.to_deterministic()
        self.assertTrue(dfa.is_deterministic())
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_c]))
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_c]))
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_d]))
        self.assertTrue(dfa.accepts([symb_a, symb_d]))
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_b]))
        self.assertFalse(dfa.accepts([symb_a, symb_c, symb_d]))
        self.assertFalse(dfa.accepts([symb_d, symb_c, symb_d]))
        self.assertFalse(dfa.accepts([]))
        self.assertFalse(dfa.accepts([symb_c]))

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
        self.assertEqual(dfa.get_number_states(), 3)
        self.assertEqual(dfa.get_number_transitions(), 6)
