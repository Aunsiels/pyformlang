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

    def test_accepts(self):
        """ Tests the acceptance of nfa
        """
        dfa = NondeterministicFiniteAutomaton()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        symb_d = Symbol("d")
        dfa.set_initial_state(state0)
        dfa.add_final_state(state4)
        dfa.add_final_state(state3)
        dfa.add_transition(state0, symb_a, state1)
        dfa.add_transition(state1, symb_b, state1)
        dfa.add_transition(state1, symb_c, state2)
        dfa.add_transition(state1, symb_d, state3)
        dfa.add_transition(state1, symb_c, state4)
        dfa.add_transition(state1, symb_b, state4)
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_c]))
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_c]))
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_d]))
        self.assertTrue(dfa.accepts([symb_a, symb_d]))
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_b]))
        self.assertFalse(dfa.accepts([symb_a, symb_c, symb_d]))
        self.assertFalse(dfa.accepts([symb_d, symb_c, symb_d]))
        self.assertFalse(dfa.accepts([]))

