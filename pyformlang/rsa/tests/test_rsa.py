import unittest

from pyformlang.rsa.recursive_automaton import RecursiveAutomaton
from pyformlang.finite_automaton.symbol import Symbol
from pyformlang.regular_expression import Regex


class TestRSA(unittest.TestCase):
    def test_creation(self):
        rsa = RecursiveAutomaton()
        self.assertEqual(len(rsa._boxes), 0)
        self.assertEqual(len(rsa._labels), 0)
        self.assertEqual(len(rsa._label_to_box), 0)
        self.assertEqual(rsa._initial_label, "")

        try:
            rsa = RecursiveAutomaton(new_labels={Symbol("S")})
        except ValueError:
            self.assertEqual(True, True)

        rsa = RecursiveAutomaton(new_labels={Symbol("S")},
                                 new_initial_label=Symbol("S"),
                                 new_boxes=[Regex("18*").to_epsilon_nfa()],
                                 new_label_to_box={Symbol("S"): 0})
        self.assertEqual(len(rsa._labels), 1)
        self.assertEqual(rsa._labels, {Symbol("S")})
        self.assertEqual(len(rsa._boxes), 1)
        self.assertEqual(len(rsa._boxes[0].states), 1)
        self.assertEqual(len(rsa._label_to_box), 1)
        self.assertEqual(rsa._label_to_box, {Symbol("S"): 0})
        self.assertEqual(rsa._initial_label, Symbol("S"))

    def test_addbox(self):
        rsa = RecursiveAutomaton()
        rsa.add_box(Regex("9 3*").to_epsilon_nfa(), Symbol("S"))
        self.assertEqual()


if __name__ == '__main__':
    unittest.main()
