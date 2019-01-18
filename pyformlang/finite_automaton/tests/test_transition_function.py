"""
Test the transition functions
"""


import unittest

from pyformlang.finite_automaton import State, Symbol, TransitionFunction,\
    DuplicateTransitionError


class TestTransitionFunction(unittest.TestCase):
    """ Tests the transitions functions
    """

    def test_creation(self):
        """ Tests the creation of transition functions
        """
        transition_function = TransitionFunction()
        self.assertIsNotNone(transition_function)

    # pylint: disable=protected-access
    def test_add_transitions(self):
        """ Tests the addition of transitions
        """
        transition_function = TransitionFunction()
        s_from = State(10)
        s_to = State(11)
        s_to_bis = State(2)
        symb_by = Symbol("abc")
        transition_function.add_transition(s_from, symb_by, s_to)
        transition_function.add_transition(s_from, symb_by, s_to)
        with self.assertRaises(DuplicateTransitionError) as dte:
            transition_function.add_transition(s_from, symb_by, s_to_bis)
        dte = dte.exception
        self.assertEqual(dte.s_from, s_from)
        self.assertEqual(dte.s_to, s_to_bis)
        self.assertEqual(dte.symb_by, symb_by)
        self.assertEqual(dte.s_to_old, s_to)

    def test_number_transitions(self):
        """ Tests the number of transitions
        """
        transition_function = TransitionFunction()
        self.assertEqual(transition_function.get_number_transitions(), 0)
        s_from = State(110)
        s_to = State(12)
        s_to_bis = State(2)
        symb_by = Symbol("a")
        transition_function.add_transition(s_from, symb_by, s_to)
        self.assertEqual(transition_function.get_number_transitions(), 1)
        transition_function.add_transition(s_from, symb_by, s_to)
        self.assertEqual(transition_function.get_number_transitions(), 1)
        symb_by2 = Symbol("bc")
        transition_function.add_transition(s_from, symb_by2, s_to_bis)
        self.assertEqual(transition_function.get_number_transitions(), 2)
        transition_function.add_transition(s_to, symb_by, s_to_bis)
        self.assertEqual(transition_function.get_number_transitions(), 3)

    def test_remove_transitions(self):
        """ Tests the removal of transitions
        """
        transition_function = TransitionFunction()
        s_from = State(10)
        s_to = State(11)
        symb_by = Symbol("abc")
        transition_function.add_transition(s_from, symb_by, s_to)
        self.assertEqual(transition_function.remove_transition(s_from, symb_by, s_to), 1)
        self.assertEqual(transition_function.get_number_transitions(), 0)
        self.assertEqual(transition_function(s_to, symb_by), [])
        self.assertEqual(transition_function(s_from, symb_by), [])
        self.assertEqual(transition_function.remove_transition(s_from, symb_by, s_to), 0)

    def test_call(self):
        """ Tests the call of a transition function
        """
        transition_function = TransitionFunction()
        s_from = State(0)
        s_to = State(1)
        symb_by = Symbol("a")
        transition_function.add_transition(s_from, symb_by, s_to)
        self.assertEqual(transition_function(s_from, symb_by), [s_to])
        self.assertEqual(transition_function(s_to, symb_by), [])
