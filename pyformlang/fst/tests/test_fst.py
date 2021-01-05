""" Tests the FST """
# pylint: disable=duplicate-code


import unittest
from os import path

from pyformlang.fst import FST
from pyformlang.indexed_grammar import (
    DuplicationRule, ProductionRule, EndRule,
    ConsumptionRule, IndexedGrammar, Rules)


class TestFST(unittest.TestCase):
    """ Tests FST """

    def setUp(self) -> None:
        self.fst0 = FST()
        self.fst0.add_start_state("q0")
        self.fst0.add_transition("q0", "a", "q1", ["b"])
        self.fst0.add_final_state("q1")
        self.fst1 = FST()
        self.fst1.add_start_state("q1")
        self.fst1.add_transition("q1", "b", "q2", ["c"])
        self.fst1.add_final_state("q2")

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
        intersection = fst & indexed_grammar
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
        fst_union = self.fst0.union(self.fst1)
        self._make_test_fst_union(fst_union)
        fst_union = self.fst0 | self.fst1
        self._make_test_fst_union(fst_union)

    def _make_test_fst_union(self, fst_union):
        self.assertEqual(len(fst_union.start_states), 2)
        self.assertEqual(len(fst_union.final_states), 2)
        self.assertEqual(fst_union.get_number_transitions(), 2)
        translation = list(fst_union.translate(["a"]))
        self.assertEqual(translation, [["b"]])
        translation = list(fst_union.translate(["b"]))
        self.assertEqual(translation, [["c"]])
        translation = list(fst_union.translate(["a", "b"]))
        self.assertEqual(translation, [])

    def test_concatenate(self):
        """ Tests the concatenation """
        fst_concatenate = self.fst0 + self.fst1
        translation = list(fst_concatenate.translate(["a", "b"]))
        self.assertEqual(translation, [["b", "c"]])
        translation = list(fst_concatenate.translate(["a"]))
        self.assertEqual(translation, [])
        translation = list(fst_concatenate.translate(["b"]))
        self.assertEqual(translation, [])

    def test_concatenate2(self):
        """ Tests the concatenation """
        fst_concatenate = self.fst0 + self.fst1 + self.fst1
        translation = list(fst_concatenate.translate(["a", "b", "b"]))
        self.assertEqual(translation, [["b", "c", "c"]])
        translation = list(fst_concatenate.translate(["a"]))
        self.assertEqual(translation, [])
        translation = list(fst_concatenate.translate(["b"]))
        self.assertEqual(translation, [])

    def test_kleene_start(self):
        """ Tests the kleene star on a fst"""
        fst_star = self.fst0.kleene_star()
        translation = list(fst_star.translate(["a"]))
        self.assertEqual(translation, [["b"]])
        translation = list(fst_star.translate(["a", "a"]))
        self.assertEqual(translation, [["b", "b"]])
        translation = list(fst_star.translate([]))
        self.assertEqual(translation, [[]])

    def test_generate_empty_word_from_nothing(self):
        """ Generate empty word from nothing """
        fst = FST()
        fst.add_start_state("q0")
        fst.add_transition("q0", "epsilon", "q1", [])
        fst.add_final_state("q1")
        translation = list(fst.translate([]))
        self.assertEqual(translation, [[]])

    def test_epsilon_loop(self):
        """ Test empty loop """
        fst = FST()
        fst.add_start_state("q0")
        fst.add_transition("q0", "epsilon", "q1", [])
        fst.add_final_state("q1")
        fst.add_transition("q1", "epsilon", "q0", [])
        translation = list(fst.translate([]))
        self.assertEqual(translation, [[]])

    def test_epsilon_loop2(self):
        """ Test empty loop bis """
        fst = FST()
        fst.add_start_state("q0")
        fst.add_transitions(
            [("q0", "epsilon", "q1", []),
             ("q1", "a", "q2", ["b"]),
             ("q1", "epsilon", "q0", [])])
        fst.add_final_state("q2")
        translation = list(fst.translate(["a"]))
        self.assertEqual(translation, [["b"]])

    def test_paper(self):
        """ Test for the paper """
        fst = FST()
        fst.add_transitions(
            [(0, "I", 1, ["Je"]), (1, "am", 2, ["suis"]),
             (2, "alone", 3, ["tout", "seul"]),
             (2, "alone", 3, ["seul"])])
        fst.add_start_state(0)
        fst.add_final_state(3)
        self.assertEqual(
            list(fst.translate(["I", "am", "alone"])),
            [['Je', 'suis', 'seul'],
             ['Je', 'suis', 'tout', 'seul']])
        fst = FST.from_networkx(fst.to_networkx())
        self.assertEqual(
            list(fst.translate(["I", "am", "alone"])),
            [['Je', 'suis', 'seul'],
             ['Je', 'suis', 'tout', 'seul']])
        fst.write_as_dot("fst.dot")
        self.assertTrue(path.exists("fst.dot"))
