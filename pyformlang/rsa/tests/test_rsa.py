import unittest

from pyformlang.rsa.recursive_automaton import RecursiveAutomaton
from pyformlang.finite_automaton.symbol import Symbol
from pyformlang.regular_expression import Regex
from pyformlang.rsa.box import Box


class TestRSA(unittest.TestCase):
    def test_creation(self):
        # S -> a S b | a b
        enfa = Regex("a S b | a b").to_epsilon_nfa()
        dfa = enfa.minimize()
        box = Box(dfa, Symbol("S"))
        rsa_1 = RecursiveAutomaton({Symbol("S")}, Symbol("S"), {box})

        self.assertEqual(rsa_1.get_number_of_boxes(), 1)
        self.assertEqual(box.is_equivalent_to(rsa_1.get_box(Symbol("S"))), True)
        self.assertEqual(rsa_1.labels(), {Symbol("S")})
        self.assertEqual(rsa_1.initial_label(), Symbol("S"))

        rsa_2 = RecursiveAutomaton()
        rsa_2.add_box(box)
        rsa_2.change_initial_label(Symbol("S"))

        self.assertEqual(rsa_2.is_equivalent_to(rsa_1), True)

    def test_from_regex(self):
        # S -> a*
        rsa_2 = RecursiveAutomaton.from_regex("a*", Symbol("S"))

        enfa = Regex("a*").to_epsilon_nfa()
        dfa = enfa.minimize()
        box = Box(dfa, Symbol("S"))
        rsa_1 = RecursiveAutomaton({Symbol("S")}, Symbol("S"), {box})

        self.assertEqual(rsa_2.is_equivalent_to(rsa_1), True)

    def test_is_equivalent_to(self):
        # S -> a* b*
        rsa_1 = RecursiveAutomaton.from_regex("a* b*", Symbol("S"))

        # S -> a+ b+
        rsa_2 = RecursiveAutomaton.from_regex("a a* b b*", Symbol("S"))

        self.assertEqual(rsa_1.is_equivalent_to(rsa_2), False)


if __name__ == '__main__':
    unittest.main()
