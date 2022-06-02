import unittest

from pyformlang.finite_automaton.symbol import Symbol
from pyformlang.regular_expression import Regex
from pyformlang.cfg import CFG

from pyformlang.rsa.recursive_automaton import RecursiveAutomaton
from pyformlang.rsa.box import Box


class TestRSA(unittest.TestCase):
    def test_creation(self):
        # S -> a S b | a b
        enfa = Regex("a S b | a b").to_epsilon_nfa()
        dfa = enfa.minimize()
        box = Box(dfa, Symbol("S"))
        rsa_1 = RecursiveAutomaton({Symbol("S")}, Symbol("S"), {box})

        self.assertEqual(rsa_1.get_number_of_boxes(), 1)
        self.assertEqual(box, rsa_1.get_box(Symbol("S")))
        self.assertEqual(rsa_1.labels, {Symbol("S")})
        self.assertEqual(rsa_1.initial_label, Symbol("S"))

        rsa_2 = RecursiveAutomaton()
        rsa_2.add_box(box)
        rsa_2.change_initial_label(Symbol("S"))

        self.assertEqual(rsa_2, rsa_1)

        # Checking to add a start label
        rsa_3 = RecursiveAutomaton(set(), Symbol("S"), {box})
        self.assertEqual(rsa_3.labels, {Symbol("S")})

        try:
            rsa_4 = RecursiveAutomaton({Symbol("S"), Symbol("v")}, Symbol("S"), {box})
        except ValueError:
            self.assertEqual(True, True)

    def test_from_regex(self):
        # S -> a*
        rsa_2 = RecursiveAutomaton.from_regex(Regex("a*"), Symbol("S"))

        enfa = Regex("a*").to_epsilon_nfa()
        dfa = enfa.minimize()
        box = Box(dfa, Symbol("S"))
        rsa_1 = RecursiveAutomaton({Symbol("S")}, Symbol("S"), {box})

        self.assertEqual(rsa_2, rsa_1)

    def test_is_equivalent_to(self):
        # S -> a* b*
        rsa_1 = RecursiveAutomaton.from_regex(Regex("a* b*"), Symbol("S"))

        # S -> a+ b+
        rsa_2 = RecursiveAutomaton.from_regex(Regex("a a* b b*"), Symbol("S"))

        self.assertNotEqual(rsa_1, rsa_2)

    def test_add_box(self):
        rsa_1 = RecursiveAutomaton.from_regex(Regex("a* b*"), Symbol("S"))
        new_box = Box(Regex("a*").to_epsilon_nfa().minimize(), Symbol("S"))
        rsa_1.add_box(new_box)
        self.assertEqual(new_box.dfa, rsa_1.get_box(Symbol("S")).dfa)
        self.assertEqual(rsa_1.labels, {Symbol("S")})

    def test_from_text(self):
        # g1: S -> a S b | a b
        rsa1_g1 = RecursiveAutomaton.from_text("S -> a S b | a b")
        rsa2_g1 = RecursiveAutomaton.from_regex(Regex("a S b | a b"), Symbol("S"))

        self.assertEqual(rsa1_g1, rsa2_g1)

        # g2: S -> a V b
        #     V -> c S d | c d
        rsa1_g2 = RecursiveAutomaton.from_cfg(
            CFG.from_text("""
                S -> a V b
                V -> c S d | c d"""))
        self.assertEqual(rsa1_g2.get_number_of_boxes(), 2)
        self.assertEqual(rsa1_g2.labels, {Symbol("S"), Symbol("V")})

        dfa_S = Regex("a V b").to_epsilon_nfa().minimize()
        self.assertEqual(rsa1_g2.get_box(Symbol("S")), Box(dfa_S, Symbol("S")))

        dfa_V = Regex("c S d | c d").to_epsilon_nfa().minimize()
        self.assertEqual(rsa1_g2.get_box(Symbol("V")), Box(dfa_V, Symbol("V")))
