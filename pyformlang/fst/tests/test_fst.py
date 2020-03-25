""" Tests the FST """

import unittest

from pyformlang.fst import FST
from pyformlang.indexed_grammar import (
    DuplicationRule, ProductionRule, EndRule,
    ConsumptionRule, IndexedGrammar, Rules)


class TestFST(unittest.TestCase):
    """ Tests FST """

    def test_creation(self):
        """ Test Translate """
        fst = FST()
        self.assertIsNotNone(fst)
        self.assertEqual(len(fst.states), 0)
        self.assertEqual(len(fst.input_symbols), 0)
        self.assertEqual(len(fst.output_symbols), 0)
        self.assertEqual(fst.get_number_transitions(), 0)
        self.assertEqual(len(fst.final_states), 0)

        fst.add_start_state("q0")
        self.assertEqual(len(fst.states), 1)

        fst.add_transition("q0", "a", "q1", ["bc"])
        self.assertEqual(len(fst.states), 2)
        self.assertEqual(len(fst.input_symbols), 1)
        self.assertEqual(len(fst.output_symbols), 1)
        self.assertEqual(fst.get_number_transitions(), 1)
        self.assertEqual(len(fst.final_states), 0)

        fst.add_transition("q0", "epsilon", "q1", ["bc"])
        self.assertEqual(len(fst.states), 2)
        self.assertEqual(len(fst.input_symbols), 1)
        self.assertEqual(len(fst.output_symbols), 1)
        self.assertEqual(fst.get_number_transitions(), 2)
        self.assertEqual(len(fst.final_states), 0)

        fst.add_final_state("q2")
        self.assertEqual(len(fst.states), 3)
        self.assertEqual(len(fst.input_symbols), 1)
        self.assertEqual(len(fst.output_symbols), 1)
        self.assertEqual(fst.get_number_transitions(), 2)
        self.assertEqual(len(fst.final_states), 1)

        fst.add_transition("q0", "a", "q1", ["d"])
        self.assertEqual(len(fst.states), 3)
        self.assertEqual(len(fst.input_symbols), 1)
        self.assertEqual(len(fst.output_symbols), 2)
        self.assertEqual(fst.get_number_transitions(), 3)
        self.assertEqual(len(fst.final_states), 1)

    def test_translate(self):
        """ Test a translation """
        fst = FST()
        fst.add_start_state("q0")
        translation = list(fst.translate(["a"]))
        self.assertEqual(len(translation), 0)

        fst.add_transition("q0", "a", "q1", ["b"])
        translation = list(fst.translate(["a"]))
        self.assertEqual(len(translation), 0)

        fst.add_final_state("q1")
        translation = list(fst.translate(["a"]))
        self.assertEqual(len(translation), 1)
        self.assertEqual(translation, [["b"]])

        fst.add_transition("q1", "epsilon", "q1", ["c"])
        translation = list(fst.translate(["a"], max_length=10))
        self.assertEqual(len(translation), 10)
        self.assertIn(["b"], translation)
        self.assertIn(["b", "c"], translation)
        self.assertIn(["b"] + ["c"] * 9, translation)

    def test_intersection_indexed_grammar(self):
        """ Test the intersection with indexed grammar """
        l_rules = []
        rules = Rules(l_rules)
        indexed_grammar = IndexedGrammar(rules)
        fst = FST()
        intersection = fst.intersection(indexed_grammar)
        self.assertTrue(intersection.is_empty())

        l_rules.append(ProductionRule("S", "D", "f"))
        l_rules.append(DuplicationRule("D", "A", "B"))
        l_rules.append(ConsumptionRule("f", "A", "Afinal"))
        l_rules.append(ConsumptionRule("f", "B", "Bfinal"))
        l_rules.append(EndRule("Afinal", "a"))
        l_rules.append(EndRule("Bfinal", "b"))

        rules = Rules(l_rules)
        indexed_grammar = IndexedGrammar(rules)
        intersection = fst.intersection(indexed_grammar)
        self.assertTrue(intersection.is_empty())

        fst.add_start_state("q0")
        fst.add_final_state("final")
        fst.add_transition("q0", "a", "q1", ["a"])
        fst.add_transition("q1", "b", "final", ["b"])
        intersection = fst.intersection(indexed_grammar)
        self.assertFalse(intersection.is_empty())

    def test_union(self):
        """ Tests the union"""
        fst0 = FST()
        fst0.add_start_state("q0")
        fst0.add_transition("q0", "a", "q1", ["b"])
        fst0.add_final_state("q1")
        fst1 = FST()
        fst1.add_start_state("q1")
        fst1.add_transition("q1", "b", "q2", ["c"])
        fst1.add_final_state("q2")
        fst_repeated = fst0.union(fst1)
        self.assertEqual(len(fst_repeated.start_states), 2)
        self.assertEqual(len(fst_repeated.final_states), 2)
        self.assertEqual(fst_repeated.get_number_transitions(), 2)
        translation = list(fst_repeated.translate(["a"]))
        self.assertEqual(translation, [["b"]])
        translation = list(fst_repeated.translate(["b"]))
        self.assertEqual(translation, [["c"]])
        translation = list(fst_repeated.translate(["a", "b"]))
        self.assertEqual(translation, [])

        fst_repeated = fst0 | fst1
        self.assertEqual(len(fst0.start_states), 1)
        self.assertEqual(len(fst1.start_states), 1)
        self.assertEqual(len(fst_repeated.start_states), 2)
        self.assertEqual(len(fst_repeated.final_states), 2)
        self.assertEqual(fst_repeated.get_number_transitions(), 2)
        translation = list(fst_repeated.translate(["a"]))
        self.assertEqual(translation, [["b"]])
        translation = list(fst_repeated.translate(["b"]))
        self.assertEqual(translation, [["c"]])
        translation = list(fst_repeated.translate(["a", "b"]))
        self.assertEqual(translation, [])
