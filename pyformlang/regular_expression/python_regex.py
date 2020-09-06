"""
A class to read Python format regex
"""

import re
import string

# pylint: disable=cyclic-import
from pyformlang.regular_expression import regex, MisformedRegexError
from pyformlang.regular_expression.regex_reader import \
    WRONG_PARENTHESIS_MESSAGE

PRINTABLES = list(string.printable)

TRANSFORMATIONS = {
    "|": "\\|",
    "(": "\\(",
    ")": "\\)",
    "*": "\\*",
    "+": "\\+",
    ".": "\\.",
    "$": "\\$",
    "\n": "",
    " ": "\\ "
}

ESCAPED_PRINTABLES = [TRANSFORMATIONS.get(x, x)
                      for x in PRINTABLES
                      if TRANSFORMATIONS.get(x, x)]

DOT_REPLACEMENT = "(" + "|".join(ESCAPED_PRINTABLES) + ")"

TO_ESCAPE_IN_BRACKETS = "(+*)?"

SHORTCUTS = {
    " ": "\\ ",  # We have to do this due to how Regex separate words
    r"\d": "[0-9]",
    r"\s": "[\\ \t\n\r\f\v]",
    r"\w": "[a-zA-Z0-9_]"
}


class PythonRegex(regex.Regex):
    """ Represents a regular expression as used in Python.

    It adds the following features to the basic regex:

    * Set of characters with [] (no inverse with [^...])
    * positive closure +
    * . for all printable characters
    * ? for optional character/group
    * Shortcuts: \\d, \\s, \\w

    Parameters
    ----------
    python_regex : str
        The regex represented as a string or a compiled regex (
        re.compile(...))

    Raises
    ------
    MisformedRegexError
        If the regular expression is misformed.

    Examples
    --------
    Python regular expressions wrapper

    >>> from pyformlang.regular_expression import PythonRegex

    >>> p_regex = PythonRegex("a+[cd]")
    >>> p_regex.accepts(["a", "a", "d"])
    True

    As the alphabet is composed of single characters, one could also write

    >>> p_regex.accepts("aad")
    True
    >>> p_regex.accepts(["d"])
    False

    """

    def __init__(self, python_regex):
        if not isinstance(python_regex, str):
            python_regex = python_regex.pattern
        else:
            re.compile(python_regex)  # Check if it is valid
        self._python_regex = python_regex
        self._replace_shortcuts()
        self._escape_in_brackets()
        self._preprocess_brackets()
        self._preprocess_positive_closure()
        self._preprocess_optional()
        self._preprocess_dot()
        self._separate()
        super().__init__(self._python_regex)

    def _separate(self):
        regex_temp = []
        for symbol in self._python_regex:
            if self._should_escape_next_symbol(regex_temp):
                regex_temp[-1] += symbol
            else:
                regex_temp.append(symbol)
        self._python_regex = " ".join(regex_temp)

    def _preprocess_brackets(self):
        regex_temp = []
        in_brackets = 0
        in_brackets_temp = []
        for symbol in self._python_regex:
            if symbol == "[" and (not regex_temp or regex_temp[-1] != "\\"):
                in_brackets += 1
                in_brackets_temp.append([])
            elif symbol == "]" and (not regex_temp or regex_temp[-1] != "\\"):
                if len(in_brackets_temp) == 1:
                    regex_temp.append("(")
                    regex_temp += self._preprocess_brackets_content(
                        in_brackets_temp[-1])
                    regex_temp.append(")")
                else:
                    in_brackets_temp[-2].append(
                        "(" +
                        "".join(
                            self._preprocess_brackets_content(
                                in_brackets_temp[-1])) +
                        ")")
                in_brackets -= 1
                in_brackets_temp.pop()
            elif in_brackets > 0:
                in_brackets_temp[-1].append(symbol)
            else:
                if self._should_escape_next_symbol(regex_temp):
                    regex_temp[-1] += symbol
                else:
                    regex_temp.append(symbol)
        self._python_regex = "".join(regex_temp)

    def _preprocess_brackets_content(self, bracket_content):
        bracket_content_temp = []
        previous_is_valid_for_range = False
        for i, symbol in enumerate(bracket_content):
            if (symbol == "-" and not self._should_escape_next_symbol(
                    bracket_content_temp)):
                if (not previous_is_valid_for_range
                        or i == len(bracket_content) - 1):
                    bracket_content_temp.append("-")
                    previous_is_valid_for_range = True
                else:
                    for j in range(ord(bracket_content[i - 1]) + 1,
                                   ord(bracket_content[i + 1])):
                        bracket_content_temp.append(chr(j))
                    previous_is_valid_for_range = False
            else:
                if self._should_escape_next_symbol(bracket_content_temp):
                    bracket_content_temp[-1] += symbol
                else:
                    bracket_content_temp.append(symbol)
                if (i != 0 and bracket_content[i - 1] == "-"
                        and not previous_is_valid_for_range):
                    previous_is_valid_for_range = False
                else:
                    previous_is_valid_for_range = True
        return "|".join(bracket_content_temp)

    def _find_previous_opening_parenthesis(self, split_sequence):
        counter = 0
        for i in range(len(split_sequence) - 1, -1, -1):
            temp = split_sequence[i]
            if temp == ")":
                counter += 1
            elif temp == "(" and counter == 1:
                return i
            elif temp == "(":
                counter -= 1
        raise MisformedRegexError(WRONG_PARENTHESIS_MESSAGE,
                                  self._python_regex)

    def _preprocess_positive_closure(self):
        regex_temp = []
        for symbol in self._python_regex:
            if symbol != "+" or (self._should_escape_next_symbol(regex_temp)):
                if self._should_escape_next_symbol(regex_temp):
                    regex_temp[-1] += symbol
                else:
                    regex_temp.append(symbol)
            elif regex_temp[-1] != ")":
                regex_temp.append(regex_temp[-1])
                regex_temp.append("*")
            else:
                pos_opening = \
                    self._find_previous_opening_parenthesis(regex_temp)
                for j in range(pos_opening, len(regex_temp)):
                    regex_temp.append(regex_temp[j])
                regex_temp.append("*")
        self._python_regex = "".join(regex_temp)

    def _preprocess_dot(self):
        self._python_regex = self._python_regex.replace(".", DOT_REPLACEMENT)

    def _preprocess_optional(self):
        regex_temp = []
        for symbol in self._python_regex:
            if symbol == "?":
                if regex_temp[-1] == ")":
                    regex_temp[-1] = "|$)"
                elif regex_temp[-1] == "\\":
                    regex_temp[-1] = "?"
                else:
                    regex_temp[-1] = "(" + regex_temp[-1] + "|$)"
            else:
                if self._should_escape_next_symbol(regex_temp):
                    regex_temp[-1] += symbol
                else:
                    regex_temp.append(symbol)
        self._python_regex = "".join(regex_temp)

    @staticmethod
    def _should_escape_next_symbol(regex_temp):
        return regex_temp and regex_temp[-1] == "\\"

    def _escape_in_brackets(self):
        regex_temp = []
        in_brackets = False
        for symbol in self._python_regex:
            if (symbol == "["
                    and not self._should_escape_next_symbol(regex_temp)):
                in_brackets = True
            elif (symbol == "]"
                  and not self._should_escape_next_symbol(regex_temp)):
                in_brackets = False
            if (in_brackets
                    and not self._should_escape_next_symbol(regex_temp)
                    and symbol in TO_ESCAPE_IN_BRACKETS):
                regex_temp.append("\\" + symbol)
            else:
                regex_temp.append(symbol)
        self._python_regex = "".join(regex_temp)

    def _replace_shortcuts(self):
        for to_replace, replacement in SHORTCUTS.items():
            self._python_regex = self._python_regex.replace(to_replace,
                                                            replacement)
