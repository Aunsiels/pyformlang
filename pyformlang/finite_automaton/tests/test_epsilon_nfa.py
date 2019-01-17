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
        self.assertEqual(enfa.remove_transition(states[1], epsilon, states[4]),
                         1)
        self.assertFalse(enfa.is_deterministic())

    def test_accept(self):
        """ Test the acceptance """
        self._perform_tests_digits(False)

    def test_copy(self):
        """ Tests the copy of enda """
        self._perform_tests_digits(True)

    def _perform_tests_digits(self, copy=False):
        enfa, digits, epsilon, plus, minus, point = get_digits_enfa()
        if copy:
            enfa = enfa.copy()
        self.assertTrue(enfa.accepts([plus, digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([minus, digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], point]))
        self.assertTrue(enfa.accepts([digits[1], point, epsilon]))
        self.assertTrue(enfa.accepts([point, digits[9]]))
        self.assertFalse(enfa.accepts([point]))
        self.assertFalse(enfa.accepts([plus]))
        self.assertFalse(enfa.is_deterministic())

    def test_deterministic(self):
        """ Tests the transformation to a dfa"""
        enfa, digits, _, plus, minus, point = get_digits_enfa()
        dfa = enfa.to_deterministic()
        self.assertTrue(dfa.is_deterministic())
        self.assertEqual(dfa.get_number_states(), 6)
        self.assertEqual(dfa.get_number_transitions(), 65)
        self.assertEqual(dfa.get_number_final_states(), 2)
        self.assertTrue(dfa.accepts([plus, digits[1], point, digits[9]]))
        self.assertTrue(dfa.accepts([minus, digits[1], point, digits[9]]))
        self.assertTrue(dfa.accepts([digits[1], point, digits[9]]))
        self.assertTrue(dfa.accepts([digits[1], point]))
        self.assertTrue(dfa.accepts([digits[1], point]))
        self.assertTrue(dfa.accepts([point, digits[9]]))
        self.assertFalse(dfa.accepts([point]))
        self.assertFalse(dfa.accepts([plus]))

    def test_create_or_transitions(self):
        """ Tests the creation of or transitions """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        symb_plus = Symbol("c+d")
        enfa.add_start_state(state0)
        enfa.add_final_state(state2)
        enfa.add_transition(state0, symb_a, state1)
        enfa.add_transition(state0, symb_b, state1)
        enfa.add_transition(state0, symb_plus, state1)
        enfa.add_transition(state0, symb_c, state2)
        enfa.add_transition(state1, symb_b, state2)
        enfa.add_transition(state1, symb_c, state2)
        enfa.add_transition(state1, symb_b, state1)
        enfa.add_transition(state1, symb_c, state1)
        self.assertEqual(enfa.get_number_transitions(), 8)
        enfa.create_or_transitions()
        self.assertEqual(enfa.get_number_transitions(), 4)

    def test_remove_state(self):
        " Tests the remove of state """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        symb02 = Symbol("a+b")
        symb01 = Symbol("c*")
        symb11 = Symbol("b+(c.d)")
        symb12 = Symbol("a.b.c")
        enfa.add_start_state(state0)
        enfa.add_final_state(state2)
        enfa.add_transition(state0, symb01, state1)
        enfa.add_transition(state0, symb02, state2)
        enfa.add_transition(state1, symb11, state1)
        enfa.add_transition(state1, symb12, state2)
        enfa.remove_state(state1)
        self.assertEqual(enfa.get_number_transitions(), 1)
        self.assertEqual(enfa.get_number_states(), 2)


def get_digits_enfa():
    """ An epsilon NFA to recognize digits """
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
    return (enfa, digits, epsilon, plus, minus, point)
