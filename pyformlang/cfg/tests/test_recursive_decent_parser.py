# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import unittest

from pyformlang.cfg import CFG, Variable, Terminal
from pyformlang.cfg.cfg import NotParsableException
from pyformlang.cfg.recursive_decent_parser import RecursiveDecentParser


class TestRecursiveDecentParser(unittest.TestCase):

    def setUp(self) -> None:
        cfg = CFG.from_text("""
                    E -> S + S
                    E -> S * S
                    S -> ( E )
                    S -> int
                """)
        self.parser = RecursiveDecentParser(cfg)

    def test_creation(self):
        self.assertIsNotNone(self.parser)

    def test_get_parsing_tree(self):
        self.assertTrue(self.parser.is_parsable(
            ["(", "int", "+", "(", "int", "*", "int", ")", ")"]
        ))
        parse_tree = self.parser.get_parse_tree(
            ["(", "int", "+", "(", "int", "*", "int", ")", ")"])
        derivation = parse_tree.get_leftmost_derivation()
        self.assertEqual(
            derivation,
            [[Variable("S")],
             [Terminal("("), Variable("E"), Terminal(")")],
             [Terminal("("), Variable("S"), Terminal("+"), Variable("S"),
              Terminal(")")],
             [Terminal("("), Terminal("int"), Terminal("+"), Variable("S"),
              Terminal(")")],
             [Terminal("("), Terminal("int"), Terminal("+"), Terminal("("),
              Variable("E"), Terminal(")"), Terminal(")")],
             [Terminal("("), Terminal("int"), Terminal("+"), Terminal("("),
              Variable("S"), Terminal("*"), Variable("S"), Terminal(")"),
              Terminal(")")],
             [Terminal("("), Terminal("int"), Terminal("+"), Terminal("("),
              Terminal("int"), Terminal("*"), Variable("S"), Terminal(")"),
              Terminal(")")],
             [Terminal("("), Terminal("int"), Terminal("+"), Terminal("("),
              Terminal("int"), Terminal("*"), Terminal("int"), Terminal(")"),
              Terminal(")")],
             ])

    def test_no_parse_tree(self):
        with self.assertRaises(NotParsableException):
            self.parser.get_parse_tree([")"])
        self.assertFalse((self.parser.is_parsable([")"])))

    def test_infinite_recursion(self):
        cfg = CFG.from_text("""
            S -> S E
        """)
        parser = RecursiveDecentParser(cfg)
        with self.assertRaises(RecursionError):
            parser.is_parsable([")"])
        self.assertFalse(parser.is_parsable([")"], left=False))
