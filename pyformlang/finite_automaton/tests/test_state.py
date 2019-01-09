import unittest

from pyformlang.finite_automaton import State


class TestState(unittest.TestCase):

    def test_can_create(self):
        self.assertIsNotNone(State(""))
        self.assertIsNotNone(State(1))

    def test_repr(self):
        s1 = State("ABC")
        self.assertEqual(str(s1), "ABC")
        s2 = State(1)
        self.assertEqual(str(s2), "1")

    def test_eq(self):
        s1 = State("ABC")
        s2 = State(1)
        s3 = State("ABC")
        self.assertEqual(s1, s3)
        self.assertFalse(s2 == 1)
        self.assertNotEqual(s2, s3)
        self.assertNotEqual(s2, 1)
        self.assertNotEqual(s1, s2)

    def test_hash(self):
        s1 = hash(State("ABC"))
        s2 = hash(State(1))
        s3 = hash(State("ABC"))
        self.assertIsInstance(s1, int)
        self.assertEqual(s1, s3)
        self.assertNotEqual(s2, s3)
        self.assertNotEqual(s1, s2)
