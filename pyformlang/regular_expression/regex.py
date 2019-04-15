"""
Representation of a regular expression
"""

import re

from pyformlang import finite_automaton


def _find_first_complete_closing_if_possible(parenthesis_depths):
    try:
        first_complete_closing = parenthesis_depths.index(0)
    except ValueError:
        first_complete_closing = -2
    return first_complete_closing


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
        self.components = get_regex_componants(regex)
        self._pre_process_input_regex_componants()
        self._setup_sons()
        self._setup_from_regex_componants()

    def _pre_process_input_regex_componants(self):
        self._remove_useless_extreme_parenthesis_from_components()
        self._compute_precedence()
        self._remove_useless_extreme_parenthesis_from_components()

    def _remove_useless_extreme_parenthesis_from_components(self):
        if self._begins_with_parenthesis_components():
            self._remove_useless_expreme_parenthesis_from_componants_when_starting_with_parenthesis()

    def _remove_useless_expreme_parenthesis_from_componants_when_starting_with_parenthesis(self):
        if self._is_surrounded_by_parenthesis():
            self.components = self.components[1:-1]
            self._remove_useless_extreme_parenthesis_from_components()

    def _is_surrounded_by_parenthesis(self):
        parenthesis_depths = self._get_parenthesis_depths()
        first_complete_closing = _find_first_complete_closing_if_possible(parenthesis_depths)
        return first_complete_closing == len(self.components) - 1

    def _get_parenthesis_depths(self):
        depths = [0]
        for component in self.components:
            depths.append(depths[-1] + self._get_parenthesis_value(component))
        return depths[1:]

    @staticmethod
    def _get_parenthesis_value(component):
        if component == "(":
            return 1
        elif component == ")":
            return -1
        else:
            return 0

    def _begins_with_parenthesis_components(self):
        return self.components[0] == "("

    def _compute_precedence(self):
        """ Add parenthesis for the first group in indicate precedence """
        if len(self.components) <= 1:
            return
        end_group = self._get_end_first_group_in_components()
        if end_group == len(self.components):
            return
        next_node = to_node(self.components[end_group])
        if isinstance(next_node, KleeneStar):
            self._add_parenthesis_around_part_of_componants(0, end_group + 1)
            self._compute_precedence()
        elif not isinstance(next_node, Union):
            while self._found_no_union(end_group, next_node):
                if isinstance(next_node, Operator):
                    end_group += 1
                end_group += self._get_end_first_group_in_components(end_group)
                if end_group < len(self.components):
                    next_node = to_node(self.components[end_group])
            if isinstance(next_node, Union):
                self._add_parenthesis_around_part_of_componants(0, end_group)

    def _found_no_union(self, end_group, next_node):
        return end_group < len(self.components) and not isinstance(next_node, Union)

    def _add_parenthesis_around_part_of_componants(self, index_opening, index_closing):
        self.components.insert(index_opening, "(")
        # Add 1 as something was added before
        self.components.insert(index_closing + 1, ")")

    def _get_end_first_group_in_components(self, idx_from=0) -> int:
        """ Gives the end of the first group """
        if idx_from >= len(self.components):
            return 0
        if self.components[idx_from] == ")":
            raise MisformedRegexError("Wrong parenthesis regex", " ".join(self.components))
        if self.components[idx_from] == "(":
            counter = 1
            for i in range(idx_from + 1, len(self.components)):
                if self.components[i] == "(":
                    counter += 1
                elif self.components[i] == ")":
                    counter -= 1
                if counter == 0:
                    return i + 1
            raise MisformedRegexError("Wrong parenthesis regex", " ".join(self.components))
        else:
            return 1

    def _setup_from_regex_componants(self):
        if not self.components:
            self._setup_empty_regex()
        elif len(self.components) == 1:
            self._setup_one_symbol_regex()
        else:
            self._setup_non_trivial_regex()

    def _setup_non_trivial_regex(self):
        end_first_group = self._get_end_first_group_in_components()
        next_node = to_node(self.components[end_first_group])
        if isinstance(next_node, KleeneStar):
            self.head = next_node
            self.sons.append(process_sub_regex(self.components, 0, end_first_group))
        else:
            begin_second_group = end_first_group
            if isinstance(next_node, Symbol):
                self.head = Concatenation()
            else:
                self.head = next_node
                begin_second_group += 1
            self.sons.append(process_sub_regex(self.components, 0, end_first_group))
            self.sons.append(process_sub_regex(self.components, begin_second_group, len(self.components)))

    def _setup_empty_regex(self):
        self.head = to_node("")

    def _setup_one_symbol_regex(self):
        first_symbol = to_node(self.components[0])
        self._check_is_valid_single_first_symbol(first_symbol)
        self.head = first_symbol

    def _check_is_valid_single_first_symbol(self, first_symbol):
        if not isinstance(first_symbol, Symbol):
            raise MisformedRegexError("The regex is misformed here.", self._regex)

    def _setup_sons(self):
        self.sons = []

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
        if (current_c in CONCATENATION_SYMBOLS \
                or current_c in UNION_SYMBOLS \
                or current_c in KLEENE_STAR_SYMBOLS \
                or current_c in EPSILON_SYMBOLS \
                or current_c in [")", "("]) and \
                pos != 0 and res[-1] != " ":
            res.append(" ")
        res.append(current_c)
        if (current_c in CONCATENATION_SYMBOLS \
                or current_c in UNION_SYMBOLS \
                or current_c in KLEENE_STAR_SYMBOLS \
                or current_c in EPSILON_SYMBOLS \
                or current_c in [")", "("]) and \
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


def get_regex_componants(regex):
    return regex.split(" ")

def process_sub_regex(regex_componants, idx_from, idx_to):
    return Regex(" ".join(regex_componants[idx_from:idx_to]))
