import unittest

from pyformlang.regular_expression.python_regex import PythonRegex


class TestPythonRegex(unittest.TestCase):
    """ Tests for python regex """

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