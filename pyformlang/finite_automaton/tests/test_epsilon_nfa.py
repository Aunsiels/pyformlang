"""
Tests for epsilon NFA
"""

import unittest

from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon


class TestEpsilonNFA(unittest.TestCase):
    """ Tests epsilon NFA """

    def test_eclose(self):
        """ Test of the epsilon closure """
        states = [State(x) for x in range(8)]
        epsilon = Epsilon()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        enfa = EpsilonNFA()
        enfa.add_transition(states[1], epsilon, states[2])
        enfa.add_transition(states[1], epsilon, states[4])
        enfa.add_transition(states[2], epsilon, states[3])
        enfa.add_transition(states[3], epsilon, states[6])
        enfa.add_transition(states[5], epsilon, states[7])
        enfa.add_transition(states[4], symb_a, states[5])
        enfa.add_transition(states[5], symb_b, states[6])
        self.assertEqual(len(enfa.eclose(states[1])), 5)
        self.assertEqual(len(enfa.eclose(states[2])), 3)
        self.assertEqual(len(enfa.eclose(states[5])), 2)
        self.assertEqual(len(enfa.eclose(states[6])), 1)

    def test_accept(self):
        """ Test the acceptance """
        epsilon = Epsilon()
        plus = Symbol("+")
        minus = Symbol("-")
        point = Symbol(".")
        digits = [Symbol(x) for x in range(10)]
        states = [State("q" + str(x)) for x in range(6)]
        enfa = EpsilonNFA()
        enfa.add_start_state(states[0])
        enfa.add_final_state(states[5])
        enfa.add_transition(states[0], epsilon, states[1])
        enfa.add_transition(states[0], plus, states[1])
        enfa.add_transition(states[0], minus, states[1])
        for digit in digits:
            enfa.add_transition(states[1], digit, states[1])
            enfa.add_transition(states[1], digit, states[4])
            enfa.add_transition(states[2], digit, states[3])
            enfa.add_transition(states[3], digit, states[3])
        enfa.add_transition(states[1], point, states[2])
        enfa.add_transition(states[4], point, states[3])
        enfa.add_transition(states[3], epsilon, states[5])
        self.assertTrue(enfa.accepts([plus, digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([minus, digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], point]))
        self.assertTrue(enfa.accepts([digits[1], point, epsilon]))
        self.assertTrue(enfa.accepts([point, digits[9]]))
        self.assertFalse(enfa.accepts([point]))
        self.assertFalse(enfa.accepts([plus]))
