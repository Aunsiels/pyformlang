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
        self._test_compare(".", "\n")

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
        self._test_compare(r"a\\[ab]", "a\\a")

    def test_escape_backslash_closing_bracket(self):
        self._test_compare(r"a[ab\\]", "aa")
        self._test_compare(r"a[ab\\]", "ab")
        self._test_compare(r"a[ab\\]", "a\\")

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

    def _test_compare(self, regex, s_test):
        r_pyformlang = PythonRegex(regex)
        r_python = re.compile(regex)
        self.assertEqual(r_python.fullmatch(s_test) is not None, r_pyformlang.accepts(s_test))

    def test_backslash(self):
        self._test_compare(".*", "]")
        self._test_compare(".*", "\\")

    def test_escape_dot(self):
        self._test_compare("\\.", ".")

    def test_brackets(self):
        self._test_compare(r"[{-}]", "}")
        self._test_compare(r"[{}]", "{")
        self._test_compare(r"[{-}]", "{")
        self._test_compare(r"[{-}]", "-")
        self._test_compare(r"[{-}]", "|")

    def test_brackets_escape(self):
        self._test_compare(r"[\[]", "[")
        self._test_compare(r"[Z-\[]", "Z")
        self._test_compare(r"[Z-\[]", "[")
        self._test_compare(r"[\[-a]", "[")
        self._test_compare(r"[\[-a]", "a")
        self._test_compare(r"[\[-\]]", "[")
        self._test_compare(r"[\[-\]]", "]")
        self._test_compare(r"[Z-\]]", "Z")
        self._test_compare(r"[Z-\]]", "]")
        self._test_compare(r"[\]-a]", "]")
        self._test_compare(r"[\]-a]", "a")

    def test_brackets_end_range_escaped(self):
        self._test_compare(r"[{-\}]", "|")
        self._test_compare(r"[{\}]", "{")
        self._test_compare(r"[{-\}]", "{")
        self._test_compare(r"[{-\}]", "-")
        self._test_compare(r"[{-\}]", "}")

    def test_brackets_backslash_middle(self):
        self._test_compare(r"[a\b]", "b")
        self._test_compare(r"[a\b]", "\b")
        self._test_compare(r"[a\\b]", "a")
        self._test_compare(r"[a\\b]", "b")
        self._test_compare(r"[a\\b]", "\\")
        self._test_compare(r"[a\b]", "a")
        self._test_compare(r"[a\b]", "\\b")
        self._test_compare(r"[a\b]", "\\")

    def test_backslash(self):
        self._test_compare(r"\t", "t")
        self._test_compare(r"\t", "\t")
        self._test_compare(r"\t", "\\t")
        self._test_compare(r"(a | \t)", "t")
        self._test_compare(r"(a | \t)", "\t")
        self._test_compare(r"(a | \t)", "\\t")

    def test_octal(self):
        self._test_compare(r"\x10", "\x10")
        self._test_compare(r"\110", "\110")
        self._test_compare(r"\\\\x10", "\x10")
        self._test_compare(r"\\\\x10", "\\x10")

    def test_backspace(self):
        self._test_compare(r"a[b\b]", "ab")
        self._test_compare(r"a[b\b]", "a\b")
        self._test_compare(r"\ba[b\b]", "ab")
        self._test_compare(r"\ba[b\b]", "a\b")
        self._test_compare(r"a[b|\b]", "ab")
        self._test_compare(r"a[b|\b]", "a|")

    def test_unicode_name(self):
        self._test_compare(r" ", " ")
        self._test_compare(r"\N{space}", " ")
        self._test_compare(r"\N{space}", "a")

    def test_unicode(self):
        self._test_compare(r"\u1111", "\u1111")
        self._test_compare(r"\U00001111", "\U00001111")

    def test_dot_harder(self):
        self._test_compare(r"\\.", "\\a")
        self._test_compare(r"\\.", "\\.")
        self._test_compare(r"\.", "a")
        self._test_compare(r"\.", ".")
        self._test_compare(r"\\\.", "\\a")
        self._test_compare(r"\\\.", "\\.")

    def test_single_repetition(self):
        self._test_compare(r"\d{3}-\d{3}-\d{4}", "012-876-3789")
        self._test_compare(r"a{5}b", "ab")
        self._test_compare(r"a{5}b", "aaaaab")
        self._test_compare(r"a{5b", "aaaaab")
        self._test_compare(r"a{5b", "a{5b")
        self._test_compare(r"T{4}P{3}", "TTTTTTPPPPPPPPPPPP")

    def test_range_repetition(self):
        self._test_compare(r"a{2,5}b", "ab")
        self._test_compare(r"a{2,5}b", "aab")
        self._test_compare(r"a{2,5}b", "aaaaab")
        self._test_compare(r"a{2,5}b", "aaaaaab")
        self._test_compare(r"a{2,5,7}b", "aaaaab")
        self._test_compare(r"a{2,5,7}b", "a{2,5,7}b")
        self._test_compare(r"ab{2,5}", "ab")
        self._test_compare(r"ab{2,5}", "abbb")
        self._test_compare(r"ab{2,5}", "abbbbb")
        self._test_compare(r"ab{2,5}", "abbbbbbbbb")
        self._test_compare(r"[a-z]{1,3}", "")
        self._test_compare(r"[a-z]{1,3}", "d")
        self._test_compare(r"[a-z]{1,3}", "do")
        self._test_compare(r"[a-z]{1,3}", "dpo")
        self._test_compare(r"[a-z]{1,3}", "dpoz")

    def test_error_backslash(self):
        self._test_compare(r"[a\\\\\\]]", "\\]")
        self._test_compare(r"\"([d\"\\\\]|\\\\.)*\"", '"d\\"')
        self._test_compare(r"[a\\\\]", "a")
        self._test_compare(r"\"([^\"\\\\]|\\\\.)*\"", '"ddd"')
        self._test_compare(r"([a-z_]+:\s([^,\n]+,)*[^,\n]*)", "abho-ja: njzk,szi,szkok")

    def test_negation_brackets(self):
        self._test_compare(r"[^abc]*", "")
        self._test_compare(r"[^abc]*", "a")
        self._test_compare(r"[^abc]*", "b")
        self._test_compare(r"[^abc]*", "c")
        self._test_compare(r"[^abc]*", "d")
        self._test_compare(r"[^abc]*", "dga")
        self._test_compare(r"[^abc]*", "dgh")
        self._test_compare(r"[^?]*", "dgh")

    def test_question_mark(self):
        self._test_compare(r".", "?")
        self._test_compare(r"a(a|b)?", "a")
        self._test_compare(r"a(a|b)\?", "ab?")
