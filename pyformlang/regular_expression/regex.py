"""
Representation of a regular expression
"""

from typing import Iterable
import re

from pyformlang import finite_automaton


class Regex(object):
    """ Represents a regular expression

    Parameters
    ----------
    regex : str
        The regex represented as a string

    Attributes
    ----------
    head : Node
        In the tree representation of the regex, represents a node
    sons : list of Node
        In the tree representation of the regex, represents the sons
    """

    def __init__(self, regex: str):
        regex = preprocess_regex(regex)
        self._regex = regex
        regex_l = regex.split(" ")
        regex_l = remove_extreme_parenthesis(regex_l)
        regex_l = compute_precedence(regex_l)
        regex_l = remove_extreme_parenthesis(regex_l)
        self.sons = []
        if not regex:
            self.head = to_node("")
        elif len(regex_l) == 1:
            first = to_node(regex_l[0])
            if not isinstance(first, Symbol):
                raise MisformedRegexError("The regex is misformed here.", regex)
            self.head = first
        else:
            end_first_group = get_end_first_group(regex_l)
            next_node = to_node(regex_l[end_first_group])
            if isinstance(next_node, KleeneStar):
                self.head = next_node
                self.sons.append(Regex(" ".join(regex_l[:end_first_group])))
            else:
                begin_second_group = end_first_group
                if isinstance(next_node, Symbol):
                    self.head = Concatenation()
                else:
                    self.head = next_node
                    begin_second_group += 1
                self.sons.append(Regex(" ".join(regex_l[:end_first_group])))
                self.sons.append(Regex(" ".join(regex_l[begin_second_group:])))

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
        enfa = finite_automaton.EpsilonNFA()
        counter = 0
        s_initial = finite_automaton.State(counter)
        counter += 1
        s_final = finite_automaton.State(counter)
        counter += 1
        enfa.add_start_state(s_initial)
        enfa.add_final_state(s_final)
        self.process_to_enfa(enfa, s_initial, s_final, counter)
        return enfa

    def process_to_enfa(self, enfa: "EpsilonNFA",
                        s_from: "State",
                        s_to: "State",
                        counter: int) -> int:
        """ Internal function to add a regex to a given epsilon NFA

        Parameters
        ----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The Epsilon NFA to which we add the regex
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        s_to : :class:`~pyformlang.finite_automaton.State`
            The destination state
        counter : int
            Prevents duplicate states
        """
        if self.sons:
            state0 = finite_automaton.State(counter)
            counter += 1
            state1 = finite_automaton.State(counter)
            counter += 1
            if isinstance(self.head, Concatenation):
                enfa.add_transition(state0, finite_automaton.Epsilon(), state1)
                counter = self.sons[0].process_to_enfa(enfa, s_from, state0, counter)
                counter = self.sons[1].process_to_enfa(enfa, state1, s_to, counter)
            elif isinstance(self.head, Union):
                state2 = finite_automaton.State(counter)
                counter += 1
                state3 = finite_automaton.State(counter)
                counter += 1
                enfa.add_transition(s_from, finite_automaton.Epsilon(), state0)
                enfa.add_transition(s_from, finite_automaton.Epsilon(), state1)
                enfa.add_transition(state2, finite_automaton.Epsilon(), s_to)
                enfa.add_transition(state3, finite_automaton.Epsilon(), s_to)
                counter = self.sons[0].process_to_enfa(enfa, state0, state2, counter)
                counter = self.sons[1].process_to_enfa(enfa, state1, state3, counter)
            elif isinstance(self.head, KleeneStar):
                enfa.add_transition(state1, finite_automaton.Epsilon(), state0)
                enfa.add_transition(s_from, finite_automaton.Epsilon(), s_to)
                enfa.add_transition(s_from, finite_automaton.Epsilon(), state0)
                enfa.add_transition(state1, finite_automaton.Epsilon(), s_to)
                counter = self.sons[0].process_to_enfa(enfa, state0, state1, counter)
        else:
            if isinstance(self.head, Epsilon):
                enfa.add_transition(s_from, finite_automaton.Epsilon(), s_to)
            elif not isinstance(self.head, Empty):
                symb = finite_automaton.Symbol(self.head.get_value())
                enfa.add_transition(s_from, symb, s_to)
        return counter

    def get_tree_str(self, depth: int = 0) -> str:
        """ Print the regex as a tree """
        temp = " " * depth + str(self.head) + "\n"
        for son in self.sons:
            temp += son.get_tree_str(depth + 1)
        return temp

    def union(self, other: "Regex") -> "Regex":
        """ Makes the union with another regex

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The union of the two regexes
        """
        regex = Regex("")
        regex.head = Union()
        regex.sons = [self, other]
        return regex

    def concatenate(self, other: "Regex") -> "Regex":
        """ Concatenates a regular expression with an other one

        Parameters
        ----------
        other : :class:`~pyformlang.regular_expression.Regex`
            The other regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The concatenation of the two regexes
        """
        regex = Regex("")
        regex.head = Concatenation()
        regex.sons = [self, other]
        return regex

    def kleene_star(self) -> "Regex":
        """ Makes the kleene star of the current regex

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            The kleene star of the current regex
        """
        regex = Regex("")
        regex.head = KleeneStar()
        regex.sons = [self]
        return regex


