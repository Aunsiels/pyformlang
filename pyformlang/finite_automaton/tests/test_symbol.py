import unittest

from pyformlang.finite_automaton import Symbol


class TestSymbol(unittest.TestCase):

    def test_can_create(self):
        self.assertIsNotNone(Symbol(""))
        self.assertIsNotNone(Symbol(1))

    def test_repr(self):
        s1 = Symbol("ABC")
        self.assertEqual(str(s1), "ABC")
        s2 = Symbol(1)
        self.assertEqual(str(s2), "1")

    def test_eq(self):
        s1 = Symbol("ABC")
        s2 = Symbol(1)
        s3 = Symbol("ABC")
        self.assertEqual(s1, s3)
        self.assertNotEqual(s2, s3)
        self.assertNotEqual(s1, s2)

    def test_hash(self):
        s1 = hash(Symbol("ABC"))
        s2 = hash(Symbol(1))
        s3 = hash(Symbol("ABC"))
        self.assertIsInstance(s1, int)
        self.assertEqual(s1, s3)
        self.assertNotEqual(s2, s3)
        self.assertNotEqual(s1, s2)
