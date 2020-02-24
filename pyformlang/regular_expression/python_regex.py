import re
import string

from pyformlang.regular_expression import Regex

DOT_REPLACEMENT = "(" + "|".join((string.ascii_letters + string.punctuation +
                                  string.digits)
                                 .replace("\n", "")
                                 .replace("|", "")
                                 .replace("(", "")
                                 .replace(")", "")
                                 .replace("*", "")
                                 .replace("+", "")
                                 .replace(".", "")
                                 .replace("$", "")) + ")"


class PythonRegex(Regex):
    """ Represents a regular expression as used in Python. It adds the
    following features to the basic regex:

    * Set of characters with []
    * positive closure +
    * . for all letters, punctuation or digits different from |, (, ), *, +,
    ., $ (TODO: not like in python)

        Parameters
        ----------
        regex : str
            The regex represented as a string or a compiled regex (
            re.compile(...))
    """

    def __init__(self, regex):
        if not isinstance(regex, str):
            regex = regex.pattern
        else:
            re.compile(regex)  # Check if it is valid
        self._python_regex = regex
        self._preprocess_brackets()
        self._preprocess_positive_closure()
        self._preprocess_dot()
        super().__init__(" ".join(self._python_regex))

    def _preprocess_brackets(self):
        regex_temp = []
        in_brackets = False
        in_brackets_temp = []
        for symbol in self._python_regex:
            if symbol == "[":
                regex_temp.append("(")
                in_brackets = True
            elif symbol == "]":
                regex_temp += self._preprocess_brackets_content(
                    in_brackets_temp)
                regex_temp.append(")")
                in_brackets = False
                in_brackets_temp = []
            elif in_brackets:
                in_brackets_temp.append(symbol)
            else:
                regex_temp.append(symbol)
        self._python_regex = "".join(regex_temp)

    def _preprocess_brackets_content(self, bracket_content):
        bracket_content_temp = []
        previous_is_valid_for_range = False
        for i, symbol in enumerate(bracket_content):
            if symbol == "-":
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
                bracket_content_temp.append(symbol)
                if (i != 0 and bracket_content[i - 1] == "-"
                        and not previous_is_valid_for_range):
                    previous_is_valid_for_range = False
                else:
                    previous_is_valid_for_range = True
        return "|".join(bracket_content_temp)

    def _find_previous_opening_parenthesis(self, pos):
        counter = 0
        for i in range(pos - 1, 0, -1):
            temp = self._python_regex[i]
            if temp == ")":
                counter += 1
            elif temp == "(" and counter == 0:
                return i
            elif temp == "(":
                counter -= 1
        return -1  # Not supposed to happen if valid

    def _preprocess_positive_closure(self):
        regex_temp = []
        for i, symbol in enumerate(self._python_regex):
            if symbol != "+":
                regex_temp.append(symbol)
            elif self._python_regex[i - 1] != ")":
                regex_temp.append(self._python_regex[i - 1])
                regex_temp.append("*")
            else:
                pos_opening = self._find_previous_opening_parenthesis(i - 1)
                for j in range(pos_opening, i):
                    regex_temp.append(self._python_regex[j])
                regex_temp.append("*")
        self._python_regex = "".join(regex_temp)

    def _preprocess_dot(self):
        self._python_regex = self._python_regex.replace(".", DOT_REPLACEMENT)
