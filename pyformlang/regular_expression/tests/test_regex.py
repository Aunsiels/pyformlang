"""
Tests for regular expressions
"""

import pytest

from pyformlang.regular_expression import Regex, MisformedRegexError
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State, Symbol, Epsilon
from pyformlang.finite_automaton.tests.test_deterministic_finite_automaton \
    import get_example0, get_dfa_example, perform_tests_example0


class TestRegex:
    """ Tests for regex """

    # pylint: disable=missing-function-docstring,too-many-public-methods
    # pylint: disable=protected-access

    def test_creation(self):
        """ Try to create regex """
        regex = Regex("a|b")
        assert regex.get_number_symbols() == 2
        assert regex.get_number_operators() == 1
        regex = Regex("a b")
        assert regex.get_number_symbols() == 2
        assert regex.get_number_operators() == 1
        regex = Regex("a b c")
        assert regex.get_number_symbols() == 3
        assert regex.get_number_operators() == 2
        regex = Regex("(a b)|c")
        assert regex.get_number_symbols() == 3
        assert regex.get_number_operators() == 2
        regex = Regex("")
        assert regex.get_number_symbols() == 1
        assert regex.get_number_operators() == 0
        regex = Regex("a*")
        assert regex.get_number_symbols() == 1
        assert regex.get_number_operators() == 1
        regex = Regex("a**")
        assert regex.get_number_symbols() == 1
        assert regex.get_number_operators() == 2
        regex = Regex("a*b|c")
        assert regex.get_number_symbols() == 3
        assert regex.get_number_operators() == 3
        regex = Regex("a*(b|c)")
        assert regex.get_number_symbols() == 3
        assert regex.get_number_operators() == 3
        regex = Regex("a*.(b|c)")
        assert regex.get_number_symbols() == 3
        assert regex.get_number_operators() == 3
        regex = Regex("a*.(b|c)epsilon")
        assert regex.get_number_symbols() == 4
        assert regex.get_number_operators() == 4
        regex = Regex("$")
        assert regex.get_number_symbols() == 1
        regex = Regex("a|")
        assert regex.get_number_symbols() == 2
        assert regex.get_number_operators() == 1
        with pytest.raises(MisformedRegexError):
            Regex(")a b()")
        with pytest.raises(MisformedRegexError):
            Regex("(a b()")
        with pytest.raises(MisformedRegexError):
            Regex("(a b))")
        with pytest.raises(MisformedRegexError):
            Regex("| a b")
        regex = Regex("(a-|a a b)")
        assert regex.get_number_symbols() == 4
        assert regex.get_number_operators() == 3

    def test_to_enfa0(self):
        """ Tests the transformation to a regex """
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        epsilon = Epsilon()
        regex = Regex("a|b")
        enfa = regex.to_epsilon_nfa()
        assert enfa.accepts([symb_a])
        assert enfa.accepts([symb_b])
        assert not enfa.accepts([symb_c])
        assert not enfa.accepts([epsilon])
        assert not enfa.accepts([symb_a, symb_b])
        regex = Regex("a b")
        enfa = regex.to_epsilon_nfa()
        assert not enfa.accepts([symb_a])
        assert not enfa.accepts([symb_b])
        assert enfa.accepts([symb_a, symb_b])
        regex = Regex("a b c")
        enfa = regex.to_epsilon_nfa()
        assert not enfa.accepts([symb_a, symb_b])
        assert enfa.accepts([symb_a, symb_b, symb_c])
        assert not enfa.accepts([symb_a, symb_b, symb_a])
        regex = Regex("(a b)|c")
        enfa = regex.to_epsilon_nfa()
        assert enfa.accepts([symb_a, symb_b])
        assert not enfa.accepts([symb_a, symb_c])
        assert not enfa.accepts([symb_b, symb_c])
        assert enfa.accepts([symb_c])
        regex = Regex("")
        enfa = regex.to_epsilon_nfa()
        assert not enfa.accepts([symb_a])
        assert not enfa.accepts([symb_b])
        assert not enfa.accepts([symb_c])
        assert not enfa.accepts([])
        regex = Regex("a*")
        enfa = regex.to_epsilon_nfa()
        assert enfa.accepts([symb_a])
        assert enfa.accepts([])
        assert enfa.accepts([symb_a, symb_a])
        assert enfa.accepts([symb_a, symb_a, symb_a])

    def test_to_enfa1(self):
        """ Tests the transformation to a regex """
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        regex = Regex("a**")
        enfa = regex.to_epsilon_nfa()
        assert enfa.accepts([symb_a])
        assert enfa.accepts([])
        assert enfa.accepts([symb_a, symb_a])
        assert enfa.accepts([symb_a, symb_a, symb_a])
        regex = Regex("a*b|c")
        enfa = regex.to_epsilon_nfa()
        assert enfa.accepts([symb_a, symb_a, symb_b])
        assert enfa.accepts([symb_b])
        assert enfa.accepts([symb_c])
        assert not enfa.accepts([symb_a, symb_a, symb_c])
        regex = Regex("a*(b|c)")
        enfa = regex.to_epsilon_nfa()
        assert enfa.accepts([symb_a, symb_a, symb_b])
        assert enfa.accepts([symb_b])
        assert enfa.accepts([symb_c])
        assert enfa.accepts([symb_a, symb_a, symb_c])
        regex = Regex("a*.(b|c)")
        enfa = regex.to_epsilon_nfa()
        assert enfa.accepts([symb_a, symb_a, symb_b])
        assert enfa.accepts([symb_b])
        assert enfa.accepts([symb_c])
        assert enfa.accepts([symb_a, symb_a, symb_c])
        regex = Regex("a*.(b|c)epsilon")
        enfa = regex.to_epsilon_nfa()
        assert enfa.accepts([symb_a, symb_a, symb_b])
        assert enfa.accepts([symb_b])
        assert enfa.accepts([symb_c])
        assert enfa.accepts([symb_a, symb_a, symb_c])
        regex = Regex("$")
        enfa = regex.to_epsilon_nfa()
        assert not enfa.accepts([symb_a])
        assert not enfa.accepts([symb_b])
        assert not enfa.accepts([symb_c])
        assert enfa.accepts([])

    def test_print(self):
        """ Test printing functions """
        regex = Regex("a*.(b|c)epsilon")
        tree_str = regex.get_tree_str()
        assert "Concatenation" in tree_str
        assert "Union" in tree_str
        assert "Kleene Star" in tree_str
        assert "Symbol" in tree_str
        regex = Regex("")
        tree_str = regex.get_tree_str()
        assert "Empty" in tree_str

    def test_get_repr(self):
        regex0 = Regex("a*.(b|c)epsilon")
        regex_str = str(regex0)
        regex1 = Regex(regex_str)
        dfa0 = regex0.to_minimal_dfa()
        dfa1 = regex1.to_minimal_dfa()
        assert dfa0 == dfa1

    def test_accepts(self):
        regex = Regex("a|b|c")
        assert regex.accepts(["a"])
        assert not regex.accepts(["a", "b"])

    def test_space(self):
        regex = Regex("\\ ")
        assert regex.accepts([" "])

    def test_parenthesis_gorilla(self):
        regex = Regex("george touches (a|an) (sky|gorilla) !")
        assert regex.accepts(["george", "touches", "a", "sky", "!"])

    def test_regex_or(self):
        regex = Regex("a|b")
        assert regex.accepts(["a"])

    def test_regex_or_concat(self):
        regex = Regex("c (a|b)")
        assert regex.accepts(["c", "b"])

    def test_regex_two_or_concat(self):
        regex = Regex("c (a|b) (d|e)")
        assert regex.accepts(["c", "b", "e"])

    def test_regex_two_or_concat_parenthesis(self):
        regex = Regex("c.(a|b)(d|e)")
        assert regex.accepts(["c", "b", "e"])

    def test_regex_two_or_concat_parenthesis2(self):
        regex = Regex("c (a|(b d)|e)")
        assert regex.accepts(["c", "a"])
        assert regex.accepts(["c", "b", "d"])
        assert regex.accepts(["c", "e"])

    def test_regex_two_or_concat_parenthesis2_concat(self):
        regex = Regex("c (a|(b d)|e) !")
        assert regex.accepts(["c", "a", "!"])
        assert regex.accepts(["c", "b", "d", "!"])
        assert regex.accepts(["c", "e", "!"])

    def test_regex_or_two_concat(self):
        regex = Regex("c d (a|b)")
        assert regex.accepts(["c", "d", "b"])

    def test_after_union(self):
        regex = Regex("(a|b) !")
        assert regex.accepts(["a", "!"])

    def test_star_union(self):
        regex = Regex("a*(b|c)")
        assert regex.accepts(["a", "a", "c"])

    def test_misformed(self):
        with pytest.raises(MisformedRegexError):
            Regex(")")

    def test_misformed2(self):
        with pytest.raises(MisformedRegexError):
            Regex("(")

    def test_escaped_parenthesis(self):
        regex = Regex("\\(")
        assert regex.accepts(["("])

    def test_escaped_mid_bar(self):
        regex = Regex('a(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q'
                      '|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|'
                      'S|T|U|V|W|X|Y|Z|!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|'
                      '\\.|/|:|;|<|=|>|?|@|[|\\|]|^|_|`|{|\\||}|~|\\ |	|)')
        assert regex.accepts(["a", "|"])

    def test_to_cfg(self):
        regex = Regex("a")
        cfg = regex.to_cfg()
        assert cfg.contains(["a"])
        regex = Regex("a|b")
        cfg = regex.to_cfg()
        assert cfg.contains(["b"])
        regex = Regex("a b")
        cfg = regex.to_cfg()
        assert cfg.contains(["a", "b"])
        regex = Regex("a*")
        cfg = regex.to_cfg()
        assert cfg.contains([])
        assert cfg.contains(["a"])
        assert cfg.contains(["a", "a"])
        regex = Regex("epsilon")
        cfg = regex.to_cfg()
        assert cfg.contains([])
        regex = Regex("")
        cfg = regex.to_cfg()
        assert cfg.is_empty()
        regex = Regex("(a|b)* c")
        cfg = regex.to_cfg()
        assert cfg.contains(["c"])
        assert cfg.contains(["a", "c"])
        assert cfg.contains(["a", "b", "c"])

    def test_priority(self):
        assert Regex('b a* | a').accepts('a')
        assert Regex('b a* | a').accepts('b')
        assert Regex('(b a*) | a').accepts('a')

    def test_backslash_b(self):
        assert Regex("( a | \b )").accepts("\b")
        assert Regex("( a | \b )").accepts("a")
        assert not Regex("( a | \b )").accepts("b")

    def test_backslash(self):
        assert Regex("(\\\\|])").accepts("\\")
        assert Regex("(\\\\|])").accepts("]")

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
        Regex._remove_all_basic_states(enfa)
        assert enfa.get_number_transitions() == 1
        assert len(enfa.states) == 2

    def test_from_enfa1(self):
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
        regex = Regex.from_finite_automaton(enfa)
        enfa2 = regex.to_epsilon_nfa()
        assert enfa2.accepts([symb_e, symb_f])
        assert enfa2.accepts([symb_g])
        assert not enfa2.accepts([])
        assert not enfa2.accepts([symb_e])
        assert not enfa2.accepts([symb_f])
        enfa.add_final_state(state0)
        with pytest.raises(ValueError) as _:
            Regex._get_regex_simple(enfa)
        regex = Regex.from_finite_automaton(enfa)
        enfa3 = regex.to_epsilon_nfa()
        assert enfa3.accepts([symb_e, symb_f])
        assert enfa3.accepts([symb_g])
        assert enfa3.accepts([])
        assert not enfa3.accepts([symb_e])
        assert not enfa3.accepts([symb_f])
        enfa.remove_start_state(state0)
        regex = Regex.from_finite_automaton(enfa)
        enfa3 = regex.to_epsilon_nfa()
        assert not enfa3.accepts([symb_e, symb_f])
        assert not enfa3.accepts([symb_g])
        assert not enfa3.accepts([])
        assert not enfa3.accepts([symb_e])
        assert not enfa3.accepts([symb_f])
        enfa.add_start_state(state0)
        enfa.add_transition(state0, symb_f, state0)
        regex = Regex.from_finite_automaton(enfa)
        enfa3 = regex.to_epsilon_nfa()
        assert enfa3.accepts([symb_e, symb_f])
        assert enfa3.accepts([symb_f, symb_e, symb_f])
        assert enfa3.accepts([symb_g])
        assert enfa3.accepts([symb_f, symb_f, symb_g])
        assert enfa3.accepts([])
        assert not enfa3.accepts([symb_e])
        assert enfa3.accepts([symb_f])

    def test_from_enfa2(self):
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
        regex = Regex.from_finite_automaton(enfa)
        enfa2 = regex.to_epsilon_nfa()
        assert enfa2.accepts([symb_a])
        assert enfa2.accepts([symb_a, symb_a])
        assert enfa2.accepts([symb_a, symb_a, symb_b])
        assert enfa2.accepts([symb_a, symb_a, symb_b, symb_b])
        assert enfa2.accepts([symb_a, symb_a,
                                       symb_b, symb_b, symb_a])
        assert enfa2.accepts([symb_a, symb_a, symb_b,
                                       symb_b, symb_a, symb_b])
        assert not enfa2.accepts([symb_b])

    def test_from_enfa3(self):
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
        regex = Regex.from_finite_automaton(enfa)
        enfa2 = regex.to_epsilon_nfa()
        assert not enfa2.accepts([symb_a])
        assert not enfa2.accepts([symb_a, symb_a])
        assert not enfa2.accepts([symb_a, symb_a, symb_b])
        assert not enfa2.accepts([symb_a, symb_a,
                                        symb_b, symb_b, symb_a])
        assert not enfa2.accepts([symb_a, symb_a, symb_b,
                                        symb_b, symb_a, symb_b])
        assert not enfa2.accepts([symb_b])
        epsilon = Epsilon()
        enfa.add_transition(state0, epsilon, state1)
        regex = Regex.from_finite_automaton(enfa)
        enfa2 = regex.to_epsilon_nfa()
        assert enfa.accepts([])
        assert enfa.accepts([symb_a])
        assert enfa2.accepts([symb_a])
        assert enfa2.accepts([symb_a, symb_a])
        assert enfa2.accepts([symb_a, symb_a, symb_b, symb_b])
        assert enfa2.accepts([symb_a, symb_a, symb_b, symb_b,
                                       symb_a, symb_b])
        assert enfa2.accepts([symb_b])
        assert enfa2.accepts([])
        enfa.remove_transition(state0, symb_a, state0)
        regex = Regex.from_finite_automaton(enfa)
        enfa2 = regex.to_epsilon_nfa()
        assert not enfa2.accepts([symb_a])
        assert not enfa2.accepts([symb_a, symb_a])
        assert not enfa2.accepts([symb_a, symb_a, symb_b])
        assert not enfa2.accepts([symb_a, symb_a, symb_b,
                                        symb_b, symb_a])
        assert not enfa2.accepts([symb_a, symb_a, symb_b, symb_b,
                                        symb_a, symb_b])
        assert enfa2.accepts([symb_b])
        assert enfa2.accepts([])
        enfa.remove_transition(state1, symb_b, state1)
        regex = Regex.from_finite_automaton(enfa)
        enfa2 = regex.to_epsilon_nfa()
        assert enfa2.accepts([symb_b, symb_b])
        enfa.add_transition(state0, symb_a, state0)
        regex = Regex.from_finite_automaton(enfa)
        enfa2 = regex.to_epsilon_nfa()
        assert enfa2.accepts([symb_a, symb_b])

    def test_example_doc(self):
        enfa0 = EpsilonNFA()
        state0 = State(0)
        state1 = State(1)
        symb_a = Symbol("0")
        symb_b = Symbol("1")
        enfa0.add_start_state(state0)
        enfa0.add_final_state(state1)
        enfa0.add_transition(state0, symb_a, state0)
        enfa0.add_transition(state1, symb_b, state0)
        enfa0.add_transition(state1, symb_b, state1)

        # Turn a finite automaton into a regex...
        regex = Regex.from_finite_automaton(enfa0)
        # And turn it back into an epsilon non deterministic automaton
        enfa1 = regex.to_epsilon_nfa()
        dfa0 = DeterministicFiniteAutomaton.from_epsilon_nfa(enfa0)
        dfa1 = DeterministicFiniteAutomaton.from_epsilon_nfa(enfa1)
        assert dfa0.is_equivalent_to(dfa1)

    def test_from_dfa0(self):
        """ Tests the regex transformation """
        dfa0 = get_example0()
        enfa = Regex.from_finite_automaton(dfa0).to_epsilon_nfa()
        perform_tests_example0(enfa)

    def test_from_dfa1(self):
        dfa1 = get_dfa_example()
        enfa = Regex.from_finite_automaton(dfa1).to_epsilon_nfa()
        dfa2 = DeterministicFiniteAutomaton.from_epsilon_nfa(enfa)
        assert dfa1.is_equivalent_to(dfa2)

    def test_to_minimal_dfa(self):
        dfa0 = get_example0()
        dfa_regex = Regex.from_finite_automaton(dfa0)
        dfa1 = dfa_regex.to_minimal_dfa()
        assert dfa0 == dfa1
