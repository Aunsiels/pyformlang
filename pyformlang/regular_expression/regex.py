"""
Representation of a regular expression
"""

from typing import List, Iterable, Tuple, Optional, Any

from pyformlang.finite_automaton import FiniteAutomaton, EpsilonNFA
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State, Symbol, Epsilon as FAEpsilon
from pyformlang.cfg.cfg import CFG, Production
from pyformlang.cfg.utils import to_variable

from .regex_reader import RegexReader
from .regex_objects import Epsilon as RegexEpsilon, Node, \
    Empty, Concatenation, Union, KleeneStar


class Regex(RegexReader):
    """ Represents a regular expression

    Pyformlang implements the operators of textbooks, which deviate slightly \
    from the operators in Python. For a representation closer to Python one, \
    please use :class:`~pyformlang.regular_expression.PythonRegex`

    * The concatenation can be represented either by a space or a dot (.)
    * The union is represented either by | or +
    * The Kleene star is represented by *
    * The epsilon symbol can either be "epsilon" or $

    It is also possible to use parentheses. All symbols except the space, ., \
 |, +, *, (, ), epsilon and $ can be part of the alphabet. All \
 other common regex operators (such as []) are syntactic sugar that can be \
 reduced to the previous operators. Another main difference is that the \
 alphabet is not reduced to single characters as it is the case in Python. \
 For example, "python" is a single symbol in Pyformlang, whereas it is the \
 concatenation of six symbols in regular Python.

    All special characters except epsilon can be escaped with a backslash (\
    double backslash \\ in strings).

    Parameters
    ----------
    regex : str
        The regex represented as a string

    Raises
    ------
    MisformedRegexError
        If the regular expression is misformed.

    Examples
    --------

    >>> regex = Regex("abc|d")

    Check if the symbol "abc" is accepted

    >>> regex.accepts(["abc"])
    True

    Check if the word composed of the symbols "a", "b" and "c" is accepted

    >>> regex.accepts(["a", "b", "c"])
    False

    Check if the symbol "d" is accepted

    >>> regex.accepts(["d"])  # True

    >>> regex1 = Regex("a b")
    >>> regex_concat = regex.concatenate(regex1)
    >>> regex_concat.accepts(["d", "a", "b"])
    True

    >>> print(regex_concat.get_tree_str())
    Operator(Concatenation)
     Operator(Union)
      Symbol(abc)
      Symbol(d)
     Operator(Concatenation)
      Symbol(a)
      Symbol(b)

    Give the equivalent finite-state automaton

    >>> regex_concat.to_epsilon_nfa()

    """

    def __init__(self, regex: str) -> None:
        super().__init__(regex)
        self.head: Node = Empty() # type: ignore
        self.sons: List[Regex] = [] # type: ignore
        self._counter = 0
        self._enfa: Optional[EpsilonNFA] = None

    def get_number_symbols(self) -> int:
        """ Gives the number of symbols in the regex

        Returns
        ----------
        n_symbols : int
            The number of symbols in the regex

        Examples
        --------

        >>> regex = Regex("a|b*")
        >>> regex.get_number_symbols()
        2

        The two symbols are "a" and "b".
        """
        if self.sons:
            return sum(son.get_number_symbols() for son in self.sons)
        return 1

    def get_number_operators(self) -> int:
        """ Gives the number of operators in the regex

        Returns
        ----------
        n_operators : int
            The number of operators in the regex

        Examples
        --------

        >>> regex = Regex("a|b*")
        >>> regex.get_number_operators()
        2

        The two operators are "|" and "*".

        """
        if self.sons:
            return 1 + sum(son.get_number_operators() for son in self.sons)
        return 0

    def to_minimal_dfa(self) -> "DeterministicFiniteAutomaton":
        """ Builds minimal dfa from current regex """
        enfa = self.to_epsilon_nfa()
        dfa = DeterministicFiniteAutomaton.from_epsilon_nfa(enfa)
        return dfa.minimize()

    def to_epsilon_nfa(self) -> EpsilonNFA:
        """ Transforms the regular expression into an epsilon NFA

        Returns
        ----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            An epsilon NFA equivalent to the regex

        Examples
        --------

        >>> regex = Regex("abc|d")
        >>> regex.to_epsilon_nfa()

        """
        return self._to_epsilon_nfa_internal(True)

    def _to_epsilon_nfa_internal(self, copy: bool) -> EpsilonNFA:
        """
        Transforms the regular expression into an epsilon NFA.
        Copy enfa in case of external usage.
        """
        if self._enfa is not None:
            return self._enfa.copy() if copy else self._enfa
        self._enfa = EpsilonNFA()
        s_initial = self._set_and_get_initial_state_in_enfa(self._enfa)
        s_final = self._set_and_get_final_state_in_enfa(self._enfa)
        self._process_to_enfa(self._enfa, s_initial, s_final)
        return self._to_epsilon_nfa_internal(copy)

    def _set_and_get_final_state_in_enfa(self, enfa: EpsilonNFA) -> State:
        s_final = self._get_next_state_enfa()
        enfa.add_final_state(s_final)
        return s_final

    def _set_and_get_initial_state_in_enfa(self, enfa: EpsilonNFA) -> State:
        s_initial = self._get_next_state_enfa()
        enfa.add_start_state(s_initial)
        return s_initial

    def _process_to_enfa(self,
                         enfa: EpsilonNFA,
                         s_from: State,
                         s_to: State) -> None:
        """ Internal function to add a regex to a given epsilon NFA

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        s_to : :class:`~pyformlang.finite_automaton.State`
            The destination state
        """
        if self.sons:
            self._process_to_enfa_when_sons(enfa, s_from, s_to)
        else:
            self._process_to_enfa_when_no_son(enfa, s_from, s_to)

    def _process_to_enfa_when_sons(self,
                                   enfa: EpsilonNFA,
                                   s_from: State,
                                   s_to: State) -> None:
        if isinstance(self.head, Concatenation):
            self._process_to_enfa_concatenation(enfa, s_from, s_to)
        elif isinstance(self.head, Union):
            self._process_to_enfa_union(enfa, s_from, s_to)
        elif isinstance(self.head, KleeneStar):
            self._process_to_enfa_kleene_star(enfa, s_from, s_to)

    def _process_to_enfa_when_no_son(self,
                                     enfa: EpsilonNFA,
                                     s_from: State,
                                     s_to: State) -> None:
        if isinstance(self.head, RegexEpsilon):
            enfa.add_transition(s_from, FAEpsilon(), s_to)
        elif not isinstance(self.head, Empty):
            symbol = Symbol(self.head.value)
            enfa.add_transition(s_from, symbol, s_to)

    def _process_to_enfa_union(self,
                               enfa: EpsilonNFA,
                               s_from: State,
                               s_to: State) -> None:
        son_number = 0
        self._create_union_branch_in_enfa(enfa, s_from, s_to, son_number)
        son_number = 1
        self._create_union_branch_in_enfa(enfa, s_from, s_to, son_number)

    def _process_to_enfa_kleene_star(self,
                                     enfa: EpsilonNFA,
                                     s_from: State,
                                     s_to: State) -> None:
        # pylint: disable=protected-access
        state_first = self._get_next_state_enfa()
        state_second = self._get_next_state_enfa()
        enfa.add_transition(state_second, FAEpsilon(), state_first)
        enfa.add_transition(s_from, FAEpsilon(), s_to)
        enfa.add_transition(s_from, FAEpsilon(), state_first)
        enfa.add_transition(state_second, FAEpsilon(), s_to)
        self._process_to_enfa_son(enfa, state_first, state_second, 0)

    def _create_union_branch_in_enfa(self,
                                     enfa: EpsilonNFA,
                                     s_from: State,
                                     s_to: State,
                                     son_number: int) -> None:
        state0 = self._get_next_state_enfa()
        state2 = self._get_next_state_enfa()
        enfa.add_transition(s_from, FAEpsilon(), state0)
        enfa.add_transition(state2, FAEpsilon(), s_to)
        self._process_to_enfa_son(enfa, state0, state2, son_number)

    def _process_to_enfa_concatenation(self,
                                       enfa: EpsilonNFA,
                                       s_from: State,
                                       s_to: State) -> None:
        state0 = self._get_next_state_enfa()
        state1 = self._get_next_state_enfa()
        enfa.add_transition(state0, FAEpsilon(), state1)
        self._process_to_enfa_son(enfa, s_from, state0, 0)
        self._process_to_enfa_son(enfa, state1, s_to, 1)

    def _process_to_enfa_son(self,
                             enfa: EpsilonNFA,
                             s_from: State,
                             s_to: State,
                             index_son: int) -> None:
        # pylint: disable=protected-access
        self.sons[index_son]._counter = self._counter
        self.sons[index_son]._enfa = enfa
        self.sons[index_son]._process_to_enfa(enfa, s_from, s_to)
        self._counter = self.sons[index_son]._counter

    def _get_next_state_enfa(self) -> State:
        s_final = State(self._counter)
        self._counter += 1
        return s_final

    def get_tree_str(self, depth: int = 0) -> str:
        """ Get a string representation of the tree behind the regex

        Parameters
        ----------
        depth: int
            The current depth, 0 by default
        Returns
        -------
        representation: str
            The tree representation

        Examples
        --------

        >>> regex = Regex("abc|d*")
        >>> print(regex.get_tree_str())
        Operator(Union)
         Symbol(abc)
         Operator(Kleene Star)
          Symbol(d)

        """
        temp = " " * depth + str(self.head) + "\n"
        for son in self.sons:
            temp += son.get_tree_str(depth + 1)
        return temp

    def to_cfg(self, starting_symbol: str = "S") -> CFG:
        """
        Turns the regex into a context-free grammar

        Parameters
        ----------
        starting_symbol : :class:`~pyformlang.cfg.Variable`, optional
            The starting symbol

        Returns
        -------
        cfg : :class:`~pyformlang.cfg.CFG`
            An equivalent context-free grammar

        Examples
        --------

        >>> regex = Regex("(a|b)* c")
        >>> my_cfg = regex.to_cfg()
        >>> my_cfg.contains(["c"])
        True

        """
        productions, _ = self._get_production(starting_symbol)
        cfg_res = CFG(start_symbol=to_variable(starting_symbol),
                          productions=set(productions))
        return cfg_res

    def _get_production(self, current_symbol: Any, count: int = 0) \
            -> Tuple[List[Production], int]:
        next_symbols = []
        next_productions = []
        for son in self.sons:
            next_symbol = "A" + str(count)
            count += 1
            # pylint: disable=protected-access
            new_prods, count = son._get_production(next_symbol, count)
            next_symbols.append(next_symbol)
            next_productions += new_prods
        new_prods = self.head.get_cfg_rules(current_symbol, next_symbols)
        next_productions += new_prods
        return next_productions, count

    def __repr__(self) -> str:
        return self.head.get_str_repr([str(son) for son in self.sons])

    def union(self, other: "Regex") -> "Regex":
        """ Makes the union with another regex

        Equivalent to:
          >>> regex0 or regex1

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The union of the two regex

        Examples
        --------

        >>> regex0 = Regex("a b")
        >>> regex1 = Regex("c")
        >>> regex_union = regex0.union(regex1)
        >>> regex_union.accepts(["a", "b"])
        >>> regex_union.accepts(["c"])

        Or equivalently:

        >>> regex_union = regex0 or regex1
        >>> regex_union.accepts(["a", "b"])

        """
        regex = Regex("")
        regex.head = Union()
        regex.sons = [self, other]
        return regex

    def __or__(self, other: "Regex") -> "Regex":
        """ Makes the union with another regex

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The union of the two regex

        Examples
        --------

        >>> regex0 = Regex("a b")
        >>> regex1 = Regex("c")
        >>> regex_union = regex0.union(regex1)
        >>> regex_union.accepts(["a", "b"])
        True
        >>> regex_union.accepts(["c"])
        True

        Or equivalently:

        >>> regex_union = regex0 or regex1
        >>> regex_union.accepts(["a", "b"])
        True
        """
        return self.union(other)

    def concatenate(self, other: "Regex") -> "Regex":
        """ Concatenates a regular expression with an other one

        Equivalent to:
          >>> regex0 + regex1

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The concatenation of the two regex

        Examples
        --------

        >>> regex0 = Regex("a b")
        >>> regex1 = Regex("c")
        >>> regex_union = regex0.concatenate(regex1)
        >>> regex_union.accepts(["a", "b"])
        False
        >>> regex_union.accepts(["a", "b", "c"])
        True

        Or equivalently:

        >>> regex_union = regex0 + regex1
        >>> regex_union.accepts(["a", "b", "c"])
        True
        """
        regex = Regex("")
        regex.head = Concatenation()
        regex.sons = [self, other]
        return regex

    def __add__(self, other: "Regex") -> "Regex":
        """ Concatenates a regular expression with an other one

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The concatenation of the two regex

        Examples
        --------

        >>> regex0 = Regex("a b")
        >>> regex1 = Regex("c")
        >>> regex_union = regex0.concatenate(regex1)
        >>> regex_union.accepts(["a", "b"])
        False
        >>> regex_union.accepts(["a", "b", "c"])
        True

        Or equivalently:

        >>> regex_union = regex0 + regex1
        >>> regex_union.accepts(["a", "b", "c"])
        True

        """
        return self.concatenate(other)

    def kleene_star(self) -> "Regex":
        """ Makes the kleene star of the current regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The kleene star of the current regex

        Examples
        --------

        >>> regex = Regex("a")
        >>> regex_kleene = regex.kleene_star()
        >>> regex_kleene.accepts([])
        True
        >>> regex_kleene.accepts(["a", "a", "a"])
        True

        """
        regex = Regex("")
        regex.head = KleeneStar()
        regex.sons = [self]
        return regex

    def from_string(self, regex_str: str) -> "Regex":
        """ Construct a regex from a string. For internal usage.

        Equivalent to the constructor of Regex

        Parameters
        ----------
        regex_str : str
            The string representation of the regex

        Returns
        -------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The regex

        Examples
        --------
        >>> Regex.from_string("a b c")

        , which is equivalent to:

        >>> Regex("a b c")

        """
        return Regex(regex_str)

    def accepts(self, word: Iterable[str]) -> bool:
        """
        Check if a word matches (completely) the regex

        Parameters
        ----------
        word : iterable of str
            The word to check

        Returns
        -------
        is_accepted : bool
            Whether the word is recognized or not

        Examples
        --------

        >>> regex = Regex("abc|d")

        Check if the symbol "abc" is accepted

        >>> regex.accepts(["abc"])
        True

        """
        self._enfa = self._to_epsilon_nfa_internal(False)
        return self._enfa.accepts(word)

    @classmethod
    def from_finite_automaton(cls, automaton: FiniteAutomaton) -> "Regex":
        """ Creates a regular expression from given finite automaton

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            A regular expression equivalent to the current Epsilon NFA

        Examples
        --------

        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> regex = enfa.to_regex()
        >>> regex.accepts(["abc"])
        True

        """
        copies = [automaton.copy() for _ in automaton.final_states]
        final_states = list(automaton.final_states)
        for i in range(len(automaton.final_states)):
            for j in range(len(automaton.final_states)):
                if i != j:
                    copies[j].remove_final_state(final_states[i])
        regex_l = []
        for copy in copies:
            cls._remove_all_basic_states(copy)
            regex_sub = cls._get_regex_simple(copy)
            if regex_sub:
                regex_l.append(regex_sub)
        res = "+".join(regex_l)
        return Regex(res)

    @classmethod
    def _get_regex_simple(cls, automaton: FiniteAutomaton) -> str:
        """ Get the regex of an automaton when it only composed of a start and
        a final state

        CAUTION: For internal use only!

        Returns
        ----------
        regex : str
            A regex representing the automaton
        """
        if not automaton.final_states or not automaton.start_states:
            return ""
        if len(automaton.final_states) != 1 or len(automaton.start_states) != 1:
            raise ValueError("The automaton is not simple enough!")
        if automaton.start_states == automaton.final_states:
            # We are suppose to have only one good symbol
            for symbol in automaton.symbols:
                out_states = automaton(list(automaton.start_states)[0], symbol)
                if out_states:
                    return "(" + str(symbol.value) + ")*"
            return "epsilon"
        start_to_start, start_to_end, end_to_start, end_to_end = \
            cls._get_bi_transitions(automaton)
        return cls.__get_regex_sub(start_to_start,
                                    start_to_end,
                                    end_to_start,
                                    end_to_end)

    @classmethod
    def _get_bi_transitions(cls, automaton: FiniteAutomaton) \
            -> Tuple[str, str, str, str]:
        """ Internal method to compute the transition in the case of a \
        simple automaton

        Returns
        start_to_start : str
            The transition from the start state to the start state
        start_to_end : str
            The transition from the start state to the end state
        end_to_start : str
            The transition from the end state to the start state
        end_to_end : str
            The transition from the end state to the end state
        ----------
        """
        start = list(automaton.start_states)[0]
        end = list(automaton.final_states)[0]
        start_to_start = "epsilon"
        start_to_end = ""
        end_to_end = "epsilon"
        end_to_start = ""
        for state in automaton.states:
            for symbol in automaton.symbols.union({FAEpsilon()}):
                for out_state in automaton(state, symbol):
                    symbol_str = str(symbol.value)
                    if not symbol_str.isalnum():
                        symbol_str = "(" + symbol_str + ")"
                    if state == start and out_state == start:
                        start_to_start = symbol_str
                    elif state == start and out_state == end:
                        start_to_end = symbol_str
                    elif state == end and out_state == start:
                        end_to_start = symbol_str
                    elif state == end and out_state == end:
                        end_to_end = symbol_str
        return start_to_start, start_to_end, end_to_start, end_to_end

    @classmethod
    def _remove_all_basic_states(cls, automaton: FiniteAutomaton) -> None:
        """ Remove all states which are not the start state or a final state

        CAREFUL: This method modifies the current automaton, for internal usage
        only!

        The function _create_or_transitions is supposed to be called before
        calling this function
        """
        cls._create_or_transitions(automaton)
        states = automaton.states.copy()
        for state in states:
            if (state not in automaton.start_states \
                    and state not in automaton.final_states):
                cls._remove_state(automaton, state)

    @classmethod
    def _remove_state(cls, automaton: FiniteAutomaton, state: State) -> None:
        """ Removes a given state from the epsilon NFA

        CAREFUL: This method modifies the current automaton, for internal usage
        only!

        The function _create_or_transitions is supposed to be called before
        calling this function

        Parameters
        ----------
        state : :class:`~pyformlang.finite_automaton.State`
            The state to remove

        """
        # First compute all endings
        out_transitions = {}
        input_symbols = automaton.symbols.union({FAEpsilon()})
        for symbol in input_symbols:
            out_states = automaton(state, symbol).copy()
            for out_state in out_states:
                out_transitions[out_state] = str(symbol.value)
                automaton.remove_transition(state, symbol, out_state)
        if state in out_transitions:
            to_itself = "(" + out_transitions[state] + ")*"
            del out_transitions[state]
            for out_state in list(out_transitions.keys()):
                out_transitions[out_state] = to_itself + "." + \
                                             out_transitions[out_state]
        for in_state in automaton.states:
            if in_state == state:
                continue
            for symbol in input_symbols:
                out_states = automaton(in_state, symbol)
                if state not in out_states:
                    continue
                symbol_str = "(" + str(symbol.value) + ")"
                automaton.remove_transition(in_state, symbol, state)
                for out_state, next_symb in out_transitions.items():
                    new_symbol = Symbol(symbol_str + "." + next_symb)
                    automaton.add_transition(in_state, new_symbol, out_state)
        automaton.states.remove(state)
        # We make sure the automaton has the good structure
        cls._create_or_transitions(automaton)

    @classmethod
    def _create_or_transitions(cls, automaton: FiniteAutomaton) -> None:
        """ Creates a OR transition instead of several connections

        CAREFUL: This method modifies the automaton and is designed for \
        internal use only!
        """
        for state in automaton.states:
            new_transitions = {}
            input_symbols = automaton.symbols.union({FAEpsilon()})
            for symbol in input_symbols:
                out_states = automaton(state, symbol)
                out_states = out_states.copy()
                symbol_str = str(symbol.value)
                for out_state in out_states:
                    automaton.remove_transition(state, symbol, out_state)
                    base = new_transitions.setdefault(out_state, "")
                    if "+" in symbol_str:
                        symbol_str = "(" + symbol_str + ")"
                    if base:
                        new_transitions[out_state] = "((" + base + ")+(" + \
                                                     symbol_str + "))"
                    else:
                        new_transitions[out_state] = symbol_str
            for out_state, next_symb in new_transitions.items():
                automaton.add_transition(state,
                                         next_symb,
                                         out_state)

    @classmethod
    def __get_regex_sub(cls,
                        start_to_start: str,
                        start_to_end: str,
                        end_to_start: str,
                        end_to_end: str) -> str:
        """ Combines the transitions in the regex simple function """
        if not start_to_end:
            return ""
        temp, part1 = cls.__get_temp(start_to_end, end_to_start, end_to_end)
        part0 = "epsilon"
        if start_to_start != "epsilon":
            if temp:
                part0 = "(" + start_to_start + "+" + temp + ")*"
            else:
                part0 = "(" + start_to_start + ")*"
        elif temp != "epsilon" and temp:
            part0 = "(" + temp + ")*"
        return "(" + part0 + "." + part1 + ")"

    @classmethod
    def __get_temp(cls,
                   start_to_end: str,
                   end_to_start: str,
                   end_to_end: str) -> Tuple[str, str]:
        """
        Gets a temp values in the computation
        of the simple automaton regex.
        """
        temp = "epsilon"
        if (start_to_end != "epsilon"
                or end_to_end != "epsilon"
                or end_to_start != "epsilon"):
            temp = ""
        if start_to_end != "epsilon":
            temp = start_to_end
        if end_to_end != "epsilon":
            if temp:
                temp += "." + end_to_end + "*"
            else:
                temp = end_to_end + "*"
        part1 = temp
        if not part1:
            part1 = "epsilon"
        if end_to_start != "epsilon":
            if temp:
                temp += "." + end_to_start
            else:
                temp = end_to_start
        if not end_to_start:
            temp = ""
        return temp, part1
