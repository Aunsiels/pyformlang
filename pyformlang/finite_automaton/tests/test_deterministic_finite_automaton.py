import unittest

from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton import TransitionFunction


class TestDeterministicFiniteAutomaton(unittest.TestCase):

    def test_can_create(self):
        s0 = State("0")
        s1 = State("1")
        symb0 = Symbol("a")
        states = {s0, s1}
        input_symbols = {symb0}
        tf = TransitionFunction()
        tf.add_transition(s0, symb0, s1)
        start_state = s0
        final_states = {s1}
        dfa = DeterministicFiniteAutomaton(states,
                                           input_symbols,
                                           tf,
                                           start_state,
                                           final_states)
        self.assertIsNotNone(dfa)
        dfa = DeterministicFiniteAutomaton()
        self.assertIsNotNone(dfa)
        dfa = DeterministicFiniteAutomaton(start_state=s1,
                                           final_states={s0, s1})
        self.assertIsNotNone(dfa)

    def test_add_transition(self):
        dfa = DeterministicFiniteAutomaton()
        self.assertEqual(dfa.get_number_states(), 0)
        s0 = State("0")
        s1 = State("1")
        symb = Symbol("a")
        dfa.add_transition(s0, symb, s1)
        self.assertEqual(dfa.get_number_states(), 2)
        self.assertEqual(dfa.get_number_symbols(), 1)

    def test_add_remove_initial_final(self):
        dfa = DeterministicFiniteAutomaton()
        s0 = State("0")
        s1 = State("1")
        self.assertEqual(dfa.set_initial_state(s0), 1)
        self.assertEqual(dfa.get_number_states(), 1)
        self.assertEqual(dfa.add_final_state(s1), 1)
        self.assertEqual(dfa.get_number_states(), 2)
        self.assertEqual(dfa.remove_final_state(s0), 0)
        self.assertTrue(dfa._is_final_state(s1))
        self.assertFalse(dfa._is_final_state(s0))
        self.assertEqual(dfa.remove_final_state(s1), 1)
        self.assertFalse(dfa._is_final_state(s1))
        self.assertEqual(dfa.remove_final_state(s1), 0)

    def test_accepts(self):
        dfa = DeterministicFiniteAutomaton()
        s0 = State(0)
        s1 = State(1)
        s2 = State(2)
        s3 = State(3)
        a = Symbol("a")
        b = Symbol("b")
        c = Symbol("c")
        d = Symbol("d")
        dfa.set_initial_state(s0)
        dfa.add_final_state(s2)
        dfa.add_final_state(s3)
        dfa.add_transition(s0, a, s1)
        dfa.add_transition(s1, b, s1)
        dfa.add_transition(s1, c, s2)
        dfa.add_transition(s1, d, s3)
        self.assertTrue(dfa.accepts([a, b, c]))
        self.assertTrue(dfa.accepts([a, b, b, b, c]))
        self.assertTrue(dfa.accepts([a, b, d]))
        self.assertTrue(dfa.accepts([a, d]))
        self.assertFalse(dfa.accepts([a, c, d]))
        self.assertFalse(dfa.accepts([d, c, d]))
        self.assertFalse(dfa.accepts([]))
