"""
Representation of a regular expression
"""
from typing import Iterable

from pyformlang import finite_automaton
# pylint: disable=cyclic-import
import pyformlang.regular_expression.regex_objects
from pyformlang.finite_automaton import State
# pylint: disable=cyclic-import
from pyformlang.regular_expression.regex_reader import RegexReader
from pyformlang import regular_expression


class Regex(RegexReader):
    """ Represents a regular expression

    Special Operators: |, +, *, ., $, epsilon
    All except epsilon can be escaped with a backslash (\\ in strings).

    Parameters
    ----------
    regex : str
        The regex represented as a string
    """

    def __init__(self, regex):
        self.head = None
        self.sons = None
        super().__init__(regex)
        self._counter = 0
        self._initialize_enfa()
        self._enfa = None

    def _initialize_enfa(self):
        self._enfa = finite_automaton.EpsilonNFA()

    def get_number_symbols(self) -> int:
        """ Gives the number of symbols in the regex

        Returns
        ----------
        n_symbols : int
            The number of symbols in the regex
        """
        if self.sons:
            return sum([son.get_number_symbols() for son in self.sons])
        return 1

    def get_number_operators(self) -> int:
        """ Gives the number of operators in the regex

        Returns
        ----------
        n_operators : int
            The number of operators in the regex
        """
        if self.sons:
            return 1 + sum([son.get_number_operators() for son in self.sons])
        return 0

    def to_epsilon_nfa(self):
        """ Transforms the regular expression into an epsilon NFA

        Returns
        ----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            An epsilon NFA equivalent to the regex
        """
        self._initialize_enfa()
        s_initial = self._set_and_get_initial_state_in_enfa()
        s_final = self._set_and_get_final_state_in_enfa()
        self._process_to_enfa(s_initial, s_final)
        return self._enfa

    def _set_and_get_final_state_in_enfa(self):
        s_final = self._get_next_state_enfa()
        self._enfa.add_final_state(s_final)
        return s_final

    def _get_next_state_enfa(self):
        s_final = finite_automaton.State(self._counter)
        self._counter += 1
        return s_final

    def _set_and_get_initial_state_in_enfa(self):
        s_initial = self._get_next_state_enfa()
        self._enfa.add_start_state(s_initial)
        return s_initial

    def _process_to_enfa(self, s_from: State, s_to: State):
        """ Internal function to add a regex to a given epsilon NFA

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        s_to : :class:`~pyformlang.finite_automaton.State`
            The destination state
        """
        if self.sons:
            self._process_to_enfa_when_sons(s_from, s_to)
        else:
            self._process_to_enfa_when_no_son(s_from, s_to)

    def _process_to_enfa_when_no_son(self, s_from, s_to):
        if isinstance(self.head,
                      pyformlang.regular_expression.regex_objects.Epsilon):
            self._add_epsilon_transition_in_enfa_between(s_from, s_to)
        elif not isinstance(self.head,
                            pyformlang.regular_expression.regex_objects.Empty):
            symbol = finite_automaton.Symbol(self.head.value)
            self._enfa.add_transition(s_from, symbol, s_to)

    def _process_to_enfa_when_sons(self, s_from, s_to):
        if isinstance(
                self.head,
                pyformlang.regular_expression.regex_objects.Concatenation):
            self._process_to_enfa_concatenation(s_from, s_to)
        elif isinstance(self.head,
                        pyformlang.regular_expression.regex_objects.Union):
            self._process_to_enfa_union(s_from, s_to)
        elif isinstance(
                self.head,
                pyformlang.regular_expression.regex_objects.KleeneStar):
            self._process_to_enfa_kleene_star(s_from, s_to)

    def _process_to_enfa_kleene_star(self, s_from, s_to):
        # pylint: disable=protected-access
        state_first = self._get_next_state_enfa()
        state_second = self._get_next_state_enfa()
        self._add_epsilon_transition_in_enfa_between(state_second, state_first)
        self._add_epsilon_transition_in_enfa_between(s_from, s_to)
        self._add_epsilon_transition_in_enfa_between(s_from, state_first)
        self._add_epsilon_transition_in_enfa_between(state_second, s_to)
        self._process_to_enfa_son(state_first, state_second, 0)

    def _process_to_enfa_union(self, s_from, s_to):
        son_number = 0
        self._create_union_branch_in_enfa(s_from, s_to, son_number)
        son_number = 1
        self._create_union_branch_in_enfa(s_from, s_to, son_number)

    def _create_union_branch_in_enfa(self, s_from, s_to, son_number):
        state0 = self._get_next_state_enfa()
        state2 = self._get_next_state_enfa()
        self._add_epsilon_transition_in_enfa_between(s_from, state0)
        self._add_epsilon_transition_in_enfa_between(state2, s_to)
        self._process_to_enfa_son(state0, state2, son_number)

    def _process_to_enfa_concatenation(self, s_from, s_to):
        state0 = self._get_next_state_enfa()
        state1 = self._get_next_state_enfa()
        self._add_epsilon_transition_in_enfa_between(state0, state1)
        self._process_to_enfa_son(s_from, state0, 0)
        self._process_to_enfa_son(state1, s_to, 1)

    def _add_epsilon_transition_in_enfa_between(self, state0, state1):
        self._enfa.add_transition(state0, finite_automaton.Epsilon(), state1)

    def _process_to_enfa_son(self, s_from, s_to, index_son):
        # pylint: disable=protected-access
        self.sons[index_son]._counter = self._counter
        self.sons[index_son]._enfa = self._enfa
        self.sons[index_son]._process_to_enfa(s_from, s_to)
        self._counter = self.sons[index_son]._counter

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
        """
        temp = " " * depth + str(self.head) + "\n"
        for son in self.sons:
            temp += son.get_tree_str(depth + 1)
        return temp

    def __repr__(self):
        return self.head.get_str_repr([str(son) for son in self.sons])

    def union(self, other: "Regex") -> "Regex":
        """ Makes the union with another regex

        Equivalent to:
          >> regex0 or regex1

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The union of the two regex
        """
        regex = Regex("")
        regex.head = pyformlang.regular_expression.regex_objects.Union()
        regex.sons = [self, other]
        return regex

    def __or__(self, other):
        """ Makes the union with another regex

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The union of the two regex
        """
        return self.union(other)

    def concatenate(self, other: "Regex") -> "Regex":
        """ Concatenates a regular expression with an other one

        Equivalent to:
          >> regex0 + regex1

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The concatenation of the two regex
        """
        regex = Regex("")
        regex.head = \
            pyformlang.regular_expression.regex_objects.Concatenation()
        regex.sons = [self, other]
        return regex

    def __add__(self, other):
        """ Concatenates a regular expression with an other one

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The concatenation of the two regex
        """
        return self.concatenate(other)

    def kleene_star(self) -> "Regex":
        """ Makes the kleene star of the current regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The kleene star of the current regex
        """
        regex = Regex("")
        regex.head = pyformlang.regular_expression.regex_objects.KleeneStar()
        regex.sons = [self]
        return regex

    def from_string(self, regex):
        return Regex(regex)

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

        """
        if self._enfa is None:
            self._enfa = self.to_epsilon_nfa()
        return self._enfa.accepts(word)

    @classmethod
    def from_python_regex(cls, regex):
        """
        Creates a regex from a string using the python way to write it.

        Careful: Not everything is implemented, check PythonRegex class
        documentation for more details.

        Parameters
        ----------
        regex : str
            The regex given as a string or compile regex

        Returns
        -------
        python_regex : :class:`~pyformlang.regular_expression.PythonRegex`

        """
        return regular_expression.PythonRegex(regex)
