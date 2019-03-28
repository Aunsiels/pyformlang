"""
Tests for epsilon NFA
"""

import unittest

from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon
from ..regexable import Regexable


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

        self.assertTrue(enfa.accepts(["+", digits[1], ".", digits[9]]))
        self.assertTrue(enfa.accepts(["-", digits[1], ".", digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], ".", digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], "."]))
        self.assertTrue(enfa.accepts([digits[1], ".", "epsilon"]))
        self.assertTrue(enfa.accepts([".", digits[9]]))
        self.assertFalse(enfa.accepts(["."]))
        self.assertFalse(enfa.accepts(["+"]))

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
        enfa.remove_all_basic_states()
        self.assertEqual(enfa.get_number_transitions(), 1)
        self.assertEqual(enfa.get_number_states(), 2)

    def test_to_regex(self):
        """ Tests the transformation to regex """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        symb_e = Symbol("e")
        symb_f = Symbol("f")
        symb_g = Symbol("g")
        enfa.add_start_state(state0)
        enfa.add_final_state(state2)
        enfa.add_transition(state0, symb_e, state1)
        enfa.add_transition(state1, symb_f, state2)
        enfa.add_transition(state0, symb_g, state2)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa2.accepts([symb_e, symb_f]))
        self.assertTrue(enfa2.accepts([symb_g]))
        self.assertFalse(enfa2.accepts([]))
        self.assertFalse(enfa2.accepts([symb_e]))
        self.assertFalse(enfa2.accepts([symb_f]))
        enfa.add_final_state(state0)
        with self.assertRaises(ValueError) as _:
            enfa.get_regex_simple()
        regex = enfa.to_regex()
        enfa3 = regex.to_epsilon_nfa()
        self.assertTrue(enfa3.accepts([symb_e, symb_f]))
        self.assertTrue(enfa3.accepts([symb_g]))
        self.assertTrue(enfa3.accepts([]))
        self.assertFalse(enfa3.accepts([symb_e]))
        self.assertFalse(enfa3.accepts([symb_f]))
        enfa.remove_start_state(state0)
        regex = enfa.to_regex()
        enfa3 = regex.to_epsilon_nfa()
        self.assertFalse(enfa3.accepts([symb_e, symb_f]))
        self.assertFalse(enfa3.accepts([symb_g]))
        self.assertFalse(enfa3.accepts([]))
        self.assertFalse(enfa3.accepts([symb_e]))
        self.assertFalse(enfa3.accepts([symb_f]))
        enfa.add_start_state(state0)
        enfa.add_transition(state0, symb_f, state0)
        regex = enfa.to_regex()
        enfa3 = regex.to_epsilon_nfa()
        self.assertTrue(enfa3.accepts([symb_e, symb_f]))
        self.assertTrue(enfa3.accepts([symb_f, symb_e, symb_f]))
        self.assertTrue(enfa3.accepts([symb_g]))
        self.assertTrue(enfa3.accepts([symb_f, symb_f, symb_g]))
        self.assertTrue(enfa3.accepts([]))
        self.assertFalse(enfa3.accepts([symb_e]))
        self.assertTrue(enfa3.accepts([symb_f]))

    def test_to_regex2(self):
        """ Tests the transformation to regex """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("0")
        symb_b = Symbol("1")
        enfa.add_start_state(state0)
        enfa.add_final_state(state1)
        enfa.add_transition(state0, symb_a, state0)
        enfa.add_transition(state0, symb_a, state1)
        enfa.add_transition(state1, symb_b, state0)
        enfa.add_transition(state1, symb_b, state1)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa2.accepts([symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b, symb_b]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b, symb_b, symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b, symb_b, symb_a, symb_b]))
        self.assertFalse(enfa2.accepts([symb_b]))

    def test_to_regex3(self):
        """ Tests the transformation to regex """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("0")
        symb_b = Symbol("1")
        enfa.add_start_state(state0)
        enfa.add_final_state(state1)
        enfa.add_transition(state0, symb_a, state0)
        enfa.add_transition(state1, symb_b, state0)
        enfa.add_transition(state1, symb_b, state1)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertFalse(enfa2.accepts([symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b, symb_b, symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b, symb_b, symb_a, symb_b]))
        self.assertFalse(enfa2.accepts([symb_b]))
        epsilon = Epsilon()
        enfa.add_transition(state0, epsilon, state1)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([]))
        self.assertTrue(enfa.accepts([symb_a]))
        self.assertTrue(enfa2.accepts([symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b, symb_b]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b, symb_b, symb_a, symb_b]))
        self.assertTrue(enfa2.accepts([symb_b]))
        self.assertTrue(enfa2.accepts([]))
        enfa.remove_transition(state0, symb_a, state0)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertFalse(enfa2.accepts([symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b, symb_b, symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b, symb_b, symb_a, symb_b]))
        self.assertTrue(enfa2.accepts([symb_b]))
        self.assertTrue(enfa2.accepts([]))
        enfa.remove_transition(state1, symb_b, state1)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa2.accepts([symb_b, symb_b]))
        enfa.add_transition(state0, symb_a, state0)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa2.accepts([symb_a, symb_b]))

    def test_union(self):
        """ Tests the union of two epsilon NFA """
        with self.assertRaises(NotImplementedError) as _:
            Regexable().to_regex()
        enfa0 = get_enfa_example0()
        enfa1 = get_enfa_example1()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        enfa = enfa0.union(enfa1)
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([]))

    def test_concatenate(self):
        """ Tests the concatenation of two epsilon NFA """
        enfa0 = get_enfa_example0()
        enfa1 = get_enfa_example1()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        enfa = enfa0.concatenate(enfa1)
        self.assertTrue(enfa.accepts([symb_b, symb_c]))
        self.assertTrue(enfa.accepts([symb_a, symb_b, symb_c]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b, symb_c]))
        self.assertFalse(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([]))

    def test_kleene(self):
        """ Tests the kleene star of an epsilon NFA """
        enfa0 = get_enfa_example0()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        enfa = enfa0.kleene_star()
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_b, symb_a, symb_b]))
        self.assertTrue(enfa.accepts([]))
        self.assertTrue(enfa.accepts([symb_b, symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([symb_a, symb_b, symb_a]))

    def test_complement(self):
        """ Tests the complement operation """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        symb_a = Symbol("a")
        enfa.add_start_state(state0)
        enfa.add_final_state(state2)
        enfa.add_transition(state0, Epsilon(), state1)
        enfa.add_transition(state1, symb_a, state2)
        enfa_comp = enfa.get_complement()
        self.assertFalse(enfa_comp.accepts([symb_a]))

    def test_intersection(self):
        """ Tests the intersection of two enfas """
        enfa0 = get_enfa_example0()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        eps = Epsilon()
        enfa1 = EpsilonNFA()
        state0 = State(10)
        state1 = State(11)
        state2 = State(12)
        state3 = State(13)
        state4 = State(14)
        enfa1.add_start_state(state0)
        enfa1.add_final_state(state3)
        enfa1.add_final_state(state4)
        enfa1.add_transition(state0, eps, state1)
        enfa1.add_transition(state1, symb_a, state2)
        enfa1.add_transition(state2, eps, state3)
        enfa1.add_transition(state3, symb_b, state4)
        enfa = enfa0.get_intersection(enfa1)
        self.assertEqual(len(enfa.get_start_states()), 4)
        self.assertEqual(len(enfa.get_final_states()), 2)
        self.assertEqual(len(enfa.get_symbols()), 2)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([]))
        self.assertFalse(enfa.accepts([symb_a, symb_a, symb_b]))

    def test_difference(self):
        """ Tests the intersection of two languages """
        enfa0 = get_enfa_example0()
        enfa1 = get_enfa_example1()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        enfa = enfa0.get_difference(enfa1)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([]))
        enfa2 = EpsilonNFA()
        state0 = State(0)
        enfa2.add_start_state(state0)
        enfa2.add_final_state(state0)
        enfa2.add_transition(state0, symb_b, state0)
        enfa = enfa0.get_difference(enfa2)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_c]))

    def test_reverse(self):
        """ Test the reversal of a language """
        enfa0 = get_enfa_example0()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        enfa = enfa0.reverse()
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_b, symb_a]))
        self.assertTrue(enfa.accepts([symb_b, symb_a, symb_a]))
        self.assertFalse(enfa.accepts([symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([]))

    def test_empty(self):
        """ Tests the emptiness of a finite automaton """
        self.assertFalse(get_enfa_example0().is_empty())
        self.assertFalse(get_enfa_example1().is_empty())
        enfa = EpsilonNFA()
        state0 = State(0)
        enfa.add_start_state(state0)
        self.assertTrue(enfa.is_empty())
        state1 = State(1)
        symb_a = Symbol('a')
        enfa.add_transition(state0, symb_a, state1)
        self.assertTrue(enfa.is_empty())
        enfa.add_final_state(state1)
        self.assertFalse(enfa.is_empty())

    def test_minimization(self):
        """ Tests the minimization algorithm """
        enfa = get_enfa_example0_bis()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        enfa = enfa.minimize()
        self.assertTrue(enfa.is_deterministic())
        self.assertEqual(enfa.get_number_states(), 2)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        enfa = get_example_non_minimal()
        enfa = enfa.minimize()
        self.assertTrue(enfa.is_deterministic())
        self.assertEqual(enfa.get_number_states(), 3)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        enfa = EpsilonNFA()
        enfa = enfa.minimize()
        self.assertTrue(enfa.is_deterministic())
        self.assertEqual(enfa.get_number_states(), 0)
        self.assertFalse(enfa.accepts([]))


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

def get_enfa_example0():
    """ Gives an example ENFA
    Accepts a*b
    """
    enfa0 = EpsilonNFA()
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    enfa0.add_start_state(state0)
    enfa0.add_final_state(state2)
    enfa0.add_transition(state0, symb_a, state0)
    enfa0.add_transition(state0, Epsilon(), state1)
    enfa0.add_transition(state1, symb_b, state2)
    return enfa0

def get_enfa_example1():
    """ Gives and example ENFA
    Accepts c
    """
    enfa1 = EpsilonNFA()
    state2 = State(2)
    state3 = State(3)
    symb_c = Symbol("c")
    enfa1.add_start_state(state2)
    enfa1.add_final_state(state3)
    enfa1.add_transition(state2, symb_c, state3)
    return enfa1

def get_enfa_example0_bis():
    """ A non minimal NFA, equivalent to example0 """
    enfa0 = EpsilonNFA()
    state3 = State(3)
    state4 = State(4)
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    enfa0.add_start_state(state0)
    enfa0.add_final_state(state2)
    enfa0.add_final_state(state4)
    enfa0.add_transition(state0, symb_a, state0)
    enfa0.add_transition(state0, Epsilon(), state1)
    enfa0.add_transition(state1, symb_b, state2)
    # New part
    enfa0.add_transition(state0, Epsilon(), state3)
    enfa0.add_transition(state3, symb_a, state3)
    enfa0.add_transition(state3, symb_b, state4)
    return enfa0

def get_example_non_minimal():
    """ A non minimal example a.a*.b"""
    enfa0 = EpsilonNFA()
    state0 = State(0)
    state3 = State(3)
    state4 = State(4)
    state5 = State(5)
    state6 = State(6)
    state1 = State(1)
    state2 = State(2)
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    enfa0.add_start_state(state0)
    enfa0.add_final_state(state3)
    enfa0.add_final_state(state4)
    enfa0.add_transition(state0, symb_a, state1)
    enfa0.add_transition(state1, symb_a, state2)
    enfa0.add_transition(state2, symb_a, state5)
    enfa0.add_transition(state5, symb_a, state6)
    enfa0.add_transition(state6, symb_a, state1)
    enfa0.add_transition(state1, symb_b, state3)
    enfa0.add_transition(state2, symb_b, state4)
    enfa0.add_transition(state5, symb_b, state3)
    enfa0.add_transition(state6, symb_b, state4)
    return enfa0
