"""
Tests for regular expressions
"""

import unittest

from pyformlang.regular_expression import Regex, MisformedRegexError


class TestRegex(unittest.TestCase):
    """ Tests for regex """

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
        with self.assertRaises(MisformedRegexError):
            Regex(")a b()")
        with self.assertRaises(MisformedRegexError):
            Regex("(a b()")
        with self.assertRaises(MisformedRegexError):
            Regex("(a b))")
        with self.assertRaises(MisformedRegexError):
            Regex("| a b")
