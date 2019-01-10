"""
Tests for epsilon transitions
"""

import unittest

from pyformlang.finite_automaton import Epsilon
from pyformlang.finite_automaton import Symbol


class TestEpsilon(unittest.TestCase):
    """ Tests for epsilon transitions """

    def test_epsilon(self):
        """ Generic tests for epsilon """
        eps0 = Epsilon()
        eps1 = Epsilon()
        symb = Symbol(0)
        self.assertEqual(eps0, eps1)
        self.assertNotEqual(eps0, symb)
