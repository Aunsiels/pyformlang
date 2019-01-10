"""
Tests for the symbols
"""


import unittest

from pyformlang.finite_automaton import Symbol


class TestSymbol(unittest.TestCase):
    """ Tests for the symbols
    """

    def test_can_create(self):
        """ Tests the creation of symbols
        """
        self.assertIsNotNone(Symbol(""))
        self.assertIsNotNone(Symbol(1))

    def test_repr(self):
        """ Tests the representation of symbols
        """
        symbol1 = Symbol("ABC")
        self.assertEqual(str(symbol1), "ABC")
        symbol2 = Symbol(1)
        self.assertEqual(str(symbol2), "1")

    def test_eq(self):
        """ Tests equality of symbols
        """
        symbol1 = Symbol("ABC")
        symbol2 = Symbol(1)
        symbol3 = Symbol("ABC")
        self.assertEqual(symbol1, symbol3)
        self.assertFalse(symbol2 == 1)
        self.assertNotEqual(symbol2, symbol3)
        self.assertNotEqual(symbol2, 1)
        self.assertNotEqual(symbol1, symbol2)

    def test_hash(self):
        """ Tests the hashing of symbols
        """
        symbol1 = hash(Symbol("ABC"))
        symbol2 = hash(Symbol(1))
        symbol3 = hash(Symbol("ABC"))
        self.assertIsInstance(symbol1, int)
        self.assertEqual(symbol1, symbol3)
        self.assertNotEqual(symbol2, symbol3)
        self.assertNotEqual(symbol1, symbol2)
