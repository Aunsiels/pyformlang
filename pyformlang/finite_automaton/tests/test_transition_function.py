import unittest

from pyformlang.finite_automaton import State, Symbol, TransitionFunction,\
    DuplicateTransitionError


class TestTransitionFunction(unittest.TestCase):

    def test_creation(self):
        tf = TransitionFunction()
        self.assertIsNotNone(tf)

    def test_add_transitions(self):
        tf = TransitionFunction()
        s_from = State(0)
        s_to = State(1)
        s_to_bis = State(2)
        by = Symbol("a")
        tf.add_transition(s_from, by, s_to)
        tf.add_transition(s_from, by, s_to)
        with self.assertRaises(DuplicateTransitionError) as dte:
            tf.add_transition(s_from, by, s_to_bis)
        dte = dte.exception
        self.assertEqual(dte._s_from, s_from)
        self.assertEqual(dte._s_to, s_to_bis)
        self.assertEqual(dte._by, by)
        self.assertEqual(dte._s_to_old, s_to)

    def test_number_transitions(self):
        tf = TransitionFunction()
        self.assertEqual(tf.get_number_transitions(), 0)
        s_from = State(0)
        s_to = State(1)
        s_to_bis = State(2)
        by = Symbol("a")
        by2 = Symbol("b")
        tf.add_transition(s_from, by, s_to)
        self.assertEqual(tf.get_number_transitions(), 1)
        tf.add_transition(s_from, by, s_to)
        self.assertEqual(tf.get_number_transitions(), 1)
        tf.add_transition(s_from, by2, s_to_bis)
        self.assertEqual(tf.get_number_transitions(), 2)
        tf.add_transition(s_to, by, s_to_bis)
        self.assertEqual(tf.get_number_transitions(), 3)

    def test_remove_transitions(self):
        tf = TransitionFunction()
        s_from = State(0)
        s_to = State(1)
        by = Symbol("a")
        tf.add_transition(s_from, by, s_to)
        self.assertEqual(tf.remove_transition(s_from, by, s_to), 1)
        self.assertEqual(tf.get_number_transitions(), 0)
        self.assertIsNone(tf(s_to, by))
        self.assertEqual(tf.remove_transition(s_from, by, s_to), 0)

    def test_call(self):
        tf = TransitionFunction()
        s_from = State(0)
        s_to = State(1)
        by = Symbol("a")
        tf.add_transition(s_from, by, s_to)
        self.assertEqual(tf(s_from, by), s_to)
        self.assertIsNone(tf(s_to, by))
