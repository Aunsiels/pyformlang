"""
Tests for regular expressions
"""

import unittest

from pyformlang.regular_expression import Regex, MisformedRegexError


class TestRegex(unittest.TestCase):
    """ Tests for regex """

    def test_creation(self):
        """ Try to create regex """
        Regex("a|b")
        Regex("a b")
        Regex("a b c")
        Regex("(a b)|c")
        Regex("")
        Regex("a*")
        Regex("a**")
        Regex("a*b|c")
        Regex("a*(b|c)")
        Regex("a*.(b|c)")
        Regex("a*.(b|c)epsilon")
        Regex("$")
        with self.assertRaises(MisformedRegexError):
            Regex(")a b()")
        with self.assertRaises(MisformedRegexError):
            Regex("(a b()")
        with self.assertRaises(MisformedRegexError):
            Regex("(a b))")
        with self.assertRaises(MisformedRegexError):
            Regex("| a b")
