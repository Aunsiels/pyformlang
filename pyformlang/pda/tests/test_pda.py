""" Tests the PDA """

import unittest
from os import path

from pyformlang.pda import PDA, State, StackSymbol, Symbol, Epsilon
from pyformlang.cfg import Terminal
from pyformlang import finite_automaton
from pyformlang.pda.utils import PDAObjectCreator
from pyformlang.regular_expression import Regex


class TestPDA(unittest.TestCase):
    """ Tests the pushdown automata """

    def test_creation(self):
        """ Test of creation """
        pda = PDA()
        self.assertIsNotNone(pda)
        self.assertEqual(len(pda.states), 0)
        self.assertEqual(len(pda.final_states), 0)
        self.assertEqual(len(pda.input_symbols), 0)
        self.assertEqual(len(pda.stack_symbols), 0)
        self.assertEqual(len(pda.to_dict()), 0)

        pda = PDA(start_state=State("A"))
        self.assertIsNotNone(pda)
        self.assertEqual(len(pda.states), 1)
        self.assertEqual(len(pda.stack_symbols), 0)
        self.assertEqual(len(pda.final_states), 0)

        pda = PDA(final_states={State("A"), State("A"), State("B"),
                                Symbol("B")})
        self.assertIsNotNone(pda)
        self.assertEqual(len(pda.states), 3)
        self.assertEqual(len(pda.input_symbols), 0)
        self.assertEqual(len(pda.stack_symbols), 0)
        self.assertEqual(len(pda.final_states), 3)

        pda = PDA(input_symbols={Symbol("A"), Symbol("B"),
                                 Symbol("A"), State("A")})
        self.assertIsNotNone(pda)
        self.assertEqual(len(pda.states), 0)
        self.assertEqual(len(pda.input_symbols), 3)
        self.assertEqual(len(pda.stack_symbols), 0)
        self.assertEqual(len(pda.final_states), 0)

        pda = PDA(start_stack_symbol=StackSymbol("A"))
        self.assertIsNotNone(pda)
        self.assertEqual(len(pda.input_symbols), 0)
        self.assertEqual(len(pda.states), 0)
        self.assertEqual(len(pda.stack_symbols), 1)
        self.assertEqual(len(pda.final_states), 0)

        pda = PDA(stack_alphabet={StackSymbol("A"), StackSymbol("A"),
                                  StackSymbol("B")})
        self.assertIsNotNone(pda)
        self.assertEqual(len(pda.states), 0)
        self.assertEqual(len(pda.input_symbols), 0)
        self.assertEqual(len(pda.stack_symbols), 2)
        self.assertEqual(len(pda.final_states), 0)

        pda = PDA(input_symbols={Epsilon()})
        self.assertIsNotNone(pda)
        self.assertEqual(len(pda.states), 0)
        self.assertEqual(len(pda.input_symbols), 1)
        self.assertEqual(len(pda.stack_symbols), 0)
        self.assertEqual(pda.get_number_transitions(), 0)
        self.assertEqual(len(pda.final_states), 0)

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
        self.assertEqual(len(pda.states), 2)
        self.assertEqual(len(pda.input_symbols), 1)
        self.assertEqual(len(pda.stack_symbols), 3)
        self.assertEqual(pda.get_number_transitions(), 1)
        pda.add_transition(State("from"),
                           Epsilon(),
                           StackSymbol("stack symbol"),
                           State("to"),
                           [StackSymbol("A"), StackSymbol("B")])
        self.assertEqual(len(pda.states), 2)
        self.assertEqual(len(pda.input_symbols), 1)
        self.assertEqual(len(pda.stack_symbols), 3)
        self.assertEqual(pda.get_number_transitions(), 2)

    def test_example62(self):
        """ Example from the book """
        state0 = State("q0")
        state1 = State("q1")
        state2 = State("q2")
        s_zero = Symbol("0")
        s_one = Symbol("1")
        ss_zero = StackSymbol("0")
        ss_one = StackSymbol("1")
        ss_z0 = StackSymbol("Z0")
        pda = PDA(states={state0, state1, state2},
                  input_symbols={s_zero, s_one},
                  stack_alphabet={ss_zero, ss_one, ss_z0},
                  start_state=state0,
                  start_stack_symbol=ss_z0,
                  final_states={state2})
        self.assertEqual(len(pda.states), 3)
        self.assertEqual(len(pda.input_symbols), 2)
        self.assertEqual(len(pda.stack_symbols), 3)
        self.assertEqual(pda.get_number_transitions(), 0)

        pda.add_transition(state0, s_zero, ss_z0, state0, [ss_zero, ss_z0])
        pda.add_transition(state0, s_one, ss_z0, state0, [ss_one, ss_z0])

        pda.add_transition(state0, s_zero, ss_zero, state0, [ss_zero, ss_zero])
        pda.add_transition(state0, s_one, ss_one, state0, [ss_zero, ss_one])
        pda.add_transition(state0, s_one, ss_zero, state0, [ss_one, ss_zero])
        pda.add_transition(state0, s_one, ss_one, state0, [ss_one, ss_one])

        pda.add_transition(state0, Epsilon(), ss_z0, state1, [ss_z0])
        pda.add_transition(state0, Epsilon(), ss_zero, state1, [ss_zero])
        pda.add_transition(state0, Epsilon(), ss_one, state1, [ss_one])

        pda.add_transition(state1, s_zero, ss_zero, state1, [])
        pda.add_transition(state1, s_one, ss_one, state1, [])

        pda.add_transition(state1, Epsilon(), ss_z0, state2, [ss_z0])

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
        state = State("#STARTTOFINAL#")
        symbol_e = Symbol("e")
        symbol_i = Symbol("i")
        symbol_z = StackSymbol("Z")
        pda = PDA(states={state},
                  input_symbols={symbol_i, symbol_e},
                  stack_alphabet={symbol_z},
                  start_state=state,
                  start_stack_symbol=symbol_z)
        pda.add_transition(state,
                           symbol_i,
                           symbol_z,
                           state,
                           [symbol_z, symbol_z])
        pda.add_transition(state, symbol_e, symbol_z, state, [])
        new_pda = pda.to_final_state()
        self.assertEqual(len(new_pda.states), 3)
        self.assertEqual(len(new_pda.input_symbols), 2)
        self.assertEqual(len(new_pda.stack_symbols), 2)
        self.assertEqual(new_pda.get_number_transitions(), 4)
        self.assertEqual(len(new_pda.final_states), 1)

    def test_to_empty_stack(self):
        """ Test transformation to empty stack """
        state_q = State("#STARTTOFINAL#")
        state_q0 = State("q0")
        symbol_e = Symbol("e")
        symbol_i = Symbol("i")
        symbol_z = StackSymbol("Z")
        symbol_z0 = StackSymbol("Z0")
        pda = PDA(states={state_q, state_q0},
                  input_symbols={symbol_i, symbol_e},
                  stack_alphabet={symbol_z, symbol_z0},
                  start_state=state_q,
                  start_stack_symbol=symbol_z0,
                  final_states={state_q0})
        pda.add_transition(state_q, symbol_i, symbol_z, state_q,
                           [symbol_z, symbol_z])
        pda.add_transition(state_q, symbol_i, symbol_z0, state_q,
                           [symbol_z, symbol_z0])
        pda.add_transition(state_q, symbol_e, symbol_z, state_q, [])
        pda.add_transition(state_q, Epsilon(), symbol_z0, state_q0, [])
        new_pda = pda.to_empty_stack()
        self.assertEqual(len(new_pda.states), 4)
        self.assertEqual(len(new_pda.input_symbols), 2)
        self.assertEqual(len(new_pda.stack_symbols), 3)
        self.assertEqual(new_pda.get_number_transitions(), 11)
        self.assertEqual(len(new_pda.final_states), 0)

    def test_to_cfg(self):
        """ Test the transformation to CFG """
        state_q = State("#STARTTOFINAL#")
        symbol_e = Symbol("e")
        symbol_i = Symbol("i")
        symbol_z = StackSymbol("Z")
        pda = PDA(states={state_q},
                  input_symbols={symbol_i, symbol_e},
                  stack_alphabet={symbol_z},
                  start_state=state_q,
                  start_stack_symbol=symbol_z)
        pda.add_transition(state_q, symbol_i, symbol_z, state_q,
                           [symbol_z, symbol_z])
        pda.add_transition(state_q, symbol_e, symbol_z, state_q, [])
        cfg = pda.to_cfg()
        self.assertEqual(len(cfg.variables), 2)
        self.assertEqual(len(cfg.terminals), 2)
        self.assertEqual(len(cfg.productions), 3)

        pda = PDA(states={"q"},
                  input_symbols={"i", "e"},
                  stack_alphabet={"Z"},
                  start_state="q",
                  start_stack_symbol="Z")
        pda.add_transition("q", "i", "Z", "q", ("Z", "Z"))
        pda.add_transition("q", "e", "Z", "q", [])
        cfg = pda.to_cfg()
        self.assertEqual(len(cfg.variables), 2)
        self.assertEqual(len(cfg.terminals), 2)
        self.assertEqual(len(cfg.productions), 3)
        pda.add_transition("q", "epsilon", "Z", "q", ["Z"])

    def test_pda_conversion(self):
        """ Tests conversions from a PDA """
        state_p = State("p")
        state_q = State("q")
        state_a = Symbol("a")
        state_b = Symbol("b")
        state_c = Symbol("c")
        terminal_a = Terminal("a")
        terminal_b = Terminal("b")
        terminal_c = Terminal("c")
        stack_symbol_a = StackSymbol("a")
        stack_symbol_b = StackSymbol("b")
        stack_symbol_c = StackSymbol("c")
        stack_symbol_x0 = StackSymbol("X0")
        pda = PDA(states={state_p, state_q},
                  input_symbols={state_a, state_b, state_c},
                  stack_alphabet={stack_symbol_a, stack_symbol_b,
                                  stack_symbol_c, stack_symbol_x0},
                  start_state=state_p,
                  start_stack_symbol=stack_symbol_x0,
                  final_states={state_q})
        pda.add_transition(state_p, Epsilon(), stack_symbol_x0, state_q, [])
        pda.add_transition(state_p, Epsilon(), stack_symbol_x0, state_p,
                           [stack_symbol_a, stack_symbol_b,
                            stack_symbol_c, stack_symbol_x0])
        pda.add_transition(state_p, state_a, stack_symbol_a, state_p, [])
        pda.add_transition(state_p, state_b, stack_symbol_b, state_p, [])
        pda.add_transition(state_p, state_c, stack_symbol_c, state_p, [])
        cfg = pda.to_empty_stack().to_cfg()
        self.assertTrue(cfg.contains([]))
        self.assertTrue(cfg.contains([terminal_a, terminal_b, terminal_c]))
        self.assertFalse(cfg.contains([terminal_c, terminal_b, terminal_a]))

    def test_intersection_regex(self):
        """ Tests the intersection with a regex """
        # pylint: disable=too-many-locals
        state_p = State("p")
        state_q = State("q")
        state_r = State("r")
        state_i = Symbol("i")
        state_e = Symbol("e")
        state_z = StackSymbol("Z")
        state_x0 = StackSymbol("X0")
        pda = PDA(states={state_p, state_q, state_r},
                  input_symbols={state_i, state_e},
                  stack_alphabet={state_z, state_x0},
                  start_state=state_p,
                  start_stack_symbol=state_x0,
                  final_states={state_r})
        pda.add_transition(state_p, Epsilon(), state_x0, state_q,
                           [state_z, state_x0])
        pda.add_transition(state_q, state_i, state_z, state_q,
                           [state_z, state_z])
        pda.add_transition(state_q, state_e, state_z, state_q, [])
        pda.add_transition(state_q, Epsilon(), state_x0, state_r, [])

        state_s = finite_automaton.State("s")
        state_t = finite_automaton.State("t")
        i_dfa = finite_automaton.Symbol("i")
        e_dfa = finite_automaton.Symbol("e")
        dfa = finite_automaton.DeterministicFiniteAutomaton(
            states={state_s, state_t},
            input_symbols={i_dfa, e_dfa},
            start_state=state_s,
            final_states={state_s, state_t})
        dfa.add_transition(state_s, i_dfa, state_s)
        dfa.add_transition(state_s, e_dfa, state_t)
        dfa.add_transition(state_t, e_dfa, state_t)

        new_pda = pda.intersection(dfa)
        pda_es = new_pda.to_empty_stack()
        cfg = pda_es.to_cfg()
        self.assertEqual(new_pda.get_number_transitions(), 6)
        self.assertEqual(len(new_pda.states), 5)
        self.assertEqual(len(new_pda.final_states), 2)
        self.assertEqual(len(new_pda.input_symbols), 2)
        self.assertEqual(len(new_pda.stack_symbols), 2)

        i_cfg = Terminal("i")
        e_cfg = Terminal("e")

        self.assertTrue(cfg.contains([i_cfg, i_cfg, e_cfg, e_cfg, e_cfg]))

        new_pda = pda.intersection(
            finite_automaton.DeterministicFiniteAutomaton())
        self.assertEqual(new_pda.get_number_transitions(), 0)

        new_pda = pda.intersection(Regex(""))
        pda_es = new_pda.to_empty_stack()
        cfg = pda_es.to_cfg()
        self.assertFalse(cfg)

        new_pda = pda & Regex("z|y").to_epsilon_nfa()
        pda_es = new_pda.to_empty_stack()
        cfg = pda_es.to_cfg()
        self.assertFalse(cfg)

    def test_pda_object_creator_epsilon(self):
        """ Test creation objects """
        poc = PDAObjectCreator()
        self.assertEqual(poc.to_stack_symbol(Epsilon()), Epsilon())

    def test_pda_paper(self):
        """ Code in the paper """
        pda = PDA()
        pda.add_transitions(
            [
                ("q0", "0", "Z0", "q1", ("Z1", "Z0")),
                ("q1", "1", "Z1", "q2", []),
                ("q0", "epsilon", "Z1", "q2", [])
            ]
        )
        pda.set_start_state("q0")
        pda.set_start_stack_symbol("Z0")
        pda.add_final_state("q2")
        pda_final_state = pda.to_final_state()
        self.assertIsNotNone(pda_final_state)
        cfg = pda.to_empty_stack().to_cfg()
        self.assertTrue(cfg.contains(["0", "1"]))
        pda_networkx = PDA.from_networkx(pda.to_networkx())
        self.assertEqual(pda.states, pda_networkx.states)
        self.assertEqual(pda.start_state, pda_networkx.start_state)
        self.assertEqual(pda.final_states, pda_networkx.final_states)
        self.assertEqual(pda.input_symbols, pda_networkx.input_symbols)
        self.assertEqual(pda.stack_symbols, pda_networkx.stack_symbols)
        cfg = pda_networkx.to_empty_stack().to_cfg()
        pda_networkx.write_as_dot("pda.dot")
        self.assertTrue(cfg.contains(["0", "1"]))
        self.assertTrue(path.exists("pda.dot"))