class Node(object): # pylint: disable=too-few-public-methods
    """ Represents a node in the tree representation of a regex

    Parameters
    ----------
    value : str
        The value of the node
    """

    def __init__(self, value):
        self._value = value

    def get_value(self):
        """ Give the value of the node

        Returns
        ----------
        value : str
            The value of the node
        """
        return self._value


CONCATENATION_SYMBOLS = ["."]
UNION_SYMBOLS = ["|", "+"]
KLEENE_STAR_SYMBOLS = ["*"]
EPSILON_SYMBOLS = ["epsilon", "$"]


def to_node(value: str) -> Node:
    """ Transforms a given value into a node """
    if not value:
        return Empty()
    if value in CONCATENATION_SYMBOLS:
        return Concatenation()
    if value in UNION_SYMBOLS:
        return Union()
    if value in KLEENE_STAR_SYMBOLS:
        return KleeneStar()
    if value in EPSILON_SYMBOLS:
        return Epsilon()
    return Symbol(value)


def remove_extreme_parenthesis(value_l: Iterable[str]) -> Iterable[str]:
    """ Remove useless extreme parenthesis """
    if value_l[0] != "(":
        return value_l
    counter = 0
    pos = 0
    for value in value_l:
        if value == "(":
            counter += 1
        elif value == ")":
            counter -= 1
        if counter == 0 and pos == len(value_l) - 1:
            return remove_extreme_parenthesis(value_l[1:-1])
        elif counter == 0:
            break
        pos += 1
    return value_l


def get_end_first_group(value_l: Iterable[str]) -> int:
    """ Gives the end of the first group """
    if not value_l:
        return 0
    if value_l[0] == ")":
        raise MisformedRegexError("Wrong parenthesis regex", " ".join(value_l))
    if value_l[0] == "(":
        counter = 1
        for i in range(1, len(value_l)):
            if value_l[i] == "(":
                counter += 1
            elif value_l[i] == ")":
                counter -= 1
            if counter == 0:
                return i + 1
        raise MisformedRegexError("Wrong parenthesis regex", " ".join(value_l))
    else:
        return 1


def compute_precedence(value_l: Iterable[str]) -> Iterable[str]:
    """ Add parenthesis for the first group in indicate precedence """
    if len(value_l) <= 1:
        return value_l
    end_group = get_end_first_group(value_l)
    if end_group == len(value_l):
        return value_l
    next_node = to_node(value_l[end_group])
    if isinstance(next_node, KleeneStar):
        return compute_precedence(["("] + value_l[:end_group+1] + [")"] + value_l[end_group+1:])
    elif isinstance(next_node, Union):
        return value_l
    else:
        # Try to see if there is a union somewhere
        while end_group < len(value_l) and not isinstance(next_node, Union):
            if isinstance(next_node, Operator):
                end_group += 1
            end_group += get_end_first_group(value_l[end_group:])
            if end_group < len(value_l):
                next_node = to_node(value_l[end_group])
        if isinstance(next_node, Union):
            return ["("] + value_l[:end_group] + [")"] + value_l[end_group:]
    return value_l


def preprocess_regex(regex: str) -> str:
    """ Preprocess a regex represented as a string

    Parameters
    ----------
    regex : str
        The regex represented as a string

    Returns
    ----------
    regex_prepro : str
        The preprocessed regex
    """
    regex = re.sub(r"\s+", " ", regex.strip())
    res = []
    pos = 0
    for current_c in regex:
        if not current_c.isalnum() and current_c != " " and \
                pos != 0 and res[-1] != " ":
            res.append(" ")
        res.append(current_c)
        if not current_c.isalnum() and current_c != " " and \
                pos != len(regex) - 1 and regex[pos+1] != " ":
            res.append(" ")
        pos += 1
    return "".join(res)


class Operator(Node): # pylint: disable=too-few-public-methods
    """ Represents an operator

    Parameters
    ----------
    value : str
        The value of the operator
    """

    def __repr__(self):
        return "Operator(" + str(self._value) + ")"


class Symbol(Node): # pylint: disable=too-few-public-methods
    """ Represents a symbol

    Parameters
    ----------
    value : str
        The value of the symbol
    """

    def __repr__(self):
        return "Symbol(" + str(self._value) + ")"


class Concatenation(Operator): # pylint: disable=too-few-public-methods
    """ Represents a concatenation
    """

    def __init__(self):
        super().__init__("Concatenation")


class Union(Operator): # pylint: disable=too-few-public-methods
    """ Represents a union
    """

    def __init__(self):
        super().__init__("Union")


class KleeneStar(Operator): # pylint: disable=too-few-public-methods
    """ Represents an epsilon symbol
    """

    def __init__(self):
        super().__init__("Kleene Star")


class Epsilon(Symbol): # pylint: disable=too-few-public-methods
    """ Represents an epsilon symbol
    """

    def __init__(self):
        super().__init__("Epsilon")


class Empty(Symbol): # pylint: disable=too-few-public-methods
    """ Represents an empty symbol
    """

    def __init__(self):
        super().__init__("Empty")


class MisformedRegexError(Exception):
    """ Error for misformed regex """

    def __init__(self, message: str, regex: str):
        super().__init__(message + " Regex: " + regex)
        self._regex = regex
