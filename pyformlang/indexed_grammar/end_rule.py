"""
Represents a end rule, i.e. a rule which give only a terminal
"""

from typing import Any, Iterable, AbstractSet

from .reduced_rule import ReducedRule


class EndRule(ReducedRule):
    """Represents an end rule, i.e. a rule of the form:
        A[sigma] -> a

    Parameters
    -----------
    left : any
        The non-terminal on the left, "A" here
    right : any
        The terminal on the right, "a" here
    """

    def __init__(self, left, right):
        self.left_term = left
        self.right_term = right

    def is_end_rule(self) -> bool:
        """Whether the rule is an end rule or not

        Returns
        ----------
        is_end : bool
            Whether the rule is an end rule or not
        """
        return True

    def get_left_term(self) -> Any:
        """Gets the non-terminal on the left of the rule

        Returns
        ---------
        left_term : any
            The left non-terminal of the rule
        """
        return self.left_term

    def get_right_term(self) -> Any:
        """Gets the terminal on the right of the rule

        Returns
        ----------
        right_term : any
            The right terminal of the rule
        """
        return self.right_term

    def get_non_terminals(self) -> Iterable[Any]:
        """Gets the non-terminals used

        Returns
        ----------
        non_terminals : iterable of any
            The non terminals used in this rule
        """
        return [self.left_term]

    def get_terminals(self) -> AbstractSet[Any]:
        """Gets the terminals used

        Returns
        ----------
        terminals : set of any
             The terminals used in this rule
        """
        return {self.right_term}

    def __repr__(self):
        """Gets the string representation of the rule"""
        return self.left_term + " -> " + self.right_term

    def __eq__(self, other):
        return other.is_end_rule() and other.get_left_term() == self.get_left_term()\
            and other.get_right_term() == self.get_right_term()
