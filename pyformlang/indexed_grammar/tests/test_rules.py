"""
Testing the rules
"""

import unittest

from pyformlang.indexed_grammar import Rules
from pyformlang.indexed_grammar import ConsumptionRule
from pyformlang.indexed_grammar import EndRule
from pyformlang.indexed_grammar import ProductionRule
from pyformlang.indexed_grammar import DuplicationRule

class TestIndexedGrammar(unittest.TestCase):
    """ Tests things related to rules """

    def test_consumption_rules(self):
        """ Tests the consumption rules """
        conso = ConsumptionRule("end", "C", "T")
        terminals = conso.get_terminals()
        self.assertEqual(terminals, {"end"})
        representation = str(conso)
        self.assertEqual(representation, "C [ end ] -> T")

    def test_duplication_rules(self):
        """ Tests the duplication rules """
        dupli = DuplicationRule("B0", "A0", "C")
        self.assertEqual(dupli.get_terminals(), {})
        self.assertEqual(str(dupli),
                         "B0 -> A0 C")

    def test_end_rule(self):
        """ Tests the end rules """
        end_rule = EndRule("A0", "b")
        self.assertEqual(end_rule.get_terminals(), {"b"})
        self.assertEqual(end_rule.get_right_term(), "b")
        self.assertEqual(str(end_rule), "A0 -> b")

    def test_production_rules(self):
        """ Tests the production rules """
        produ = ProductionRule("S", "C", "end")
        self.assertEqual(produ.get_terminals(), {"end"})
        self.assertEqual(str(produ), "S -> C[ end ]")

    def test_rules(self):
        """ Tests the rules """
        l_rules = []
        l_rules.append(ProductionRule("S", "Cinit", "end"))
        l_rules.append(ProductionRule("Cinit", "C", "b"))
        l_rules.append(ConsumptionRule("end", "C", "T"))
        l_rules.append(EndRule("T", "epsilon"))
        l_rules.append(ConsumptionRule("b", "C", "B0"))
        l_rules.append(DuplicationRule("B0", "A0", "C"))
        l_rules.append(EndRule("A0", "b"))
        rules = Rules(l_rules)
        self.assertEqual(rules.get_terminals(), {"b", "end", "epsilon"})
        self.assertEqual(rules.get_length(), (5, 2))
        rules.remove_production("S", "Cinit", "end")
        self.assertEqual(rules.get_length(), (4, 2))
        rules.add_production("S", "Cinit", "end")
        self.assertEqual(rules.get_length(), (5, 2))
