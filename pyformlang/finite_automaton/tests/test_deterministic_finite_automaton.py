"""
Tests for the deterministic finite automata
"""

import unittest

from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton import TransitionFunction


class TestDeterministicFiniteAutomaton(unittest.TestCase):
    """ Tests for deterministic finite automata
    """

    def test_can_create(self):
        """ Test the creation of dfa
        """
        state0 = State("0")
        state1 = State("1")
        symb0 = Symbol("a")
        states = {state0, state1}
        input_symbols = {symb0}
        transition_function = TransitionFunction()
        transition_function.add_transition(state0, symb0, state1)
        start_state = state0
        final_states = {state1}
        dfa = DeterministicFiniteAutomaton(states,
                                           input_symbols,
                                           transition_function,
                                           start_state,
                                           final_states)
        self.assertIsNotNone(dfa)
        dfa = DeterministicFiniteAutomaton()
        self.assertIsNotNone(dfa)
        dfa = DeterministicFiniteAutomaton(start_state=state1,
                                           final_states={state0, state1})
        self.assertIsNotNone(dfa)

    def test_add_transition(self):
        """ Tests the addition of transitions
        """
        dfa = DeterministicFiniteAutomaton()
        self.assertEqual(dfa.get_number_states(), 0)
        state0 = State("0")
        state1 = State("1")
        symb = Symbol("a")
        dfa.add_transition(state0, symb, state1)
        self.assertEqual(dfa.get_number_states(), 2)
        self.assertEqual(dfa.get_number_symbols(), 1)

    def test_add_remove_initial_final(self):
        """ Tests the addition and removal of initial state and final states
        """
        dfa = DeterministicFiniteAutomaton()
        state0 = State("0")
        state1 = State("1")
        self.assertEqual(dfa.set_initial_state(state0), 1)
        self.assertEqual(dfa.get_number_states(), 1)
        self.assertEqual(dfa.add_final_state(state1), 1)
        self.assertEqual(dfa.get_number_states(), 2)
        self.assertEqual(dfa.remove_final_state(state0), 0)
        self.assertTrue(dfa.is_final_state(state1))
        self.assertFalse(dfa.is_final_state(state0))
        self.assertEqual(dfa.remove_final_state(state1), 1)
        self.assertFalse(dfa.is_final_state(state1))
        self.assertEqual(dfa.remove_final_state(state1), 0)

    def test_accepts(self):
        """ Tests the acceptance of dfa
        """
        dfa = DeterministicFiniteAutomaton()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        symb_d = Symbol("d")
        dfa.set_initial_state(state0)
        dfa.add_final_state(state2)
        dfa.add_final_state(state3)
        dfa.add_transition(state0, symb_a, state1)
        dfa.add_transition(state1, symb_b, state1)
        dfa.add_transition(state1, symb_c, state2)
        dfa.add_transition(state1, symb_d, state3)
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_c]))
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_b, symb_b, symb_c]))
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_d]))
        self.assertTrue(dfa.accepts([symb_a, symb_d]))
        self.assertFalse(dfa.accepts([symb_a, symb_c, symb_d]))
        self.assertFalse(dfa.accepts([symb_d, symb_c, symb_d]))
        self.assertFalse(dfa.accepts([]))
