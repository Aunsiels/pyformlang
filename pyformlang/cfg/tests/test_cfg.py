""" Tests the CFG """

import unittest

from pyformlang import pda
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from pyformlang.cfg.cyk_table import DerivationDoesNotExist
from pyformlang.cfg.pda_object_creator import PDAObjectCreator
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.regular_expression import Regex


class TestCFG(unittest.TestCase):
    """ Tests the context free grammar """

    # pylint: disable=missing-function-docstring, too-many-public-methods

    def test_creation(self):
        """ Tests creatin of CFG """
        variable0 = Variable(0)
        terminal0 = Terminal("a")
        prod0 = Production(variable0, [terminal0, Terminal("A"), Variable(1)])
        cfg = CFG({variable0}, {terminal0}, variable0, {prod0})
        self.assertIsNotNone(cfg)
        self.assertEqual(len(cfg.variables), 2)
        self.assertEqual(len(cfg.terminals), 2)
        self.assertEqual(len(cfg.productions), 1)
        self.assertTrue(cfg.is_empty())

        cfg = CFG()
        self.assertIsNotNone(cfg)
        self.assertEqual(len(cfg.variables), 0)
        self.assertEqual(len(cfg.terminals), 0)
        self.assertEqual(len(cfg.productions), 0)
        self.assertTrue(cfg.is_empty())

    def test_generating_object(self):
        """ Test the finding of CFGObject """
        var_a = Variable("A")
        var_b = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        prod0 = Production(start, [var_a, var_b])
        prod1 = Production(start, [ter_a])
        prod2 = Production(var_a, [ter_b])
        cfg = CFG({var_a, var_b, start}, {ter_a, ter_b}, start,
                  {prod0, prod1, prod2})
        self.assertEqual(len(cfg.variables), 3)
        self.assertEqual(len(cfg.terminals), 2)
        self.assertEqual(len(cfg.productions), 3)
        self.assertEqual(cfg.get_generating_symbols(),
                         {var_a, ter_a, ter_b, start})

        prod3 = Production(var_b, [Epsilon()])

        cfg = CFG({var_a, var_b, start}, {ter_a, ter_b}, start,
                  {prod0, prod1, prod2, prod3})
        self.assertEqual(len(cfg.variables), 3)
        self.assertEqual(len(cfg.terminals), 2)
        self.assertEqual(len(cfg.productions), 4)
        self.assertEqual(cfg.get_generating_symbols(), {var_a, var_b, ter_a,
                                                        ter_b, start})

    def test_reachable_object(self):
        """ Test the finding of reachable objects """
        var_a = Variable("A")
        var_b = Variable("B")
        var_c = Variable("C")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        start = Variable("S")
        prod0 = Production(start, [var_a, var_b])
        prod1 = Production(start, [ter_a])
        prod2 = Production(var_a, [ter_b])
        prod3 = Production(var_c, [ter_c])
        prod4 = Production(var_a, [Epsilon()])
        cfg = CFG({var_a, var_b, start, var_c},
                  {ter_a, ter_b, ter_c},
                  start, {prod0, prod1, prod2, prod3, prod4})
        self.assertEqual(cfg.get_reachable_symbols(), {var_a, ter_a, var_b,
                                                       ter_b, start})

    def test_useless_removal(self):
        """ Test the removal of useless symbols """
        var_a = Variable("A")
        var_b = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        prod0 = Production(start, [var_a, var_b])
        prod1 = Production(start, [ter_a])
        prod2 = Production(var_a, [ter_b])
        cfg = CFG({var_a, var_b, start}, {ter_a, ter_b}, start,
                  {prod0, prod1, prod2})
        new_cfg = cfg.remove_useless_symbols()
        self.assertEqual(len(new_cfg.variables), 1)
        self.assertEqual(len(new_cfg.terminals), 1)
        self.assertEqual(len(new_cfg.productions), 1)
        self.assertFalse(cfg.is_empty())

    def test_nullable_object(self):
        """ Tests the finding of nullable objects """
        var_a = Variable("A")
        var_b = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        prod0 = Production(start, [var_a, var_b])
        prod1 = Production(var_a, [ter_a, var_a, var_a])
        prod2 = Production(var_a, [Epsilon()])
        prod3 = Production(var_b, [ter_b, var_b, var_b])
        prod4 = Production(var_b, [Epsilon()])
        cfg = CFG({var_a, var_b, start},
                  {ter_a, ter_b},
                  start, {prod0, prod1, prod2, prod3, prod4})
        self.assertEqual(cfg.get_nullable_symbols(),
                         {var_a, var_b, start})

    def test_remove_epsilon(self):
        """ Tests the removal of epsilon """
        var_a = Variable("A")
        var_b = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        prod0 = Production(start, [var_a, var_b])
        prod1 = Production(var_a, [ter_a, var_a, var_a])
        prod2 = Production(var_a, [Epsilon()])
        prod3 = Production(var_b, [ter_b, var_b, var_b])
        prod4 = Production(var_b, [])
        cfg = CFG({var_a, var_b, start},
                  {ter_a, ter_b},
                  start, {prod0, prod1, prod2, prod3, prod4})
        new_cfg = cfg.remove_epsilon()
        self.assertEqual(len(new_cfg.variables), 3)
        self.assertEqual(len(new_cfg.terminals), 2)
        self.assertEqual(len(set(new_cfg.productions)), 9)
        self.assertEqual(len(new_cfg.get_nullable_symbols()), 0)
        self.assertFalse(cfg.is_empty())

    def test_unit_pair(self):
        """ Test the finding of unit pairs """
        # pylint: disable=too-many-locals
        var_i = Variable("I")
        var_f = Variable("F")
        var_e = Variable("E")
        var_t = Variable("T")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_0 = Terminal("0")
        ter_1 = Terminal("1")
        ter_par_open = Terminal("(")
        ter_par_close = Terminal(")")
        ter_mult = Terminal("*")
        ter_plus = Terminal("+")
        productions = {Production(var_i, [ter_a]),
                       Production(var_i, [ter_b]),
                       Production(var_i, [var_i, ter_a]),
                       Production(var_i, [var_i, ter_b]),
                       Production(var_i, [var_i, ter_0]),
                       Production(var_i, [var_i, ter_1]),
                       Production(var_f, [var_i]),
                       Production(var_f, [ter_par_open, var_e, ter_par_close]),
                       Production(var_t, [var_f]),
                       Production(var_t, [var_t, ter_mult, var_f]),
                       Production(var_e, [var_t]),
                       Production(var_e, [var_e, ter_plus, var_t])}
        cfg = CFG({var_i, var_f, var_e, var_t},
                  {ter_a, ter_b, ter_0, ter_1, ter_par_open,
                   ter_par_close, ter_mult, ter_plus},
                  var_e,
                  productions)
        self.assertEqual(cfg.get_unit_pairs(),
                         {(var_e, var_e),
                          (var_e, var_t),
                          (var_e, var_f),
                          (var_e, var_i),
                          (var_t, var_t),
                          (var_t, var_f),
                          (var_t, var_i),
                          (var_f, var_f),
                          (var_f, var_i),
                          (var_i, var_i)})
        new_cfg = cfg.eliminate_unit_productions()
        self.assertEqual(len(set(new_cfg.productions)), 30)

    def test_cnf(self):
        """ Tests the conversion to CNF form """
        # pylint: disable=too-many-locals
        var_i = Variable("I")
        var_f = Variable("F")
        var_e = Variable("E")
        var_t = Variable("C#CNF#1")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_0 = Terminal("0")
        ter_1 = Terminal("1")
        ter_par_open = Terminal("(")
        ter_par_close = Terminal(")")
        ter_mult = Terminal("*")
        ter_plus = Terminal("+")
        productions = {Production(var_i, [ter_a]),
                       Production(var_i, [ter_b]),
                       Production(var_i, [var_i, ter_a]),
                       Production(var_i, [var_i, ter_b]),
                       Production(var_i, [var_i, ter_0]),
                       Production(var_i, [var_i, ter_1]),
                       Production(var_f, [var_i]),
                       Production(var_f, [ter_par_open, var_e, ter_par_close]),
                       Production(var_t, [var_f]),
                       Production(var_t, [var_t, ter_mult, var_f]),
                       Production(var_e, [var_t]),
                       Production(var_e, [var_e, ter_plus, var_t])}
        cfg = CFG({var_i, var_f, var_e, var_t},
                  {ter_a, ter_b, ter_0, ter_1, ter_par_open,
                   ter_par_close, ter_mult, ter_plus},
                  var_e,
                  productions)
        new_cfg = cfg.to_normal_form()
        self.assertEqual(len(new_cfg.variables), 15)
        self.assertEqual(len(new_cfg.terminals), 8)
        self.assertEqual(len(new_cfg.productions), 41)
        self.assertFalse(cfg.is_empty())
        new_cfg2 = cfg.to_normal_form()
        self.assertEqual(new_cfg, new_cfg2)

        cfg2 = CFG(start_symbol=var_e,
                   productions={Production(var_e, [var_t])})
        new_cfg = cfg2.to_normal_form()
        self.assertEqual(len(new_cfg.variables), 1)
        self.assertEqual(len(new_cfg.terminals), 0)
        self.assertEqual(len(new_cfg.productions), 0)
        self.assertTrue(cfg2.is_empty())

    def test_substitution(self):
        """ Tests substitutions in a CFG """
        var_s = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        prod0 = Production(var_s, [ter_a, var_s, ter_b])
        prod1 = Production(var_s, [])
        cfg = CFG({var_s}, {ter_a, ter_b}, var_s, {prod0, prod1})
        new_cfg = cfg.substitute({ter_a: cfg})
        self.assertEqual(len(new_cfg.variables), 2)
        self.assertEqual(len(new_cfg.terminals), 2)
        self.assertEqual(len(new_cfg.productions), 4)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(
            new_cfg.contains([ter_a, ter_b, ter_a, ter_b, ter_b, ter_b]))

    def test_union(self):
        """ Tests the union of two cfg """
        var_s = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        prod0 = Production(var_s, [ter_a, var_s, ter_b])
        prod1 = Production(var_s, [])
        cfg = CFG({var_s}, {ter_a, ter_b}, var_s, {prod0, prod1})
        new_cfg = cfg | cfg
        self.assertEqual(len(new_cfg.variables), 3)
        self.assertEqual(len(new_cfg.terminals), 2)
        self.assertEqual(len(new_cfg.productions), 6)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_b, ter_b]))

    def test_concatenation(self):
        """ Tests the concatenation of two cfg """
        var_s = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        prod0 = Production(var_s, [ter_a, var_s, ter_b])
        prod1 = Production(var_s, [])
        cfg = CFG({var_s}, {ter_a, ter_b}, var_s, {prod0, prod1})
        new_cfg = cfg + cfg
        self.assertEqual(len(new_cfg.variables), 3)
        self.assertEqual(len(new_cfg.terminals), 2)
        self.assertEqual(len(new_cfg.productions), 5)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(
            new_cfg.contains([ter_a, ter_a, ter_b, ter_b, ter_a, ter_b]))

    def test_closure(self):
        """ Tests the closure of a cfg """
        var_s = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        prod0 = Production(var_s, [ter_a, var_s, ter_b])
        prod1 = Production(var_s, [ter_c])
        cfg = CFG({var_s}, {ter_a, ter_b}, var_s, {prod0, prod1})
        new_cfg = cfg.get_closure()
        self.assertEqual(len(new_cfg.variables), 2)
        self.assertEqual(len(new_cfg.terminals), 3)
        self.assertEqual(len(new_cfg.productions), 5)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([]))
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_c, ter_b, ter_b,
                                          ter_a, ter_c, ter_b]))

    def test_pos_closure(self):
        """ Tests the closure of a cfg """
        var_s = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        prod0 = Production(var_s, [ter_a, var_s, ter_b])
        prod1 = Production(var_s, [ter_c])
        cfg = CFG({var_s}, {ter_a, ter_b}, var_s, {prod0, prod1})
        new_cfg = cfg.get_positive_closure()
        self.assertEqual(len(new_cfg.variables), 3)
        self.assertEqual(len(new_cfg.terminals), 3)
        self.assertEqual(len(new_cfg.productions), 6)
        self.assertFalse(new_cfg.is_empty())
        self.assertFalse(new_cfg.contains([]))
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_c, ter_b, ter_b,
                                          ter_a, ter_c, ter_b]))

    def test_reverse(self):
        """ Test the reversal of a CFG """
        var_s = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        prod0 = Production(var_s, [ter_a, var_s, ter_b])
        prod1 = Production(var_s, [])
        cfg = CFG({var_s}, {ter_a, ter_b}, var_s, {prod0, prod1})
        new_cfg = ~cfg
        self.assertEqual(len(new_cfg.variables), 1)
        self.assertEqual(len(new_cfg.terminals), 2)
        self.assertEqual(len(new_cfg.productions), 2)
        self.assertFalse(not new_cfg)
        self.assertTrue(new_cfg.contains([ter_b, ter_b, ter_a, ter_a]))

    def test_emptiness(self):
        """ Tests the emptiness of a CFG """
        # pylint: disable=too-many-locals
        var_s = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        prod0 = Production(var_s, [ter_a, var_s, ter_b])
        prod1 = Production(var_s, [])
        cfg = CFG({var_s}, {ter_a, ter_b}, var_s, {prod0, prod1})
        self.assertFalse(cfg.is_empty())

    def test_membership(self):
        """ Tests the membership of a CFG """
        # pylint: disable=too-many-locals
        var_useless = Variable("USELESS")
        var_s = Variable("S")
        var_b = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        prod0 = Production(var_s, [ter_a, var_s, var_b])
        prod1 = Production(var_useless, [ter_a, var_s, var_b])
        prod2 = Production(var_s, [var_useless])
        prod4 = Production(var_b, [ter_b])
        prod5 = Production(var_useless, [])
        cfg0 = CFG({var_useless, var_s}, {ter_a, ter_b}, var_s,
                   {prod0, prod1, prod2, prod4, prod5})
        self.assertTrue(cfg0.contains([Epsilon()]))
        self.assertTrue(cfg0.contains([ter_a, ter_b]))
        self.assertTrue(cfg0.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertTrue(cfg0.contains(
            [ter_a, ter_a, ter_a, ter_b, ter_b, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_b, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_b, ter_c, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_a, ter_a, ter_b, ter_b]))

        prod3 = Production(var_s, [ter_c])
        cfg0 = CFG({var_s}, {ter_a, ter_b, ter_c}, var_s, {prod0, prod3})
        self.assertFalse(cfg0.contains([Epsilon()]))

        var_a = Variable("A")
        prod6 = Production(var_s, [var_a, var_b])
        prod7 = Production(var_a, [var_a, var_b])
        prod8 = Production(var_a, [ter_a])
        prod9 = Production(var_b, [ter_b])
        cfg1 = CFG({var_a, var_b, var_s},
                   {ter_a, ter_b},
                   var_s,
                   {prod6, prod7, prod8, prod9})
        self.assertTrue(cfg1.contains([ter_a, ter_b, ter_b]))
        cfg1 = CFG({"A", "B", "S"},
                   {"a", "b"},
                   "S",
                   {prod6, prod7, prod8, prod9})
        self.assertTrue(cfg1.contains(["a", "b", "b"]))

    def test_to_pda(self):
        """ Tests the conversion to PDA """
        var_e = Variable("E")
        var_i = Variable("I")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_0 = Terminal("0")
        ter_1 = Terminal("1")
        ter_par_open = Terminal("(")
        ter_par_close = Terminal(")")
        ter_mult = Terminal("*")
        ter_plus = Terminal("+")
        productions = {Production(var_e, [var_i]),
                       Production(var_e, [var_e, ter_plus, var_e]),
                       Production(var_e, [var_e, ter_mult, var_e]),
                       Production(var_e, [ter_par_open, var_e, ter_par_close]),
                       Production(var_i, [ter_a]),
                       Production(var_i, [ter_b]),
                       Production(var_i, [var_i, ter_a]),
                       Production(var_i, [var_i, ter_b]),
                       Production(var_i, [var_i, ter_0]),
                       Production(var_i, [var_i, ter_1]),
                       Production(var_i, [var_i, Epsilon()])}
        cfg = CFG({var_e, var_i},
                  {ter_a, ter_b, ter_0, ter_1, ter_par_open,
                   ter_par_close, ter_mult, ter_plus},
                  var_e,
                  productions)
        pda_equivalent = cfg.to_pda()
        self.assertEqual(len(pda_equivalent.states), 1)
        self.assertEqual(len(pda_equivalent.final_states), 0)
        self.assertEqual(len(pda_equivalent.input_symbols), 8)
        self.assertEqual(len(pda_equivalent.stack_symbols), 10)
        self.assertEqual(pda_equivalent.get_number_transitions(), 19)

    def test_conversions(self):
        """ Tests multiple conversions """
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        var_s = Variable("S")
        productions = {Production(var_s, [ter_a, var_s, ter_b]),
                       Production(var_s, [ter_c])}
        cfg = CFG(productions=productions, start_symbol=var_s)
        cfg = cfg.to_pda().to_final_state().to_empty_stack().to_cfg()
        self.assertTrue(cfg.contains([ter_c]))
        self.assertTrue(cfg.contains([ter_a, ter_c, ter_b]))
        self.assertTrue(cfg.contains([ter_a, ter_a, ter_c, ter_b, ter_b]))
        self.assertFalse(cfg.contains([ter_b, ter_c, ter_a]))
        self.assertFalse(cfg.contains([ter_b, ter_b, ter_c, ter_a, ter_a]))

    @staticmethod
    def test_profiling_conversions():
        """ Tests multiple conversions """
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        var_s = Variable("S")
        productions = {Production(var_s, [ter_a, var_s, ter_b]),
                       Production(var_s, [ter_c])}
        cfg = CFG(productions=productions, start_symbol=var_s)
        cfg = cfg.to_pda().to_final_state().to_empty_stack().to_cfg()
        cfg = cfg.to_pda().to_final_state().to_empty_stack().to_cfg()
        cfg.to_pda().to_final_state().to_empty_stack().to_cfg()

    def test_generation_words(self):
        """ Tests the generation of word """
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        productions = {Production(var_s, [ter_a, var_s, ter_b]),
                       Production(var_s, [])}
        cfg = CFG(productions=productions, start_symbol=var_s)
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
        var_s = Variable("S")
        var_s1 = Variable("S1")
        var_s2 = Variable("S2")
        productions = {Production(var_s, [var_s1, ter_a]),
                       Production(var_s1, [var_s2, ter_a]),
                       Production(var_s1, []),
                       Production(var_s2, []),
                       Production(var_s, [])}
        cfg = CFG(productions=productions, start_symbol=var_s)
        words0 = list(cfg.get_words())
        self.assertIn([], words0)
        self.assertIn([ter_a], words0)
        self.assertIn([ter_a, ter_a], words0)
        self.assertEqual(len(words0), 3)

    def test_finite(self):
        """ Tests whether a grammar is finite or not """
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        var_a = Variable("A")
        var_b = Variable("B")
        prod0 = {Production(var_s, [var_a, var_b]),
                 Production(var_a, [ter_a]),
                 Production(var_b, [ter_b])}
        cfg = CFG(productions=prod0, start_symbol=var_s)
        self.assertTrue(cfg.is_finite())
        prod0.add(Production(var_a, [var_s]))
        cfg = CFG(productions=prod0, start_symbol=var_s)
        self.assertFalse(cfg.is_finite())

    def test_intersection(self):
        """ Tests the intersection with a regex """
        regex = Regex("a*b*")
        dfa = regex.to_epsilon_nfa()
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        self.assertTrue(dfa.accepts([symb_a, symb_a, symb_b, symb_b]))
        self.assertFalse(dfa.accepts([symb_b, symb_b, symb_a]))
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        productions = {Production(var_s, [ter_a, var_s, ter_b]),
                       Production(var_s, [ter_b, var_s, ter_a]),
                       Production(var_s, [])}
        cfg = CFG(productions=productions, start_symbol=var_s)
        self.assertTrue(cfg.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg.contains([ter_a, ter_a, ter_b]))
        cfg_i = cfg.intersection(regex)
        self.assertTrue(cfg_i.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg_i.contains([ter_a, ter_a, ter_b]))
        self.assertTrue(cfg_i.contains([]))
        cfg_i = cfg.intersection(dfa)
        self.assertTrue(cfg_i.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg_i.contains([ter_a, ter_a, ter_b]))
        self.assertTrue(cfg_i.contains([]))

    def test_intersection_empty(self):
        regex = Regex("")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        productions = {Production(var_s, [ter_a, var_s, ter_b]),
                       Production(var_s, [ter_b, var_s, ter_a]),
                       Production(var_s, [])}
        cfg = CFG(productions=productions, start_symbol=var_s)
        cfg_i = cfg & regex
        self.assertFalse(cfg_i)

    def test_intersection_dfa(self):
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        dfa = DeterministicFiniteAutomaton({state0, state1},
                                           {symb_a, symb_b},
                                           start_state=state0,
                                           final_states={state0, state1})
        dfa.add_transition(state0, symb_a, state0)
        dfa.add_transition(state0, symb_b, state1)
        dfa.add_transition(state1, symb_b, state1)
        self.assertTrue(dfa.accepts([symb_a, symb_a, symb_b, symb_b]))
        self.assertFalse(dfa.accepts([symb_b, symb_b, symb_a]))

        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        productions = {Production(var_s, [ter_a, var_s, ter_b]),
                       Production(var_s, [ter_b, var_s, ter_a]),
                       Production(var_s, [])}
        cfg = CFG(productions=productions, start_symbol=var_s)
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
                                           start_state=state0,
                                           final_states={state1})
        dfa.add_transition(state0, symb_a, state1)
        self.assertTrue(dfa.accepts([symb_a]))

        ter_a = Terminal("a")
        var_s = Variable("S")
        var_l = Variable("L")
        var_t = Variable("T")
        productions = {Production(var_s, [var_l, var_t]),
                       Production(var_l, [Epsilon()]),
                       Production(var_t, [ter_a]),
                       Production(var_t, [Epsilon()])}
        cfg = CFG(productions=productions, start_symbol=var_s)
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
        state0 = State(0)
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        dfa = DeterministicFiniteAutomaton({state0},
                                           {symb_a, symb_b},
                                           start_state=state0,
                                           final_states={state0})
        dfa.add_transition(state0, symb_a, state0)
        dfa.add_transition(state0, symb_b, state0)
        self.assertTrue(dfa.accepts([symb_a, symb_a, symb_b, symb_b]))

        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        var_s1 = Variable("S1")
        var_l = Variable("L")
        productions = {Production(var_s, [var_l, var_s1]),
                       Production(var_l, [Epsilon()]),
                       Production(var_s1, [ter_a, var_s1, ter_b]),
                       Production(var_s1, [ter_b, var_s1, ter_a]),
                       Production(var_s1, [])}
        cfg = CFG(productions=productions, start_symbol=var_s)
        self.assertTrue(cfg.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertFalse(cfg.contains([ter_a, ter_a, ter_b]))
        cfg_i = cfg.intersection(dfa)
        self.assertFalse(cfg_i.is_empty())
        self.assertTrue(cfg_i.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertTrue(cfg_i.contains([]))

    def test_profiling_intersection(self):
        size = 3
        states = [State(i) for i in range(size * 2 + 1)]
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        dfa = DeterministicFiniteAutomaton(states,
                                           {symb_a, symb_b},
                                           start_state=states[0],
                                           final_states={states[-1]})
        for i in range(size):
            dfa.add_transition(states[i], symb_a, states[i + 1])
        for i in range(size, size * 2):
            dfa.add_transition(states[i], symb_b, states[i + 1])

        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        var_s1 = Variable("S1")
        var_l = Variable("L")
        productions = [Production(var_s, [var_l, var_s1]),
                       Production(var_l, [Epsilon()]),
                       Production(var_s1, [ter_a, var_s1, ter_b]),
                       Production(var_s1, [ter_b, var_s1, ter_a]),
                       Production(var_s1, [])]
        cfg = CFG(productions=productions, start_symbol=var_s)
        cfg_i = cfg.intersection(dfa)
        self.assertFalse(cfg_i.is_empty())
        self.assertTrue(cfg_i.contains([ter_a] * size + [ter_b] * size))
        self.assertFalse(cfg_i.contains([]))

    def test_pda_object_creator(self):
        pda_oc = PDAObjectCreator([], [])
        self.assertEqual(pda_oc.get_symbol_from(Epsilon()), pda.Epsilon())
        self.assertEqual(pda_oc.get_stack_symbol_from(Epsilon()),
                         pda.Epsilon())

    def test_string_variable(self):
        var = Variable("A")
        self.assertEqual(repr(var), "Variable(A)")

    def test_get_leftmost_derivation(self):
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        var_a = Variable("A")
        var_b = Variable("B")
        var_c = Variable("C")
        productions = [Production(var_s, [var_c, var_b]),
                       Production(var_c, [var_a, var_a]),
                       Production(var_a, [ter_a]),
                       Production(var_b, [ter_b])
                       ]
        cfg = CFG(productions=productions, start_symbol=var_s)
        parse_tree = cfg.get_cnf_parse_tree([ter_a, ter_a, ter_b])
        derivation = parse_tree.get_leftmost_derivation()
        self.assertEqual(derivation,
                         [[var_s],
                          [var_c, var_b],
                          [var_a, var_a, var_b],
                          [ter_a, var_a, var_b],
                          [ter_a, ter_a, var_b],
                          [ter_a, ter_a, ter_b]])
        with self.assertRaises(DerivationDoesNotExist):
            cfg.get_cnf_parse_tree([])

    def test_get_rightmost_derivation(self):
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        var_s = Variable("S")
        var_a = Variable("A")
        var_b = Variable("B")
        var_c = Variable("C")
        productions = [Production(var_s, [var_c, var_b]),
                       Production(var_c, [var_a, var_a]),
                       Production(var_a, [ter_a]),
                       Production(var_b, [ter_b])
                       ]
        cfg = CFG(productions=productions, start_symbol=var_s)
        parse_tree = cfg.get_cnf_parse_tree([ter_a, ter_a, ter_b])
        derivation = parse_tree.get_rightmost_derivation()
        self.assertEqual(derivation,
                         [[var_s],
                          [var_c, var_b],
                          [var_c, ter_b],
                          [var_a, var_a, ter_b],
                          [var_a, ter_a, ter_b],
                          [ter_a, ter_a, ter_b]])

    def test_derivation_does_not_exist(self):
        var_s = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        cfg = CFG(productions=[], start_symbol=var_s)
        with self.assertRaises(DerivationDoesNotExist):
            parse_tree = cfg.get_cnf_parse_tree([ter_a, ter_b])
            parse_tree.get_rightmost_derivation()

    def test_derivation_empty(self):
        var_s = Variable("S")
        productions = [Production(var_s, [Epsilon()])]
        cfg = CFG(productions=productions, start_symbol=var_s)
        parse_tree = cfg.get_cnf_parse_tree([])
        derivation = parse_tree.get_rightmost_derivation()
        self.assertEqual([[var_s], []], derivation)

    def test_from_text(self):
        text = """
        S ->  A  B
        A -> Bobo r
        """
        cfg = CFG.from_text(text)
        self.assertEqual(len(cfg.variables), 4)
        self.assertEqual(len(cfg.productions), 2)
        self.assertEqual(len(cfg.terminals), 1)
        self.assertEqual(cfg.start_symbol, Variable("S"))

    def test_from_text2(self):
        text = """
        S  -> A B\n\rA -> a
        B -> b\r
        """
        cfg = CFG.from_text(text)
        self.assertTrue(cfg.contains(["a", "b"]))
        self.assertTrue(["a", "b"] in cfg)

    def test_from_text_union(self):
        text = """
        "VAR:S" -> TER:a | b
        """
        cfg = CFG.from_text(text)
        self.assertEqual(2, len(cfg.productions))

    def test_epsilon(self):
        text = "S -> epsilon"
        cfg = CFG.from_text(text)
        self.assertTrue(cfg.generate_epsilon())
        self.assertEqual(len(cfg.terminals), 0)

    def test_epsilon2(self):
        text = "S ->$"
        cfg = CFG.from_text(text)
        self.assertTrue(cfg.generate_epsilon())

    def test_generate_epsilon(self):
        var_s = Variable("S")
        ter_a = Terminal("a")
        productions = [Production(var_s, [ter_a])]
        cfg = CFG(productions=productions, start_symbol=var_s)
        self.assertFalse(cfg.generate_epsilon())

    def test_change_starting_variable(self):
        text = """S1 -> a"""
        cfg = CFG.from_text(text, start_symbol="S1")
        self.assertEqual(Variable("S1"), cfg.start_symbol)

    def test_is_not_normal_form(self):
        text = get_example_text_duplicate()
        cfg = CFG.from_text(text, start_symbol="E")
        self.assertFalse(cfg.is_normal_form())

    def test_is_normal_form(self):
        text = """
                            E  -> T E’
                            E’ -> T E’
                            T  -> F T’
                            T’ -> *
                            F  -> ( | id
                        """
        cfg = CFG.from_text(text, start_symbol="E")
        self.assertTrue(cfg.is_normal_form())

    def test_to_text(self):
        text = """E  -> T E’
            E’ -> T E’
            T  -> F T’
            T’ -> *
            F  -> ( | id
            """
        text_result = CFG.from_text(text, start_symbol="E").to_text()
        self.assertIn("E -> T E’", text_result)
        self.assertIn("E’ -> T E’", text_result)
        self.assertIn("T -> F T’", text_result)
        self.assertIn("T’ -> *", text_result)
        self.assertIn("F -> (", text_result)
        self.assertIn("F -> id", text_result)

    def test_to_text_cnf(self):
        cfg = CFG.from_text("S -> a S b | a b")
        cnf = cfg.to_normal_form()
        self.assertTrue(cnf.contains(["a", "b"]))
        new_text = cnf.to_text()
        print(new_text)
        new_cfg = CFG.from_text(new_text)
        self.assertTrue(new_cfg.contains(["a", "b"]))

    def test_to_text_epsilon(self):
        cfg = CFG.from_text("S -> a S b | a b epsilon")
        self.assertTrue(cfg.contains(["a", "b"]))


def get_example_text_duplicate():
    """ Duplicate text """
    text = """
                        E  -> T E’
                        E’ -> + T E’ | Є
                        T  -> F T’
                        T’ -> * F T’ | Є
                        F  -> ( E ) | id
                    """
    return text
