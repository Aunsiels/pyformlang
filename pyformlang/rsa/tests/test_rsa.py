""" Tests for RSA """

import unittest

from pyformlang.finite_automaton.symbol import Symbol
from pyformlang.regular_expression import Regex

from pyformlang.rsa.recursive_automaton import RecursiveAutomaton
from pyformlang.rsa.box import Box


class TestRSA(unittest.TestCase):
    """ Test class for RSA """
    def test_creation(self):
        """ Test the creation of an RSA """
        # S -> a S b | a b
        enfa = Regex("a S b | a b").to_epsilon_nfa()
        dfa = enfa.minimize()
        box = Box(dfa, "S")
        rsa_1 = RecursiveAutomaton(box, {box})

        self.assertEqual(rsa_1.get_number_of_boxes(), 1)
        self.assertEqual(box, rsa_1.get_box_by_nonterminal("S"))
        self.assertEqual(rsa_1.nonterminals, {Symbol("S")})
        self.assertEqual(rsa_1.start_nonterminal, Symbol("S"))

        rsa_2 = RecursiveAutomaton.empty()
        rsa_2.add_box(box)
        rsa_2.change_start_nonterminal("S")

        self.assertEqual(rsa_2, rsa_1)

    def test_from_regex(self):
        """ Test creation of an RSA from a regex"""
        # S -> a*
        rsa_2 = RecursiveAutomaton.from_regex(Regex("a*"), "S")

        enfa = Regex("a*").to_epsilon_nfa()
        dfa = enfa.minimize()
        box = Box(dfa, "S")
        rsa_1 = RecursiveAutomaton(box, {box})

        self.assertEqual(rsa_2, rsa_1)

    def test_is_equals_to(self):
        """ Test the equivalence of two RSAs"""
        # S -> a* b*
        rsa_1 = RecursiveAutomaton.from_regex(Regex("a* b*"), "S")

        # S -> a+ b+
        rsa_2 = RecursiveAutomaton.from_regex(Regex("a a* b b*"), "S")

        self.assertNotEqual(rsa_1, rsa_2)

    def test_add_box(self):
        """ Test adding a box """
        rsa_1 = RecursiveAutomaton.from_regex(Regex("a* b*"), "S")
        new_box = Box(Regex("a*").to_epsilon_nfa().minimize(), "S")
        rsa_1.add_box(new_box)
        self.assertEqual(new_box.dfa, rsa_1.get_box_by_nonterminal("S").dfa)
        self.assertEqual(rsa_1.nonterminals, {Symbol("S")})

    def test_from_text(self):
        """ Test reading RSA from a text"""
        # g1: S -> a S b | a b
        rsa1_g1 = RecursiveAutomaton.from_ebnf("S -> a S b | a b")
        rsa2_g1 = RecursiveAutomaton.from_regex(
            Regex("a S b | a b"), "S")

        self.assertEqual(rsa1_g1, rsa2_g1)

        # g2: S -> a V b
        #     V -> c S d | c d
        rsa1_g2 = RecursiveAutomaton.from_ebnf("""
            S -> a V b
            V -> c S d | c d""")
        self.assertEqual(rsa1_g2.get_number_of_boxes(), 2)
        self.assertEqual(rsa1_g2.nonterminals, {Symbol("S"), Symbol("V")})

        dfa_s = Regex("a V b").to_epsilon_nfa().minimize()
        self.assertEqual(rsa1_g2.get_box_by_nonterminal("S"), Box(dfa_s, "S"))

        dfa_v = Regex("c S d | c d").to_epsilon_nfa().minimize()
        self.assertEqual(rsa1_g2.get_box_by_nonterminal("V"), Box(dfa_v, "V"))
