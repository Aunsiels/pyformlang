"""
Tests for epsilon NFA
"""
import copy
import unittest

import networkx

from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon
from ..regexable import Regexable


class TestEpsilonNFA(unittest.TestCase):
    """ Tests epsilon NFA """

    # pylint: disable=missing-function-docstring, protected-access
    # pylint: disable=too-many-statements, too-many-public-methods

    def test_eclose(self):
        """ Test of the epsilon closure """
        states = [State(x) for x in range(8)]
        epsilon = Epsilon()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        enfa = EpsilonNFA()
        enfa.add_transition(states[1], epsilon, states[2])
        enfa.add_transition(states[1], epsilon, states[4])
        enfa.add_transition(states[2], epsilon, states[3])
        enfa.add_transition(states[3], epsilon, states[6])
        enfa.add_transition(states[5], epsilon, states[7])
        enfa.add_transition(states[4], symb_a, states[5])
        enfa.add_transition(states[5], symb_b, states[6])
        self.assertEqual(len(enfa.eclose(states[1])), 5)
        self.assertEqual(len(enfa.eclose(states[2])), 3)
        self.assertEqual(len(enfa.eclose(states[5])), 2)
        self.assertEqual(len(enfa.eclose(states[6])), 1)
        self.assertEqual(len(list(enfa._transition_function.get_edges())), 7)
        self.assertEqual(enfa.remove_transition(states[1], epsilon, states[4]),
                         1)
        self.assertFalse(enfa.is_deterministic())

    def test_accept(self):
        """ Test the acceptance """
        self._perform_tests_digits(False)

    def test_copy(self):
        """ Tests the copy of enda """
        self._perform_tests_digits(True)

    def _perform_tests_digits(self, should_copy=False):
        enfa, digits, epsilon, plus, minus, point = get_digits_enfa()
        if should_copy:
            enfa = copy.copy(enfa)
        self.assertTrue(enfa.accepts([plus, digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([minus, digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], point, digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], point]))
        self.assertTrue(enfa.accepts([digits[1], point, epsilon]))
        self.assertTrue(enfa.accepts([point, digits[9]]))
        self.assertFalse(enfa.accepts([point]))
        self.assertFalse(enfa.accepts([plus]))
        self.assertFalse(enfa.is_deterministic())

        self.assertTrue(enfa.accepts(["+", digits[1], ".", digits[9]]))
        self.assertTrue(enfa.accepts(["-", digits[1], ".", digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], ".", digits[9]]))
        self.assertTrue(enfa.accepts([digits[1], "."]))
        self.assertTrue(enfa.accepts([digits[1], ".", "epsilon"]))
        self.assertTrue(enfa.accepts([".", digits[9]]))
        self.assertFalse(enfa.accepts(["."]))
        self.assertFalse(enfa.accepts(["+"]))

    def test_deterministic(self):
        """ Tests the transformation to a dfa"""
        enfa, digits, _, plus, minus, point = get_digits_enfa()
        dfa = enfa.to_deterministic()
        self.assertTrue(dfa.is_deterministic())
        self.assertEqual(len(dfa.states), 6)
        self.assertEqual(dfa.get_number_transitions(), 65)
        self.assertEqual(len(dfa.final_states), 2)
        self.assertTrue(dfa.accepts([plus, digits[1], point, digits[9]]))
        self.assertTrue(dfa.accepts([minus, digits[1], point, digits[9]]))
        self.assertTrue(dfa.accepts([digits[1], point, digits[9]]))
        self.assertTrue(dfa.accepts([digits[1], point]))
        self.assertTrue(dfa.accepts([digits[1], point]))
        self.assertTrue(dfa.accepts([point, digits[9]]))
        self.assertFalse(dfa.accepts([point]))
        self.assertFalse(dfa.accepts([plus]))

    def test_remove_state(self):
        " Tests the remove of state """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        symb02 = Symbol("a+b")
        symb01 = Symbol("c*")
        symb11 = Symbol("b+(c.d)")
        symb12 = Symbol("a.b.c")
        enfa.add_start_state(state0)
        enfa.add_final_state(state2)
        enfa.add_transition(state0, symb01, state1)
        enfa.add_transition(state0, symb02, state2)
        enfa.add_transition(state1, symb11, state1)
        enfa.add_transition(state1, symb12, state2)
        enfa._remove_all_basic_states()
        self.assertEqual(enfa.get_number_transitions(), 1)
        self.assertEqual(len(enfa.states), 2)

    def test_to_regex(self):
        """ Tests the transformation to regex """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        symb_e = Symbol("e")
        symb_f = Symbol("f")
        symb_g = Symbol("g")
        enfa.add_start_state(state0)
        enfa.add_final_state(state2)
        enfa.add_transition(state0, symb_e, state1)
        enfa.add_transition(state1, symb_f, state2)
        enfa.add_transition(state0, symb_g, state2)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa2.accepts([symb_e, symb_f]))
        self.assertTrue(enfa2.accepts([symb_g]))
        self.assertFalse(enfa2.accepts([]))
        self.assertFalse(enfa2.accepts([symb_e]))
        self.assertFalse(enfa2.accepts([symb_f]))
        enfa.add_final_state(state0)
        with self.assertRaises(ValueError) as _:
            enfa._get_regex_simple()
        regex = enfa.to_regex()
        enfa3 = regex.to_epsilon_nfa()
        self.assertTrue(enfa3.accepts([symb_e, symb_f]))
        self.assertTrue(enfa3.accepts([symb_g]))
        self.assertTrue(enfa3.accepts([]))
        self.assertFalse(enfa3.accepts([symb_e]))
        self.assertFalse(enfa3.accepts([symb_f]))
        enfa.remove_start_state(state0)
        regex = enfa.to_regex()
        enfa3 = regex.to_epsilon_nfa()
        self.assertFalse(enfa3.accepts([symb_e, symb_f]))
        self.assertFalse(enfa3.accepts([symb_g]))
        self.assertFalse(enfa3.accepts([]))
        self.assertFalse(enfa3.accepts([symb_e]))
        self.assertFalse(enfa3.accepts([symb_f]))
        enfa.add_start_state(state0)
        enfa.add_transition(state0, symb_f, state0)
        regex = enfa.to_regex()
        enfa3 = regex.to_epsilon_nfa()
        self.assertTrue(enfa3.accepts([symb_e, symb_f]))
        self.assertTrue(enfa3.accepts([symb_f, symb_e, symb_f]))
        self.assertTrue(enfa3.accepts([symb_g]))
        self.assertTrue(enfa3.accepts([symb_f, symb_f, symb_g]))
        self.assertTrue(enfa3.accepts([]))
        self.assertFalse(enfa3.accepts([symb_e]))
        self.assertTrue(enfa3.accepts([symb_f]))

    def test_to_regex2(self):
        """ Tests the transformation to regex """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("0")
        symb_b = Symbol("1")
        enfa.add_start_state(state0)
        enfa.add_final_state(state1)
        enfa.add_transition(state0, symb_a, state0)
        enfa.add_transition(state0, symb_a, state1)
        enfa.add_transition(state1, symb_b, state0)
        enfa.add_transition(state1, symb_b, state1)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa2.accepts([symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b, symb_b]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a,
                                       symb_b, symb_b, symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b,
                                       symb_b, symb_a, symb_b]))
        self.assertFalse(enfa2.accepts([symb_b]))

    def test_to_regex3(self):
        """ Tests the transformation to regex """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("0")
        symb_b = Symbol("1")
        enfa.add_start_state(state0)
        enfa.add_final_state(state1)
        enfa.add_transition(state0, symb_a, state0)
        enfa.add_transition(state1, symb_b, state0)
        enfa.add_transition(state1, symb_b, state1)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertFalse(enfa2.accepts([symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a,
                                        symb_b, symb_b, symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b,
                                        symb_b, symb_a, symb_b]))
        self.assertFalse(enfa2.accepts([symb_b]))
        epsilon = Epsilon()
        enfa.add_transition(state0, epsilon, state1)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa.accepts([]))
        self.assertTrue(enfa.accepts([symb_a]))
        self.assertTrue(enfa2.accepts([symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b, symb_b]))
        self.assertTrue(enfa2.accepts([symb_a, symb_a, symb_b, symb_b,
                                       symb_a, symb_b]))
        self.assertTrue(enfa2.accepts([symb_b]))
        self.assertTrue(enfa2.accepts([]))
        enfa.remove_transition(state0, symb_a, state0)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertFalse(enfa2.accepts([symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b,
                                        symb_b, symb_a]))
        self.assertFalse(enfa2.accepts([symb_a, symb_a, symb_b, symb_b,
                                        symb_a, symb_b]))
        self.assertTrue(enfa2.accepts([symb_b]))
        self.assertTrue(enfa2.accepts([]))
        enfa.remove_transition(state1, symb_b, state1)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa2.accepts([symb_b, symb_b]))
        enfa.add_transition(state0, symb_a, state0)
        regex = enfa.to_regex()
        enfa2 = regex.to_epsilon_nfa()
        self.assertTrue(enfa2.accepts([symb_a, symb_b]))

    def test_union(self):
        """ Tests the union of two epsilon NFA """
        with self.assertRaises(NotImplementedError) as _:
            Regexable().to_regex()
        enfa0 = get_enfa_example0()
        enfa1 = get_enfa_example1()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        enfa = enfa0.union(enfa1)
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([]))

    def test_concatenate(self):
        """ Tests the concatenation of two epsilon NFA """
        enfa0 = get_enfa_example0()
        enfa1 = get_enfa_example1()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        enfa = enfa0.concatenate(enfa1)
        self.assertTrue(enfa.accepts([symb_b, symb_c]))
        self.assertTrue(enfa.accepts([symb_a, symb_b, symb_c]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b, symb_c]))
        self.assertFalse(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([]))

    def test_kleene(self):
        """ Tests the kleene star of an epsilon NFA """
        enfa0 = get_enfa_example0()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        enfa = enfa0.kleene_star()
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_b, symb_a, symb_b]))
        self.assertTrue(enfa.accepts([]))
        self.assertTrue(enfa.accepts([symb_b, symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([symb_a, symb_b, symb_a]))

    def test_complement(self):
        """ Tests the complement operation """
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        symb_a = Symbol("a")
        enfa.add_start_state(state0)
        enfa.add_final_state(state2)
        enfa.add_transition(state0, Epsilon(), state1)
        enfa.add_transition(state1, symb_a, state2)
        enfa_comp = -enfa
        self.assertFalse(enfa_comp.accepts([symb_a]))

    def test_intersection(self):
        """ Tests the intersection of two enfas """
        enfa0 = get_enfa_example0()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        eps = Epsilon()
        enfa1 = EpsilonNFA()
        state0 = State(10)
        state1 = State(11)
        state2 = State(12)
        state3 = State(13)
        state4 = State(14)
        enfa1.add_start_state(state0)
        enfa1.add_final_state(state3)
        enfa1.add_final_state(state4)
        enfa1.add_transition(state0, eps, state1)
        enfa1.add_transition(state1, symb_a, state2)
        enfa1.add_transition(state2, eps, state3)
        enfa1.add_transition(state3, symb_b, state4)
        enfa = enfa0 & enfa1
        self.assertEqual(len(enfa.start_states), 4)
        self.assertEqual(len(enfa.final_states), 2)
        self.assertEqual(len(enfa.symbols), 2)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([]))
        self.assertFalse(enfa.accepts([symb_a, symb_a, symb_b]))

    def test_difference(self):
        """ Tests the intersection of two languages """
        enfa0 = get_enfa_example0()
        enfa1 = get_enfa_example1()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        enfa = enfa0 - enfa1
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_c]))
        self.assertFalse(enfa.accepts([]))
        enfa2 = EpsilonNFA()
        state0 = State(0)
        enfa2.add_start_state(state0)
        enfa2.add_final_state(state0)
        enfa2.add_transition(state0, symb_b, state0)
        enfa = enfa0.get_difference(enfa2)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_c]))

    def test_reverse(self):
        """ Test the reversal of a language """
        enfa0 = get_enfa_example0()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        enfa = ~enfa0
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertTrue(enfa.accepts([symb_b, symb_a]))
        self.assertTrue(enfa.accepts([symb_b, symb_a, symb_a]))
        self.assertFalse(enfa.accepts([symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        self.assertFalse(enfa.accepts([]))

    def test_empty(self):
        """ Tests the emptiness of a finite automaton """
        self.assertTrue(get_enfa_example0())
        self.assertFalse(get_enfa_example1().is_empty())
        enfa = EpsilonNFA()
        state0 = State(0)
        enfa.add_start_state(state0)
        self.assertTrue(enfa.is_empty())
        state1 = State(1)
        symb_a = Symbol('a')
        enfa.add_transition(state0, symb_a, state1)
        self.assertTrue(enfa.is_empty())
        enfa.add_final_state(state1)
        self.assertFalse(enfa.is_empty())

    def test_minimization(self):
        """ Tests the minimization algorithm """
        enfa = get_enfa_example0_bis()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        enfa = enfa.minimize()
        self.assertTrue(enfa.is_deterministic())
        self.assertEqual(len(enfa.states), 2)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        enfa = get_example_non_minimal()
        enfa = enfa.minimize()
        self.assertTrue(enfa.is_deterministic())
        self.assertEqual(len(enfa.states), 3)
        self.assertTrue(enfa.accepts([symb_a, symb_b]))
        self.assertTrue(enfa.accepts([symb_a, symb_a, symb_b]))
        self.assertFalse(enfa.accepts([symb_b]))
        self.assertFalse(enfa.accepts([symb_a]))
        enfa = EpsilonNFA()
        enfa = enfa.minimize()
        self.assertTrue(enfa.is_deterministic())
        self.assertEqual(len(enfa.states), 1)
        self.assertFalse(enfa.accepts([]))

    def test_to_fst(self):
        """ Tests to turn a ENFA into a FST """
        enfa = EpsilonNFA()
        fst = enfa.to_fst()
        self.assertEqual(len(fst.states), 0)
        self.assertEqual(len(fst.final_states), 0)
        self.assertEqual(len(fst.start_states), 0)
        self.assertEqual(len(fst.input_symbols), 0)
        self.assertEqual(len(fst.output_symbols), 0)
        self.assertEqual(fst.get_number_transitions(), 0)

        state0 = State("q0")
        s0bis = State("q0bis")
        enfa.add_start_state(state0)
        enfa.add_start_state(s0bis)
        fst = enfa.to_fst()
        self.assertEqual(len(fst.states), 2)
        self.assertEqual(len(fst.final_states), 0)
        self.assertEqual(len(fst.start_states), 2)
        self.assertEqual(len(fst.input_symbols), 0)
        self.assertEqual(len(fst.output_symbols), 0)
        self.assertEqual(fst.get_number_transitions(), 0)

        sfinal = State("qfinal")
        sfinalbis = State("qfinalbis")
        enfa.add_final_state(sfinal)
        enfa.add_final_state(sfinalbis)
        fst = enfa.to_fst()
        self.assertEqual(len(fst.states), 4)
        self.assertEqual(len(fst.final_states), 2)
        self.assertEqual(len(fst.start_states), 2)
        self.assertEqual(len(fst.input_symbols), 0)
        self.assertEqual(len(fst.output_symbols), 0)
        self.assertEqual(fst.get_number_transitions(), 0)

        enfa.add_transition(state0, Symbol("a"), sfinal)
        enfa.add_transition(sfinal, Symbol("b"), sfinal)
        enfa.add_transition(state0, Symbol("c"), sfinalbis)
        fst = enfa.to_fst()
        self.assertEqual(len(fst.states), 4)
        self.assertEqual(len(fst.final_states), 2)
        self.assertEqual(len(fst.start_states), 2)
        self.assertEqual(len(fst.input_symbols), 3)
        self.assertEqual(len(fst.output_symbols), 3)
        self.assertEqual(fst.get_number_transitions(), 3)

        enfa.add_transition(state0, Epsilon(), sfinalbis)
        fst = enfa.to_fst()
        self.assertEqual(len(fst.states), 4)
        self.assertEqual(len(fst.final_states), 2)
        self.assertEqual(len(fst.start_states), 2)
        self.assertEqual(len(fst.input_symbols), 3)
        self.assertEqual(len(fst.output_symbols), 3)
        self.assertEqual(fst.get_number_transitions(), 4)

        trans0 = list(fst.translate(["a"]))
        self.assertEqual(trans0, [["a"]])

        trans0 = list(fst.translate(["a", "b", "b"]))
        self.assertEqual(trans0, [["a", "b", "b"]])

        trans0 = list(fst.translate(["b", "b"]))
        self.assertEqual(trans0, [])

        trans0 = list(fst.translate(["c"]))
        self.assertEqual(trans0, [["c"]])

    def test_cyclic(self):
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol('a')
        enfa.add_start_state(state0)
        enfa.add_transition(state0, symb_a, state1)
        enfa.add_transition(state1, Epsilon(), state0)
        self.assertFalse(enfa.is_acyclic())

    def test_export_networkx(self):
        enfa = EpsilonNFA()
        state0 = State("0")
        state1 = State(1)
        symb_a = Symbol('a')
        enfa.add_start_state(state0)
        enfa.add_final_state(state1)
        enfa.add_transition(state0, symb_a, state1)
        enfa.add_transition(state1, Epsilon(), state0)
        graph = enfa.to_networkx()
        self.assertTrue(isinstance(graph, networkx.MultiDiGraph))
        self.assertTrue("0" in graph)
        self.assertTrue(("0", 1) in graph.edges)
        self.assertIn("a", [x["label"] for x in graph["0"][1].values()])
        self.assertTrue(graph.nodes["0"]["is_start"])
        self.assertFalse(graph.nodes["0"]["is_final"])
        self.assertFalse(graph.nodes[1]["is_start"])
        self.assertTrue(graph.nodes[1]["is_final"])
        enfa.write_as_dot("enfa.dot")

    def test_import_networkx(self):
        enfa = EpsilonNFA()
        state0 = State("0")
        state1 = State(1)
        symb_a = Symbol('a')
        enfa.add_start_state(state0)
        enfa.add_final_state(state1)
        enfa.add_transition(state0, symb_a, state1)
        enfa.add_transition(state1, Epsilon(), state0)
        graph = enfa.to_networkx()
        enfa_from_nx = EpsilonNFA.from_networkx(graph)
        self.assertTrue(enfa_from_nx.accepts([symb_a]))
        self.assertTrue(enfa_from_nx.accepts([symb_a, symb_a]))
        self.assertFalse(enfa_from_nx.accepts([]))

    def test_iter(self):
        enfa = EpsilonNFA()
        state0 = State("0")
        state1 = State(1)
        symb_a = Symbol('a')
        enfa.add_start_state(state0)
        enfa.add_final_state(state1)
        enfa.add_transition(state0, symb_a, state1)
        enfa.add_transition(state1, Epsilon(), state0)
        counter = 0
        for s_from, symb, s_to in enfa:
            counter += 1
            self.assertIn((s_from, symb, s_to), enfa)
        self.assertNotIn((state1, symb_a, state1), enfa)
        self.assertIn(("0", "a", 1), enfa)
        self.assertEqual(counter, 2)

    def test_equivalent(self):
        enfa0 = EpsilonNFA()
        state0 = State("0")
        state1 = State(1)
        symb_a = Symbol('a')
        enfa0.add_start_state(state0)
        enfa0.add_final_state(state1)
        enfa0.add_transition(state0, symb_a, state1)
        enfa0.add_transition(state1, Epsilon(), state0)
        enfa1 = EpsilonNFA()
        enfa1.add_start_state(state0)
        enfa1.add_final_state(state1)
        enfa1.add_transition(state0, symb_a, state1)
        enfa1.add_transition(state1, symb_a, state1)
        self.assertTrue(enfa0.is_equivalent_to(enfa1))

    def test_non_equivalent(self):
        enfa0 = EpsilonNFA()
        state0 = State("0")
        state1 = State(1)
        symb_a = Symbol('a')
        enfa0.add_start_state(state0)
        enfa0.add_final_state(state1)
        enfa0.add_transition(state0, symb_a, state1)
        enfa0.add_transition(state1, Epsilon(), state0)
        enfa1 = EpsilonNFA()
        enfa1.add_start_state(state0)
        enfa1.add_final_state(state1)
        enfa1.add_transition(state0, symb_a, state1)
        enfa1.add_transition(state1, symb_a, state0)
        self.assertFalse(enfa0.is_equivalent_to(enfa1))

    def test_get_as_dict(self):
        enfa0 = EpsilonNFA()
        state0 = State("0")
        state1 = State(1)
        symb_a = Symbol('a')
        enfa0.add_start_state(state0)
        enfa0.add_final_state(state1)
        enfa0.add_transition(state0, symb_a, state1)
        enfa0.add_transition(state1, Epsilon(), state0)
        d_enfa = enfa0.to_dict()
        self.assertIn(state0, d_enfa)
        self.assertIn(symb_a, d_enfa[state0])
        self.assertIn(state1, d_enfa[state0][symb_a])

    def test_len(self):
        enfa = get_enfa_example1()
        self.assertEqual(len(enfa), 1)

    def test_call(self):
        enfa = get_enfa_example1()
        self.assertEqual(len(enfa(2)), 1)

    def test_example_doc(self):
        enfa = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("0")
        symb_b = Symbol("1")
        enfa.add_start_state(state0)
        enfa.add_final_state(state1)
        enfa.add_transition(state0, symb_a, state0)
        enfa.add_transition(state1, symb_b, state0)
        enfa.add_transition(state1, symb_b, state1)

        # Turn a finite automaton into a regex...
        regex = enfa.to_regex()
        # And turn it back into an epsilon non deterministic automaton
        enfa2 = regex.to_epsilon_nfa()
        self.assertEqual(enfa, enfa2)

    def test_remove_epsilon_transitions(self):
        enfa = EpsilonNFA()
        enfa.add_transitions([
            ("a", "epsilon", "b"),
            ("b", "t", "c"),
            ("a", "u", "c"),
            ("b", "epsilon", "d")
        ])
        self.assertEqual(enfa.get_number_transitions(), 4)
        enfa.add_start_state("a")
        enfa.add_final_state("b")
        self.assertEqual(len(enfa.start_states), 1)
        nfa = enfa.remove_epsilon_transitions()
        self.assertEqual(len(nfa.start_states), 3)
        self.assertEqual(len(nfa.final_states), 2)
        self.assertEqual(nfa.get_number_transitions(), 3)
        self.assertTrue(nfa.is_equivalent_to(enfa))


def get_digits_enfa():
    """ An epsilon NFA to recognize digits """
    epsilon = Epsilon()
    plus = Symbol("+")
    minus = Symbol("-")
    point = Symbol(".")
    digits = [Symbol(x) for x in range(10)]
    states = [State("q" + str(x)) for x in range(6)]
    enfa = EpsilonNFA()
    enfa.add_start_state(states[0])
    enfa.add_final_state(states[5])
    enfa.add_transition(states[0], epsilon, states[1])
    enfa.add_transition(states[0], plus, states[1])
    enfa.add_transition(states[0], minus, states[1])
    for digit in digits:
        enfa.add_transitions([
            (states[1], digit, states[1]),
            (states[1], digit, states[4]),
            (states[2], digit, states[3]),
            (states[3], digit, states[3])])
    enfa.add_transitions([
        (states[1], point, states[2]),
        (states[4], point, states[3]),
        (states[3], epsilon, states[5])])
    return enfa, digits, epsilon, plus, minus, point


def get_enfa_example0():
    """ Gives an example ENFA
    Accepts a*b
    """
    enfa0 = EpsilonNFA()
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    enfa0.add_start_state(state0)
    enfa0.add_final_state(state2)
    enfa0.add_transition(state0, symb_a, state0)
    enfa0.add_transition(state0, Epsilon(), state1)
    enfa0.add_transition(state1, symb_b, state2)
    return enfa0


def get_enfa_example1():
    """ Gives and example ENFA
    Accepts c
    """
    enfa1 = EpsilonNFA()
    state2 = State(2)
    state3 = State(3)
    symb_c = Symbol("c")
    enfa1.add_start_state(state2)
    enfa1.add_final_state(state3)
    enfa1.add_transition(state2, symb_c, state3)
    return enfa1


def get_enfa_example0_bis():
    """ A non minimal NFA, equivalent to example0 """
    enfa0 = EpsilonNFA()
    state3 = State(3)
    state4 = State(4)
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    enfa0.add_start_state(state0)
    enfa0.add_final_state(state2)
    enfa0.add_final_state(state4)
    enfa0.add_transition(state0, symb_a, state0)
    enfa0.add_transition(state0, Epsilon(), state1)
    enfa0.add_transition(state1, symb_b, state2)
    # New part
    enfa0.add_transition(state0, Epsilon(), state3)
    enfa0.add_transition(state3, symb_a, state3)
    enfa0.add_transition(state3, symb_b, state4)
    return enfa0


def get_example_non_minimal():
    """ A non minimal example a.a*.b"""
    enfa0 = EpsilonNFA()
    state0 = State(0)
    state3 = State(3)
    state4 = State(4)
    state5 = State(5)
    state6 = State(6)
    state1 = State(1)
    state2 = State(2)
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    enfa0.add_start_state(state0)
    enfa0.add_final_state(state3)
    enfa0.add_final_state(state4)
    enfa0.add_transition(state0, symb_a, state1)
    enfa0.add_transition(state1, symb_a, state2)
    enfa0.add_transition(state2, symb_a, state5)
    enfa0.add_transition(state5, symb_a, state6)
    enfa0.add_transition(state6, symb_a, state1)
    enfa0.add_transition(state1, symb_b, state3)
    enfa0.add_transition(state2, symb_b, state4)
    enfa0.add_transition(state5, symb_b, state3)
    enfa0.add_transition(state6, symb_b, state4)
    return enfa0
