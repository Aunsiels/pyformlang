"""
Tests the states
"""


import unittest

from pyformlang.finite_automaton import State


class TestState(unittest.TestCase):
    """ Test the states
    """

    def test_can_create(self):
        """ Tests the creation of states
        """
        self.assertIsNotNone(State(""))
        self.assertIsNotNone(State(1))

    def test_repr(self):
        """ Tests the representation of states
        """
        state1 = State("ABC")
        self.assertEqual(str(state1), "ABC")
        state2 = State(1)
        self.assertEqual(str(state2), "1")

    def test_eq(self):
        """ Tests the equality of states
        """
        state1 = State("ABC")
        state2 = State(1)
        state3 = State("ABC")
        self.assertEqual(state1, state3)
        self.assertFalse(state2 == 1)
        self.assertNotEqual(state2, state3)
        self.assertNotEqual(state2, 1)
        self.assertNotEqual(state1, state2)

    def test_hash(self):
        """ Tests the hashing of states
        """
        state1 = hash(State("ABC"))
        state2 = hash(State(1))
        state3 = hash(State("ABC"))
        self.assertIsInstance(state1, int)
        self.assertEqual(state1, state3)
        self.assertNotEqual(state2, state3)
        self.assertNotEqual(state1, state2)
