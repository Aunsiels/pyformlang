"""
Tests for regular expressions
"""

import unittest

from pyformlang.regular_expression import Regex, MisformedRegexError
from pyformlang import finite_automaton


class TestRegex(unittest.TestCase):
    """ Tests for regex """

    # pylint: disable=missing-function-docstring,too-many-public-methods

    def test_creation(self):
        """ Try to create regex """
        regex = Regex("a|b")
        self.assertEqual(regex.get_number_symbols(), 2)
        self.assertEqual(regex.get_number_operators(), 1)
        regex = Regex("a b")
        self.assertEqual(regex.get_number_symbols(), 2)
        self.assertEqual(regex.get_number_operators(), 1)
        regex = Regex("a b c")
        self.assertEqual(regex.get_number_symbols(), 3)
        self.assertEqual(regex.get_number_operators(), 2)
        regex = Regex("(a b)|c")
        self.assertEqual(regex.get_number_symbols(), 3)
        self.assertEqual(regex.get_number_operators(), 2)
        regex = Regex("")
        self.assertEqual(regex.get_number_symbols(), 1)
        self.assertEqual(regex.get_number_operators(), 0)
        regex = Regex("a*")
        self.assertEqual(regex.get_number_symbols(), 1)
        self.assertEqual(regex.get_number_operators(), 1)
        regex = Regex("a**")
        self.assertEqual(regex.get_number_symbols(), 1)
        self.assertEqual(regex.get_number_operators(), 2)
        regex = Regex("a*b|c")
        self.assertEqual(regex.get_number_symbols(), 3)
        self.assertEqual(regex.get_number_operators(), 3)
        regex = Regex("a*(b|c)")
        self.assertEqual(regex.get_number_symbols(), 3)
        self.assertEqual(regex.get_number_operators(), 3)
        regex = Regex("a*.(b|c)")
        self.assertEqual(regex.get_number_symbols(), 3)
        self.assertEqual(regex.get_number_operators(), 3)
        regex = Regex("a*.(b|c)epsilon")
        self.assertEqual(regex.get_number_symbols(), 4)
        self.assertEqual(regex.get_number_operators(), 4)
        regex = Regex("$")
        self.assertEqual(regex.get_number_symbols(), 1)
        regex = Regex("a|")
        self.assertEqual(regex.get_number_symbols(), 2)
        self.assertEqual(regex.get_number_operators(), 1)
        with self.assertRaises(MisformedRegexError):
            Regex(")a b()")
        with self.assertRaises(MisformedRegexError):
            Regex("(a b()")
        with self.assertRaises(MisformedRegexError):
            Regex("(a b))")
        with self.assertRaises(MisformedRegexError):
            Regex("| a b")
        regex = Regex("(a-|a a b)")
        self.assertEqual(regex.get_number_symbols(), 4)
        self.assertEqual(regex.get_number_operators(), 3)

    def test_to_enfa0(self):
        """ Tests the transformation to a regex """
        symb_a = finite_automaton.Symbol("a")
        symb_b = finite_automaton.Symbol("b")
        symb_c = finite_automaton.Symbol("c")
        epsilon = finite_automaton.Epsilon()
        regex = Regex("a|b")
        enfa = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([symb_a]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([epsilon]))
        self.assertFalse(enfa.accepts([symb_a, symb_b]))
        regex = Regex("a b")
        enfa = regex.to_epsilon_nfa()
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        regex = Regex("a b c")
        enfa = regex.to_epsilon_nfa()
        self.assertFalse(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_b, symb_c]))
        self.assertFalse(enfa.accepts([symb_a, symb_b, symb_a]))
        regex = Regex("(a b)|c")
        enfa = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_a, symb_c]))
        self.assertFalse(enfa.accepts([symb_b, symb_c]))
        self.assertTrue(enfa.accepts([symb_c]))
        regex = Regex("")
        enfa = regex.to_epsilon_nfa()
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([]))
        regex = Regex("a*")
        enfa = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([symb_a]))
        self.assertTrue(enfa.accepts([]))
        self.assertTrue(enfa.accepts([symb_a, symb_a]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_a]))

    def test_to_enfa1(self):
        """ Tests the transformation to a regex """
        symb_a = finite_automaton.Symbol("a")
        symb_b = finite_automaton.Symbol("b")
        symb_c = finite_automaton.Symbol("c")
        regex = Regex("a**")
        enfa = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([symb_a]))
        self.assertTrue(enfa.accepts([]))
        self.assertTrue(enfa.accepts([symb_a, symb_a]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_a]))
        regex = Regex("a*b|c")
        enfa = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([symb_a, symb_a, symb_c]))
        regex = Regex("a*(b|c)")
        enfa = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_c]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_c]))
        regex = Regex("a*.(b|c)")
        enfa = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_c]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_c]))
        regex = Regex("a*.(b|c)epsilon")
        enfa = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_c]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_c]))
        regex = Regex("$")
        enfa = regex.to_epsilon_nfa()
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_c]))
        self.assertTrue(enfa.accepts([]))

    def test_print(self):
        """ Test printing functions """
        regex = Regex("a*.(b|c)epsilon")
        tree_str = regex.get_tree_str()
        self.assertTrue("Concatenation" in tree_str)
        self.assertTrue("Union" in tree_str)
        self.assertTrue("Kleene Star" in tree_str)
        self.assertTrue("Symbol" in tree_str)
        regex = Regex("")
        tree_str = regex.get_tree_str()
        self.assertTrue("Empty" in tree_str)

    def test_get_repr(self):
        regex0 = Regex("a*.(b|c)epsilon")
        regex_str = str(regex0)
        regex1 = Regex(regex_str)
        dfa0 = regex0.to_epsilon_nfa().to_deterministic().minimize()
        dfa1 = regex1.to_epsilon_nfa().to_deterministic().minimize()
        self.assertEqual(dfa0, dfa1)

    def test_accepts(self):
        regex = Regex("a|b|c")
        self.assertTrue(regex.accepts(["a"]))
        self.assertFalse(regex.accepts(["a", "b"]))

    def test_from_python_simple(self):
        regex = Regex.from_python_regex("abc")
        self.assertTrue(regex.accepts(["a", "b", "c"]))
        self.assertFalse(regex.accepts(["a", "b", "b"]))
        self.assertFalse(regex.accepts(["a", "b"]))

    def test_from_python_brackets(self):
        regex = Regex.from_python_regex("a[bc]")
        self.assertTrue(regex.accepts(["a", "b"]))
        self.assertTrue(regex.accepts(["a", "c"]))
        self.assertFalse(regex.accepts(["a", "b", "c"]))
        self.assertFalse(regex.accepts(["a", "a"]))

    def test_space(self):
        regex = Regex("\\ ")
        self.assertTrue(regex.accepts([" "]))

    def test_parenthesis_gorilla(self):
        regex = Regex("george touches (a|an) (sky|gorilla) !")
        self.assertTrue(regex.accepts(["george", "touches", "a", "sky", "!"]))

    def test_regex_or(self):
        regex = Regex("a|b")
        self.assertTrue(regex.accepts(["a"]))

    def test_regex_or_concat(self):
        regex = Regex("c (a|b)")
        self.assertTrue(regex.accepts(["c", "b"]))

    def test_regex_two_or_concat(self):
        regex = Regex("c (a|b) (d|e)")
        self.assertTrue(regex.accepts(["c", "b", "e"]))

    def test_regex_two_or_concat_parenthesis(self):
        regex = Regex("c.(a|b)(d|e)")
        self.assertTrue(regex.accepts(["c", "b", "e"]))

    def test_regex_two_or_concat_parenthesis2(self):
        regex = Regex("c (a|(b d)|e)")
        self.assertTrue(regex.accepts(["c", "a"]))
        self.assertTrue(regex.accepts(["c", "b", "d"]))
        self.assertTrue(regex.accepts(["c", "e"]))

    def test_regex_two_or_concat_parenthesis2_concat(self):
        regex = Regex("c (a|(b d)|e) !")
        self.assertTrue(regex.accepts(["c", "a", "!"]))
        self.assertTrue(regex.accepts(["c", "b", "d", "!"]))
        self.assertTrue(regex.accepts(["c", "e", "!"]))

    def test_regex_or_two_concat(self):
        regex = Regex("c d (a|b)")
        self.assertTrue(regex.accepts(["c", "d", "b"]))

    def test_after_union(self):
        regex = Regex("(a|b) !")
        self.assertTrue(regex.accepts(["a", "!"]))

    def test_star_union(self):
        regex = Regex("a*(b|c)")
        self.assertTrue(regex.accepts(["a", "a", "c"]))

    def test_misformed(self):
        with self.assertRaises(MisformedRegexError):
            Regex(")")

    def test_misformed2(self):
        with self.assertRaises(MisformedRegexError):
            Regex("(")

    def test_escaped_parenthesis(self):
        regex = Regex("\\(")
        self.assertTrue(regex.accepts(["("]))

    def test_escaped_mid_bar(self):
        regex = Regex('a(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q'
                      '|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|'
                      'S|T|U|V|W|X|Y|Z|!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|'
                      '\\.|/|:|;|<|=|>|?|@|[|\\|]|^|_|`|{|\\||}|~|\\ |	|)')
        self.assertTrue(regex.accepts(["a", "|"]))

    def test_to_cfg(self):
        regex = Regex("a")
        cfg = regex.to_cfg()
        self.assertTrue(cfg.contains(["a"]))
        regex = Regex("a|b")
        cfg = regex.to_cfg()
        self.assertTrue(cfg.contains(["b"]))
        regex = Regex("a b")
        cfg = regex.to_cfg()
        self.assertTrue(cfg.contains(["a", "b"]))
        regex = Regex("a*")
        cfg = regex.to_cfg()
        self.assertTrue(cfg.contains([]))
        self.assertTrue(cfg.contains(["a"]))
        self.assertTrue(cfg.contains(["a", "a"]))
        regex = Regex("epsilon")
        cfg = regex.to_cfg()
        self.assertTrue(cfg.contains([]))
        regex = Regex("")
        cfg = regex.to_cfg()
        self.assertTrue(cfg.is_empty())
        regex = Regex("(a|b)* c")
        cfg = regex.to_cfg()
        self.assertTrue(cfg.contains(["c"]))
        self.assertTrue(cfg.contains(["a", "c"]))
        self.assertTrue(cfg.contains(["a", "b", "c"]))

    def test_priority(self):
        self.assertTrue(Regex('b a* | a').accepts('a'))
        self.assertTrue(Regex('b a* | a').accepts('b'))
        self.assertTrue(Regex('(b a*) | a').accepts('a'))
