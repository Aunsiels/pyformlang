import unittest

from pyformlang.finite_automaton import DeterministicFiniteAutomaton


class TestDeterministicFiniteAutomaton(unittest.TestCase):

    def test_can_create(self):
        dfa = DeterministicFiniteAutomaton(None, None, None, None, None)
        self.assertIsNotNone(dfa)
