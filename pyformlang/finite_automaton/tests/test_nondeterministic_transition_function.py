"""
Test the nondeterministic transition functions
"""


import unittest

from pyformlang.finite_automaton import State, Symbol, \
    NondeterministicTransitionFunction


class TestNondeterministicTransitionFunction(unittest.TestCase):
    """ Tests the nondeterministic transitions functions
    """

    def test_creation(self):
        """ Tests the creation of nondeterministic transition functions
        """
        transition_function = NondeterministicTransitionFunction()
        self.assertIsNotNone(transition_function)

    def test_add_transitions(self):
        """ Tests the addition of transitions
        """
        transition_function = NondeterministicTransitionFunction()
        s_from = State(0)
        s_to = State(1)
        s_to_bis = State(2)
        symb_by = Symbol("a")
        transition_function.add_transition(s_from, symb_by, s_to)
        transition_function.add_transition(s_from, symb_by, s_to)
        transition_function.add_transition(s_from, symb_by, s_to_bis)
        transition_function.add_transition(s_to, symb_by, s_to)
        self.assertEqual(transition_function.get_number_transitions(), 3)

    def test_number_transitions(self):
        """ Tests the number of transitions
        """
        transition_function = NondeterministicTransitionFunction()
        self.assertEqual(transition_function.get_number_transitions(), 0)
        s_from = State(0)
        s_to = State(1)
        s_to_bis = State(2)
        symb_by = Symbol("a")
        symb_by2 = Symbol("b")
        transition_function.add_transition(s_from, symb_by, s_to)
        self.assertEqual(transition_function.get_number_transitions(), 1)
        transition_function.add_transition(s_from, symb_by, s_to)
        self.assertEqual(transition_function.get_number_transitions(), 1)
        transition_function.add_transition(s_from, symb_by2, s_to_bis)
        self.assertEqual(transition_function.get_number_transitions(), 2)
        transition_function.add_transition(s_to, symb_by, s_to_bis)
        self.assertEqual(transition_function.get_number_transitions(), 3)
        transition_function.add_transition(s_from, symb_by, s_from)
        self.assertEqual(transition_function.get_number_transitions(), 4)

    def test_remove_transitions(self):
        """ Tests the removal of transitions
        """
        transition_function = NondeterministicTransitionFunction()
        s_from = State(0)
        s_to = State(1)
        symb_by = Symbol("a")
        transition_function.add_transition(s_from, symb_by, s_to)
        self.assertEqual(transition_function.remove_transition(s_from, symb_by, s_to), 1)
        self.assertEqual(transition_function.get_number_transitions(), 0)
        self.assertEqual(len(transition_function(s_to, symb_by)), 0)
        self.assertEqual(len(transition_function(s_from, symb_by)), 0)
        self.assertEqual(transition_function.remove_transition(s_from, symb_by, s_to), 0)
        transition_function.add_transition(s_from, symb_by, s_to)
        transition_function.add_transition(s_from, symb_by, s_from)
        self.assertEqual(transition_function.remove_transition(s_from, symb_by, s_to), 1)
        self.assertEqual(transition_function.get_number_transitions(), 1)
        self.assertEqual(len(transition_function(s_from, symb_by)), 1)

    def test_call(self):
        """ Tests the call of a transition function
        """
        transition_function = NondeterministicTransitionFunction()
        s_from = State(0)
        s_to = State(1)
        symb_by = Symbol("a")
        transition_function.add_transition(s_from, symb_by, s_to)
        self.assertEqual(transition_function(s_from, symb_by), {s_to})
        self.assertEqual(len(transition_function(s_to, symb_by)), 0)
        transition_function.add_transition(s_from, symb_by, s_from)
        self.assertEqual(transition_function(s_from, symb_by), {s_to, s_from})
