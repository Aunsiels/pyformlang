""" Tests the CFG """

import unittest

from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol

class TestCFG(unittest.TestCase):
    """ Tests the production """

    def test_creation(self):
        """ Tests creatin of CFG """
        v0 = Variable(0)
        t0 = Terminal("a")
        p0 = Production(v0, [t0, Terminal("A"), Variable(1)])
        cfg = CFG({v0}, {t0}, v0, {p0})
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.get_number_variables(), 2)
        self.assertEqual(cfg.get_number_terminals(), 2)
        self.assertEqual(cfg.get_number_productions(), 1)
        self.assertTrue(cfg.is_empty())

        cfg = CFG()
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.get_number_variables(), 0)
        self.assertEqual(cfg.get_number_terminals(), 0)
        self.assertEqual(cfg.get_number_productions(), 0)
        self.assertTrue(cfg.is_empty())

    def test_generating_object(self):
        """ Test the finding of CFGObject """
        var_A = Variable("A")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(start, [ter_a])
        p2 = Production(var_A, [ter_b])
        cfg = CFG({var_A, var_B, start}, {ter_a, ter_b}, start, {p0, p1, p2})
        self.assertEqual(cfg.get_number_variables(), 3)
        self.assertEqual(cfg.get_number_terminals(), 2)
        self.assertEqual(cfg.get_number_productions(), 3)
        self.assertEqual(cfg.get_generating_symbols(), {var_A, ter_a, ter_b, start})

        p3 = Production(var_B, [Epsilon()])

        cfg = CFG({var_A, var_B, start}, {ter_a, ter_b}, start, {p0, p1, p2, p3})
        self.assertEqual(cfg.get_number_variables(), 3)
        self.assertEqual(cfg.get_number_terminals(), 2)
        self.assertEqual(cfg.get_number_productions(), 4)
        self.assertEqual(cfg.get_generating_symbols(), {var_A, var_B, ter_a,
                                                        ter_b, start})

    def test_reachable_object(self):
        """ Test the finding of reachable objects """
        var_A = Variable("A")
        var_B = Variable("B")
        var_C = Variable("C")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(start, [ter_a])
        p2 = Production(var_A, [ter_b])
        p3 = Production(var_C, [ter_c])
        p4 = Production(var_A, [Epsilon()])
        cfg = CFG({var_A, var_B, start, var_C},
                  {ter_a, ter_b, ter_c},
                  start, {p0, p1, p2, p3, p4})
        self.assertEqual(cfg.get_reachable_symbols(), {var_A, ter_a, var_B,
                                                       ter_b, start})

    def test_useless_removal(self):
        """ Test the removal of useless symbols """
        var_A = Variable("A")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(start, [ter_a])
        p2 = Production(var_A, [ter_b])
        cfg = CFG({var_A, var_B, start}, {ter_a, ter_b}, start, {p0, p1, p2})
        new_cfg = cfg.remove_useless_symbols()
        self.assertEqual(new_cfg.get_number_variables(), 1)
        self.assertEqual(new_cfg.get_number_terminals(), 1)
        self.assertEqual(new_cfg.get_number_productions(), 1)
        self.assertFalse(cfg.is_empty())

    def test_nullable_object(self):
        """ Tests the finding of nullable objects """
        var_A = Variable("A")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(var_A, [ter_a, var_A, var_A])
        p2 = Production(var_A, [Epsilon()])
        p3 = Production(var_B, [ter_b, var_B, var_B])
        p4 = Production(var_B, [Epsilon()])
        cfg = CFG({var_A, var_B, start},
                  {ter_a, ter_b},
                  start, {p0, p1, p2, p3, p4})
        self.assertEqual(cfg.get_nullable_symbols(),
                         {var_A, var_B, start})

    def test_remove_epsilon(self):
        """ Tests the removal of epsilon """
        var_A = Variable("A")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(var_A, [ter_a, var_A, var_A])
        p2 = Production(var_A, [Epsilon()])
        p3 = Production(var_B, [ter_b, var_B, var_B])
        p4 = Production(var_B, [])
        cfg = CFG({var_A, var_B, start},
                  {ter_a, ter_b},
                  start, {p0, p1, p2, p3, p4})
        new_cfg = cfg.remove_epsilon()
        self.assertEqual(new_cfg.get_number_variables(), 3)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(len(set(new_cfg._productions)), 9)
        self.assertEqual(len(new_cfg.get_nullable_symbols()), 0)
        self.assertFalse(cfg.is_empty())

    def test_unit_pair(self):
        """ Test the finding of unit pairs """
        var_I = Variable("I")
        var_F = Variable("F")
        var_E = Variable("E")
        var_T = Variable("T")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_0 = Terminal("0")
        ter_1 = Terminal("1")
        ter_par_open = Terminal("(")
        ter_par_close = Terminal(")")
        ter_mult = Terminal("*")
        ter_plus = Terminal("+")
        productions = {Production(var_I, [ter_a]),
                       Production(var_I, [ter_b]),
                       Production(var_I, [var_I, ter_a]),
                       Production(var_I, [var_I, ter_b]),
                       Production(var_I, [var_I, ter_0]),
                       Production(var_I, [var_I, ter_1]),
                       Production(var_F, [var_I]),
                       Production(var_F, [ter_par_open, var_E, ter_par_close]),
                       Production(var_T, [var_F]),
                       Production(var_T, [var_T, ter_mult, var_F]),
                       Production(var_E, [var_T]),
                       Production(var_E, [var_E, ter_plus, var_T])}
        cfg = CFG({var_I, var_F, var_E, var_T},
                  {ter_a, ter_b, ter_0, ter_1, ter_par_open,
                   ter_par_close, ter_mult, ter_plus},
                  var_E,
                  productions)
        self.assertEqual(cfg.get_unit_pairs(),
                         {(var_E, var_E),
                          (var_E, var_T),
                          (var_E, var_F),
                          (var_E, var_I),
                          (var_T, var_T),
                          (var_T, var_F),
                          (var_T, var_I),
                          (var_F, var_F),
                          (var_F, var_I),
                          (var_I, var_I)})
        new_cfg = cfg.eliminate_unit_productions()
        self.assertEqual(len(set(new_cfg._productions)), 30)

    def test_cnf(self):
        """ Tests the conversion to CNF form """
        var_I = Variable("I")
        var_F = Variable("F")
        var_E = Variable("E")
        var_T = Variable("C#CNF#1")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_0 = Terminal("0")
        ter_1 = Terminal("1")
        ter_par_open = Terminal("(")
        ter_par_close = Terminal(")")
        ter_mult = Terminal("*")
        ter_plus = Terminal("+")
        productions = {Production(var_I, [ter_a]),
                       Production(var_I, [ter_b]),
                       Production(var_I, [var_I, ter_a]),
                       Production(var_I, [var_I, ter_b]),
                       Production(var_I, [var_I, ter_0]),
                       Production(var_I, [var_I, ter_1]),
                       Production(var_F, [var_I]),
                       Production(var_F, [ter_par_open, var_E, ter_par_close]),
                       Production(var_T, [var_F]),
                       Production(var_T, [var_T, ter_mult, var_F]),
                       Production(var_E, [var_T]),
                       Production(var_E, [var_E, ter_plus, var_T])}
        cfg = CFG({var_I, var_F, var_E, var_T},
                  {ter_a, ter_b, ter_0, ter_1, ter_par_open,
                   ter_par_close, ter_mult, ter_plus},
                  var_E,
                  productions)
        new_cfg = cfg.to_normal_form()
        self.assertEqual(new_cfg.get_number_variables(), 15)
        self.assertEqual(new_cfg.get_number_terminals(), 8)
        self.assertEqual(new_cfg.get_number_productions(), 41)
        self.assertFalse(cfg.is_empty())
        new_cfg2 = cfg.to_normal_form()
        self.assertEqual(new_cfg, new_cfg2)

        cfg2 = CFG(start_symbol=var_E,
                   productions={Production(var_E, [var_T])})
        new_cfg = cfg2.to_normal_form()
        self.assertEqual(new_cfg.get_number_variables(), 1)
        self.assertEqual(new_cfg.get_number_terminals(), 0)
        self.assertEqual(new_cfg.get_number_productions(), 0)
        self.assertTrue(cfg2.is_empty())

    def test_substitution(self):
        """ Tests substitutions in a CFG """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.substitute({ter_a: cfg})
        self.assertEqual(new_cfg.get_number_variables(), 2)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 4)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_a, ter_b, ter_a, ter_b, ter_b, ter_b]))

    def test_union(self):
        """ Tests the union of two cfg """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.union(cfg)
        self.assertEqual(new_cfg.get_number_variables(), 3)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 6)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_b, ter_b]))

    def test_concatenation(self):
        """ Tests the concatenation of two cfg """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.concatenate(cfg)
        self.assertEqual(new_cfg.get_number_variables(), 3)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 5)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_b, ter_b, ter_a, ter_b]))

    def test_closure(self):
        """ Tests the closure of a cfg """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [ter_c])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.get_closure()
        self.assertEqual(new_cfg.get_number_variables(), 2)
        self.assertEqual(new_cfg.get_number_terminals(), 3)
        self.assertEqual(new_cfg.get_number_productions(), 5)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([]))
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_c, ter_b, ter_b,
                                          ter_a, ter_c, ter_b]))

    def test_pos_closure(self):
        """ Tests the closure of a cfg """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [ter_c])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.get_positive_closure()
        self.assertEqual(new_cfg.get_number_variables(), 3)
        self.assertEqual(new_cfg.get_number_terminals(), 3)
        self.assertEqual(new_cfg.get_number_productions(), 6)
        self.assertFalse(new_cfg.is_empty())
        self.assertFalse(new_cfg.contains([]))
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_c, ter_b, ter_b,
                                          ter_a, ter_c, ter_b]))

    def test_reverse(self):
        """ Test the reversal of a CFG """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.reverse()
        self.assertEqual(new_cfg.get_number_variables(), 1)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 2)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_b, ter_b, ter_a, ter_a]))

    def test_emptiness(self):
        """ Tests the emptiness of a CFG """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        self.assertFalse(cfg.is_empty())

    def test_membership(self):
        """ Tests the membership of a CFG """
        var_useless = Variable("USELESS")
        var_S = Variable("S")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        p0 = Production(var_S, [ter_a, var_S, var_B])
        p1 = Production(var_useless, [ter_a, var_S, var_B])
        p2 = Production(var_S, [var_useless])
        p4 = Production(var_B, [ter_b])
        p5 = Production(var_useless, [])
        cfg0 = CFG({var_useless, var_S}, {ter_a, ter_b}, var_S, {p0, p1, p2, p4, p5})
        self.assertTrue(cfg0.contains([Epsilon()]))
        self.assertTrue(cfg0.contains([ter_a, ter_b]))
        self.assertTrue(cfg0.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertTrue(cfg0.contains([ter_a, ter_a, ter_a, ter_b, ter_b, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_b, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_b, ter_c, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_a, ter_a, ter_b, ter_b]))

        p3 =  Production(var_S, [ter_c])
        cfg0 = CFG({var_S}, {ter_a, ter_b, ter_c}, var_S, {p0, p3})
        self.assertFalse(cfg0.contains([Epsilon()]))

        var_A = Variable("A")
        p6 = Production(var_S, [var_A, var_B])
        p7 = Production(var_A, [var_A, var_B])
        p8 = Production(var_A, [ter_a])
        p9 = Production(var_B, [ter_b])
        cfg1 = CFG({var_A, var_B, var_S},
                   {ter_a, ter_b},
                   var_S,
                   {p6, p7, p8, p9})
        self.assertTrue(cfg1.contains([ter_a, ter_b, ter_b]))
        cfg1 = CFG({"A", "B", "S"},
                   {"a", "b"},
                   "S",
                   {p6, p7, p8, p9})
        self.assertTrue(cfg1.contains(["a", "b", "b"]))

    def test_to_pda(self):
        """ Tests the conversion to PDA """
        var_E = Variable("E")
        var_I = Variable("I")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_0 = Terminal("0")
        ter_1 = Terminal("1")
        ter_par_open = Terminal("(")
        ter_par_close = Terminal(")")
        ter_mult = Terminal("*")
        ter_plus = Terminal("+")
        productions = {Production(var_E, [var_I]),
                       Production(var_E, [var_E, ter_plus, var_E]),
                       Production(var_E, [var_E, ter_mult, var_E]),
                       Production(var_E, [ter_par_open, var_E, ter_par_close]),
                       Production(var_I, [ter_a]),
                       Production(var_I, [ter_b]),
                       Production(var_I, [var_I, ter_a]),
                       Production(var_I, [var_I, ter_b]),
                       Production(var_I, [var_I, ter_0]),
                       Production(var_I, [var_I, ter_1]),
                       Production(var_I, [var_I, Epsilon()])}
        cfg = CFG({var_E, var_I},
                  {ter_a, ter_b, ter_0, ter_1, ter_par_open,
                   ter_par_close, ter_mult, ter_plus},
                  var_E,
                  productions)
        pda = cfg.to_pda()
        self.assertEqual(pda.get_number_states(), 1)
        self.assertEqual(pda.get_number_final_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 8)
        self.assertEqual(pda.get_number_stack_symbols(), 10)
        self.assertEqual(pda.get_number_transitions(), 19)

    def test_conversions(self):
        """ Tests multiple conversions """
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        var_S = Variable("S")
        productions = {Production(var_S, [ter_a, var_S, ter_b]),
                       Production(var_S, [ter_c])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        cfg = cfg.to_pda().to_final_state().to_empty_stack().to_cfg()
        self.assertTrue(cfg.contains([ter_c]))
        self.assertTrue(cfg.contains([ter_a, ter_c, ter_b]))
        self.assertTrue(cfg.contains([ter_a, ter_a, ter_c, ter_b, ter_b]))
        self.assertFalse(cfg.contains([ter_b, ter_c, ter_a]))
        self.assertFalse(cfg.contains([ter_b, ter_b, ter_c, ter_a, ter_a]))

    def _test_profiling_conversions(self):
        """ Tests multiple conversions """
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        var_S = Variable("S")
        productions = {Production(var_S, [ter_a, var_S, ter_b]),
                       Production(var_S, [ter_c])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        cfg = cfg.to_pda().to_final_state().to_empty_stack().to_cfg()
        cfg = cfg.to_pda().to_final_state().to_empty_stack().to_cfg()
        cfg = cfg.to_pda().to_final_state().to_empty_stack().to_cfg()
        self.assertTrue(True)

    def test_generation_words(self):
        """ Tests the generation of word """
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_S = Variable("S")
        productions = {Production(var_S, [ter_a, var_S, ter_b]),
                       Production(var_S, [])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        words0 = list(cfg.get_words(max_length=0))
        self.assertIn([], words0)
        self.assertEqual(len(words0), 1)
        words1 = list(cfg.get_words(max_length=1))
        self.assertIn([], words1)
        self.assertEqual(len(words1), 1)
        words2 = list(cfg.get_words(max_length=2))
        self.assertIn([], words2)
        self.assertIn([ter_a, ter_b], words2)
        self.assertEqual(len(words2), 2)
        words3 = list(cfg.get_words(max_length=3))
        self.assertIn([], words3)
        self.assertIn([ter_a, ter_b], words3)
        self.assertEqual(len(words3), 2)
        words4 = list(cfg.get_words(max_length=4))
        self.assertIn([], words4)
        self.assertIn([ter_a, ter_a, ter_b, ter_b], words4)
        self.assertEqual(len(words4), 3)

    def test_generation_words2(self):
        """ Tests the generation of word """
        ter_a = Terminal("a")
        var_S = Variable("S")
        var_S1 = Variable("S1")
        var_S2 = Variable("S2")
        productions = {Production(var_S, [var_S1, ter_a]),
                       Production(var_S1, [var_S2, ter_a]),
                       Production(var_S1, []),
                       Production(var_S2, []),
                       Production(var_S, [])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        words0 = list(cfg.get_words())
        self.assertIn([], words0)
        self.assertIn([ter_a], words0)
        self.assertIn([ter_a, ter_a], words0)
        self.assertEqual(len(words0), 3)

    def test_finite(self):
        """ Tests whether a grammar is finite or not """
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_S = Variable("S")
        var_A = Variable("A")
        var_B = Variable("B")
        prod0 = {Production(var_S, [var_A, var_B]),
                 Production(var_A, [ter_a]),
                 Production(var_B, [ter_b])}
        cfg = CFG(productions=prod0, start_symbol=var_S)
        self.assertTrue(cfg.is_finite())
        prod0.add(Production(var_A, [var_S]))
        cfg = CFG(productions=prod0, start_symbol=var_S)
        self.assertFalse(cfg.is_finite())


    def test_intersection(self):
        """ Tests the intersection with a regex """
        regex = Regex("a*b*")
        dfa = regex.to_epsilon_nfa().to_deterministic()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        self.assertTrue(dfa.accepts([symb_a, symb_a, symb_b, symb_b]))
        self.assertFalse(dfa.accepts([symb_b, symb_b, symb_a]))
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_S = Variable("S")
        productions = {Production(var_S, [ter_a, var_S, ter_b]),
                       Production(var_S, [ter_b, var_S, ter_a]),
                       Production(var_S, [])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        self.assertTrue(cfg.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg.contains([ter_a, ter_a, ter_b]))
        cfg_i = cfg.intersection(regex)
        self.assertTrue(cfg_i.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg_i.contains([ter_a, ter_a, ter_b]))
        self.assertTrue(cfg_i.contains([]))

    def test_intersection_dfa(self):
        state0 =  State(0)
        state1 = State(1)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        dfa = DeterministicFiniteAutomaton({state0, state1},
                                           {symb_a, symb_b},
                                           start_state = state0,
                                           final_states = {state0, state1})
        dfa.add_transition(state0, symb_a, state0)
        dfa.add_transition(state0, symb_b, state1)
        dfa.add_transition(state1, symb_b, state1)
        self.assertTrue(dfa.accepts([symb_a, symb_a, symb_b, symb_b]))
        self.assertFalse(dfa.accepts([symb_b, symb_b, symb_a]))

        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_S = Variable("S")
        productions = {Production(var_S, [ter_a, var_S, ter_b]),
                       Production(var_S, [ter_b, var_S, ter_a]),
                       Production(var_S, [])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        self.assertTrue(cfg.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg.contains([ter_a, ter_a, ter_b]))
        cfg_i = cfg.intersection(dfa)
        self.assertTrue(cfg_i.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg_i.contains([ter_a, ter_a, ter_b]))
        self.assertTrue(cfg_i.contains([]))

    def test_intersection_with_epsilon(self):
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("a")
        dfa = DeterministicFiniteAutomaton({state0, state1},
                                           {symb_a},
                                           start_state = state0,
                                           final_states = {state1})
        dfa.add_transition(state0, symb_a, state1)
        self.assertTrue(dfa.accepts([symb_a]))

        ter_a = Terminal("a")
        var_S = Variable("S")
        var_L = Variable("L")
        var_T = Variable("T")
        productions = {Production(var_S, [var_L, var_T]),
                       Production(var_L, [Epsilon()]),
                       Production(var_T, [ter_a])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        self.assertFalse(cfg.is_empty())
        self.assertTrue(cfg.contains([ter_a]))

        cfg_temp = cfg.to_pda().to_cfg()
        self.assertFalse(cfg_temp.is_empty())
        self.assertTrue(cfg_temp.contains([ter_a]))

        cfg_temp = cfg.to_pda().to_final_state().to_empty_stack().to_cfg()
        self.assertFalse(cfg_temp.is_empty())
        self.assertTrue(cfg_temp.contains([ter_a]))

        cfg_i = cfg.intersection(dfa)
        self.assertFalse(cfg_i.is_empty())

    def test_intersection_dfa2(self):
        state0 =  State(0)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        dfa = DeterministicFiniteAutomaton({state0},
                                           {symb_a, symb_b},
                                           start_state = state0,
                                           final_states = {state0})
        dfa.add_transition(state0, symb_a, state0)
        dfa.add_transition(state0, symb_b, state0)
        self.assertTrue(dfa.accepts([symb_a, symb_a, symb_b, symb_b]))

        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_S = Variable("S")
        var_S1 = Variable("S1")
        var_L = Variable("L")
        productions = {Production(var_S, [var_L, var_S1]),
                       Production(var_L, [Epsilon()]),
                       Production(var_S1, [ter_a, var_S1, ter_b]),
                       Production(var_S1, [ter_b, var_S1, ter_a]),
                       Production(var_S1, [])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        self.assertTrue(cfg.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg.contains([ter_a, ter_a, ter_b]))
        cfg_i = cfg.intersection(dfa)
        self.assertFalse(cfg_i.is_empty())
        self.assertTrue(cfg_i.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertTrue(cfg_i.contains([]))

    def _test_profiling_intersection(self):
        state0 =  State(0)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        dfa = DeterministicFiniteAutomaton({state0},
                                           {symb_a, symb_b},
                                           start_state = state0,
                                           final_states = {state0})
        dfa.add_transition(state0, symb_a, state0)
        dfa.add_transition(state0, symb_b, state0)

        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_S = Variable("S")
        var_S1 = Variable("S1")
        var_L = Variable("L")
        productions = {Production(var_S, [var_L, var_S1]),
                       Production(var_L, [Epsilon()]),
                       Production(var_S1, [ter_a, var_S1, ter_b]),
                       Production(var_S1, [ter_b, var_S1, ter_a]),
                       Production(var_S1, [])}
        cfg = CFG(productions=productions, start_symbol=var_S)
        cfg_i = cfg.intersection(dfa)
        cfg_i = cfg_i.intersection(dfa)
        cfg_i = cfg_i.intersection(dfa)
        self.assertFalse(cfg_i.is_empty())
        self.assertTrue(cfg_i.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertTrue(cfg_i.contains([]))
