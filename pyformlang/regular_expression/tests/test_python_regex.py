"""
Testing python regex parsing
"""
import re
import unittest

from pyformlang.regular_expression.python_regex import PythonRegex


class TestPythonRegex(unittest.TestCase):
    """ Tests for python regex """

    # pylint: disable=missing-function-docstring, too-many-public-methods

    def test_with_brackets(self):
        regex = PythonRegex("a[bc]")
        self.assertTrue(regex.accepts(["a", "b"]))
        self.assertTrue(regex.accepts(["a", "c"]))
        self.assertFalse(regex.accepts(["a", "b", "c"]))
        self.assertFalse(regex.accepts(["a", "a"]))

    def test_range_in_brackets(self):
        regex = PythonRegex("a[a-z]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", "c"]))
        self.assertTrue(regex.accepts(["a", "g"]))
        self.assertTrue(regex.accepts(["a", "z"]))
        self.assertFalse(regex.accepts(["a", "b", "c"]))
        self.assertFalse(regex.accepts(["a", "A"]))

    def test_range_in_brackets_trap(self):
        regex = PythonRegex("a[a-e-z]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", "c"]))
        self.assertTrue(regex.accepts(["a", "z"]))
        self.assertTrue(regex.accepts(["a", "-"]))
        self.assertFalse(regex.accepts(["a", "y"]))
        self.assertFalse(regex.accepts(["a", "f"]))

    def test_range_in_brackets_trap2(self):
        regex = PythonRegex("[a-e-g-z]*")
        self.assertTrue(regex.accepts(["a", "-", "y"]))

    def test_range_in_brackets_trap2_bis(self):
        regex = PythonRegex(re.compile("[a-e-g-z]*"))
        self.assertTrue(regex.accepts(["a", "-", "y"]))

    def test_parenthesis(self):
        regex = PythonRegex("((a)|(b))+")
        self.assertTrue(regex.accepts(["a", "b"]))

    def test_plus(self):
        regex = PythonRegex("a+")
        self.assertFalse(regex.accepts([]))
        self.assertTrue(regex.accepts(["a"]))
        self.assertTrue(regex.accepts(["a", "a"]))

    def test_dot(self):
        regex = PythonRegex("a.")
        self.assertTrue(regex.accepts(["a", "b"]))
        self.assertTrue(regex.accepts(["a", "?"]))
        self.assertFalse(regex.accepts(["a", "\n"]))
        self.assertFalse(regex.accepts(["a"]))
        self.assertTrue(regex.accepts(["a", "|"]))
        self.assertTrue(regex.accepts(["a", "("]))
        self.assertTrue(regex.accepts(["a", ")"]))
        self.assertTrue(regex.accepts(["a", "."]))
        self.assertTrue(regex.accepts(["a", "*"]))
        self.assertTrue(regex.accepts(["a", "+"]))
        self.assertTrue(regex.accepts(["a", "$"]))

    def test_dot_spaces(self):
        regex = PythonRegex("a.")
        self.assertTrue(regex.accepts(["a", " "]))
        self.assertTrue(regex.accepts(["a", "\t"]))
        self.assertTrue(regex.accepts(["a", "\v"]))
        self.assertTrue(regex.accepts(["a", "\r"]))

    def test_simple_optional(self):
        regex = PythonRegex("ab?")
        self.assertTrue(regex.accepts(["a"]))
        self.assertTrue(regex.accepts(["a", "b"]))
        self.assertFalse(regex.accepts(["a", "a"]))

    def test_with_parenthesis_optional(self):
        regex = PythonRegex("a(bb|c)?")
        self.assertTrue(regex.accepts(["a"]))
        self.assertTrue(regex.accepts(["a", "b", "b"]))
        self.assertTrue(regex.accepts(["a", "c"]))
        self.assertFalse(regex.accepts(["a", "b"]))

    def test_escape_question_mark(self):
        regex = PythonRegex(r"ab\?")
        self.assertTrue(regex.accepts(["a", "b", "?"]))

    def test_escape_kleene_star(self):
        regex = PythonRegex(r"ab\*")
        self.assertTrue(regex.accepts(["a", "b", "*"]))

    def test_escape_plus(self):
        regex = PythonRegex(r"ab\+")
        self.assertTrue(regex.accepts(["a", "b", "+"]))
        self.assertFalse(regex.accepts(["a", "b", "\\"]))

    def test_escape_opening_bracket(self):
        regex = PythonRegex(r"a\[")
        self.assertTrue(regex.accepts(["a", "["]))

    def test_escape_closing_bracket(self):
        regex = PythonRegex(r"a\]")
        self.assertTrue(regex.accepts(["a", "]"]))

    def test_escape_backslash(self):
        regex = PythonRegex(r"a\\")
        self.assertTrue(regex.accepts(["a", "\\"]))

    def test_escape_backslash_plus(self):
        regex = PythonRegex(r"a\\+")
        self.assertTrue(regex.accepts(["a", "\\", "\\"]))

    def test_escape_backslash_opening_bracket(self):
        regex = PythonRegex(r"a\\[ab]")
        self.assertTrue(regex.accepts(["a", "\\", "a"]))
        self.assertTrue(regex.accepts(["a", "\\", "b"]))

    def test_escape_backslash_closing_bracket(self):
        regex = PythonRegex(r"a[ab\\]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", "b"]))
        self.assertTrue(regex.accepts(["a", "\\"]))

    def test_escape_backslash_question_mark(self):
        regex = PythonRegex(r"a\\?")
        self.assertTrue(regex.accepts(["a"]))
        self.assertTrue(regex.accepts(["a", "\\"]))
        self.assertFalse(regex.accepts(["a", "\\", "?"]))
        self.assertFalse(regex.accepts(["a", "\\?"]))

    def test_escape_dash_in_brackets(self):
        regex = PythonRegex(r"a[a\-]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", "-"]))

    def test_special_in_brackets_opening_parenthesis(self):
        regex = PythonRegex(r"a[a(]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", "("]))

    def test_special_in_brackets_closing_parenthesis(self):
        regex = PythonRegex(r"a[a)]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", ")"]))

    def test_special_in_brackets_kleene_star(self):
        regex = PythonRegex(r"a[a*]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", "*"]))
        self.assertFalse(regex.accepts(["a", "a", "a"]))

    def test_special_in_brackets_positive_closure(self):
        regex = PythonRegex(r"a[a+]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", "+"]))
        self.assertFalse(regex.accepts(["a", "a", "a"]))

    def test_special_in_brackets_optional(self):
        regex = PythonRegex(r"a[a?]")
        self.assertTrue(regex.accepts(["a", "a"]))
        self.assertTrue(regex.accepts(["a", "?"]))
        self.assertFalse(regex.accepts(["a"]))

    def test_shortcut_digits(self):
        regex = PythonRegex(r"a\d")
        self.assertTrue(regex.accepts(["a", "0"]))
        self.assertTrue(regex.accepts(["a", "1"]))

    def test_shortcut_digits_in_brackets(self):
        regex = PythonRegex(r"a[\da]")
        self.assertTrue(regex.accepts(["a", "0"]))
        self.assertTrue(regex.accepts(["a", "1"]))
        self.assertTrue(regex.accepts(["a", "a"]))

    def test_shortcut_spaces(self):
        regex = PythonRegex(r"a\s")
        self.assertTrue(regex.accepts(["a", " "]))
        self.assertTrue(regex.accepts(["a", "\t"]))

    def test_space(self):
        regex = PythonRegex(" ")
        self.assertTrue(regex.accepts([" "]))

    def test_shortcut_word(self):
        regex = PythonRegex(r"a\w")
        self.assertTrue(regex.accepts(["a", "0"]))
        self.assertTrue(regex.accepts(["a", "_"]))
        self.assertTrue(regex.accepts(["a", "A"]))
        self.assertTrue(regex.accepts(["a", "f"]))
