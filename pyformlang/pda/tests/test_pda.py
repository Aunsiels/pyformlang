""" Tests the PDA """

import unittest

from pyformlang.pda import PDA, State, StackSymbol, Symbol, Epsilon
from pyformlang.cfg import Terminal
from pyformlang import finite_automaton

class TestPDA(unittest.TestCase):
    """ Tests the pushdown automata """

    def test_creation(self):
        """ Test of creation """
        pda = PDA()
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_final_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 0)
        self.assertEqual(pda.get_number_stack_symbols(), 0)

        pda = PDA(start_state=State("A"))
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 1)
        self.assertEqual(pda.get_number_stack_symbols(), 0)
        self.assertEqual(pda.get_number_final_states(), 0)

        pda = PDA(final_states={State("A"), State("A"), State("B"),
                                Symbol("B")})
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 3)
        self.assertEqual(pda.get_number_input_symbols(), 0)
        self.assertEqual(pda.get_number_stack_symbols(), 0)
        self.assertEqual(pda.get_number_final_states(), 3)

        pda = PDA(input_symbols={Symbol("A"), Symbol("B"),
                                 Symbol("A"), State("A")})
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 3)
        self.assertEqual(pda.get_number_stack_symbols(), 0)
        self.assertEqual(pda.get_number_final_states(), 0)

        pda = PDA(start_stack_symbol=StackSymbol("A"))
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_input_symbols(), 0)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_stack_symbols(), 1)
        self.assertEqual(pda.get_number_final_states(), 0)

        pda = PDA(stack_alphabet={StackSymbol("A"), StackSymbol("A"),
                                  StackSymbol("B")})
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 0)
        self.assertEqual(pda.get_number_stack_symbols(), 2)
        self.assertEqual(pda.get_number_final_states(), 0)

        pda = PDA(input_symbols={Epsilon()})
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 1)
        self.assertEqual(pda.get_number_stack_symbols(), 0)
        self.assertEqual(pda.get_number_transitions(), 0)
        self.assertEqual(pda.get_number_final_states(), 0)

    def test_represent(self):
        """ Tests representations """
        symb = Symbol("S")
        self.assertEqual(str(symb), "Symbol(S)")
        state = State("T")
        self.assertEqual(str(state), "State(T)")
        stack_symb = StackSymbol("U")
        self.assertEqual(str(stack_symb), "StackSymbol(U)")

    def test_transition(self):
        """ Tests the creation of transition """
        pda = PDA()
        pda.add_transition(State("from"),
                           Symbol("input symbol"),
                           StackSymbol("stack symbol"),
                           State("to"),
                           [StackSymbol("A"), StackSymbol("B")])
        self.assertEqual(pda.get_number_states(), 2)
        self.assertEqual(pda.get_number_input_symbols(), 1)
        self.assertEqual(pda.get_number_stack_symbols(), 3)
        self.assertEqual(pda.get_number_transitions(), 1)
        pda.add_transition(State("from"),
                           Epsilon(),
                           StackSymbol("stack symbol"),
                           State("to"),
                           [StackSymbol("A"), StackSymbol("B")])
        self.assertEqual(pda.get_number_states(), 2)
        self.assertEqual(pda.get_number_input_symbols(), 1)
        self.assertEqual(pda.get_number_stack_symbols(), 3)
        self.assertEqual(pda.get_number_transitions(), 2)

    def test_example62(self):
        """ Example from the book """
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        s_zero = Symbol("0")
        s_one = Symbol("1")
        ss_zero = StackSymbol("0")
        ss_one = StackSymbol("1")
        ss_z0 = StackSymbol("Z0")
        pda = PDA(states={q0, q1, q2},
                  input_symbols={s_zero, s_one},
                  stack_alphabet={ss_zero, ss_one, ss_z0},
                  start_state=q0,
                  start_stack_symbol=ss_z0,
                  final_states={q2})
        self.assertEqual(pda.get_number_states(), 3)
        self.assertEqual(pda.get_number_input_symbols(), 2)
        self.assertEqual(pda.get_number_stack_symbols(), 3)
        self.assertEqual(pda.get_number_transitions(), 0)

        pda.add_transition(q0, s_zero, ss_z0, q0, [ss_zero, ss_z0])
        pda.add_transition(q0, s_one, ss_z0, q0, [ss_one, ss_z0])

        pda.add_transition(q0, s_zero, ss_zero, q0, [ss_zero, ss_zero])
        pda.add_transition(q0, s_one, ss_one, q0, [ss_zero, ss_one])
        pda.add_transition(q0, s_one, ss_zero, q0, [ss_one, ss_zero])
        pda.add_transition(q0, s_one, ss_one, q0, [ss_one, ss_one])

        pda.add_transition(q0, Epsilon(), ss_z0, q1, [ss_z0])
        pda.add_transition(q0, Epsilon(), ss_zero, q1, [ss_zero])
        pda.add_transition(q0, Epsilon(), ss_one, q1, [ss_one])

        pda.add_transition(q1, s_zero, ss_zero, q1, [])
        pda.add_transition(q1, s_one, ss_one, q1, [])

        pda.add_transition(q1, Epsilon(), ss_z0, q2, [ss_z0])

        self.assertEqual(pda.get_number_transitions(), 12)

        t_zero = Terminal("0")
        t_one = Terminal("1")
        cfg = pda.to_empty_stack().to_cfg()
        self.assertTrue(cfg.contains([]))
        self.assertTrue(cfg.contains([t_zero, t_zero]))
        self.assertTrue(cfg.contains([t_zero, t_one, t_one, t_zero]))
        self.assertFalse(cfg.contains([t_zero]))
        self.assertFalse(cfg.contains([t_zero, t_one, t_zero]))

    def test_to_final_state(self):
        """ Test transformation to final state """
        q = State("#STARTTOFINAL#")
        e = Symbol("e")
        i = Symbol("i")
        Z = StackSymbol("Z")
        pda = PDA(states={q},
                  input_symbols={i, e},
                  stack_alphabet={Z},
                  start_state=q,
                  start_stack_symbol=Z)
        pda.add_transition(q, i, Z, q, (Z, Z))
        pda.add_transition(q, e, Z, q, [])
        new_pda = pda.to_final_state()
        self.assertEqual(new_pda.get_number_states(), 3)
        self.assertEqual(new_pda.get_number_input_symbols(), 2)
        self.assertEqual(new_pda.get_number_stack_symbols(), 2)
        self.assertEqual(new_pda.get_number_transitions(), 4)
        self.assertEqual(new_pda.get_number_final_states(), 1)

    def test_to_empty_stack(self):
        """ Test transformation to empty stack """
        q = State("#STARTTOFINAL#")
        q0 = State("q0")
        e = Symbol("e")
        i = Symbol("i")
        Z = StackSymbol("Z")
        Z0 = StackSymbol("Z0")
        pda = PDA(states={q, q0},
                  input_symbols={i, e},
                  stack_alphabet={Z, Z0},
                  start_state=q,
                  start_stack_symbol=Z0,
                  final_states={q0})
        pda.add_transition(q, i, Z, q, (Z, Z))
        pda.add_transition(q, i, Z0, q, (Z, Z0))
        pda.add_transition(q, e, Z, q, [])
        pda.add_transition(q, Epsilon(), Z0, q0, [])
        new_pda = pda.to_empty_stack()
        self.assertEqual(new_pda.get_number_states(), 4)
        self.assertEqual(new_pda.get_number_input_symbols(), 2)
        self.assertEqual(new_pda.get_number_stack_symbols(), 3)
        self.assertEqual(new_pda.get_number_transitions(), 11)
        self.assertEqual(new_pda.get_number_final_states(), 0)

    def test_to_cfg(self):
        """ Test the transformation to CFG """
        q = State("#STARTTOFINAL#")
        e = Symbol("e")
        i = Symbol("i")
        Z = StackSymbol("Z")
        pda = PDA(states={q},
                  input_symbols={i, e},
                  stack_alphabet={Z},
                  start_state=q,
                  start_stack_symbol=Z)
        pda.add_transition(q, i, Z, q, (Z, Z))
        pda.add_transition(q, e, Z, q, [])
        cfg = pda.to_cfg()
        self.assertEqual(cfg.get_number_variables(), 2)
        self.assertEqual(cfg.get_number_terminals(), 2)
        self.assertEqual(cfg.get_number_productions(), 3)

        pda = PDA(states={"q"},
                  input_symbols={"i", "e"},
                  stack_alphabet={"Z"},
                  start_state="q",
                  start_stack_symbol="Z")
        pda.add_transition("q", "i", "Z", "q", ("Z", "Z"))
        pda.add_transition("q", "e", "Z", "q", [])
        cfg = pda.to_cfg()
        self.assertEqual(cfg.get_number_variables(), 2)
        self.assertEqual(cfg.get_number_terminals(), 2)
        self.assertEqual(cfg.get_number_productions(), 3)
        pda.add_transition("q", "epsilon", "Z", "q", ["Z"])

    def test_pda_conversion(self):
        """ Tests conversions from a PDA """
        p = State("p")
        q = State("q")
        s_a = Symbol("a")
        s_b = Symbol("b")
        s_c = Symbol("c")
        t_a = Terminal("a")
        t_b = Terminal("b")
        t_c = Terminal("c")
        ss_a = StackSymbol("a")
        ss_b = StackSymbol("b")
        ss_c = StackSymbol("c")
        X0 = StackSymbol("X0")
        pda = PDA(states={p,q},
                  input_symbols={s_a, s_b, s_c},
                  stack_alphabet={ss_a, ss_b, ss_c, X0},
                  start_state=p,
                  start_stack_symbol=X0,
                  final_states={q})
        pda.add_transition(p, Epsilon(), X0, q, [])
        pda.add_transition(p, Epsilon(), X0, p, [ss_a, ss_b, ss_c, X0])
        pda.add_transition(p, s_a, ss_a, p, [])
        pda.add_transition(p, s_b, ss_b, p, [])
        pda.add_transition(p, s_c, ss_c, p, [])
        cfg = pda.to_empty_stack().to_cfg()
        self.assertTrue(cfg.contains([]))
        self.assertTrue(cfg.contains([t_a, t_b, t_c]))
        self.assertFalse(cfg.contains([t_c, t_b, t_a]))

    def test_intersection_regex(self):
        """ Tests the intersection with a regex """
        p = State("p")
        q = State("q")
        r = State("r")
        i = Symbol("i")
        e = Symbol("e")
        Z = StackSymbol("Z")
        X0 = StackSymbol("X0")
        pda = PDA(states={p, q, r},
                  input_symbols={i, e},
                  stack_alphabet={Z, X0},
                  start_state=p,
                  start_stack_symbol=X0,
                  final_states={r})
        pda.add_transition(p, Epsilon(), X0, q, [Z, X0])
        pda.add_transition(q, i, Z, q, [Z, Z])
        pda.add_transition(q, e, Z, q, [])
        pda.add_transition(q, Epsilon(), X0, r, [])

        s = finite_automaton.State("s")
        t = finite_automaton.State("t")
        i_dfa = finite_automaton.Symbol("i")
        e_dfa = finite_automaton.Symbol("e")
        dfa = finite_automaton.DeterministicFiniteAutomaton(
            states={s, t},
            input_symbols={i_dfa, e_dfa},
            start_state=s,
            final_states={s, t})
        dfa.add_transition(s, i_dfa, s)
        dfa.add_transition(s, e_dfa, t)
        dfa.add_transition(t, e_dfa, t)

        new_pda = pda.intersection(dfa)
        pda_es = new_pda.to_empty_stack()
        cfg = pda_es.to_cfg()
        self.assertEqual(new_pda.get_number_transitions(), 6)
        self.assertEqual(new_pda.get_number_states(), 5)
        self.assertEqual(new_pda.get_number_final_states(), 2)
        self.assertEqual(new_pda.get_number_input_symbols(), 2)
        self.assertEqual(new_pda.get_number_stack_symbols(), 2)

        i_cfg = Terminal("i")
        e_cfg = Terminal("e")

        self.assertTrue(cfg.contains([i_cfg, i_cfg, e_cfg, e_cfg, e_cfg]))

        new_pda = pda.intersection(finite_automaton.DeterministicFiniteAutomaton())
        self.assertEqual(new_pda.get_number_transitions(), 0)
