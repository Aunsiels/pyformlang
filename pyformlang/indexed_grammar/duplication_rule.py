"""
A representation of a duplication rule, i.e. a rule that duplicates the stack
"""

from typing import Any, Iterable, AbstractSet

from .reduced_rule import ReducedRule


class DuplicationRule(ReducedRule):
    """Represents a duplication rule, i.e. a rule of the form:
        A[sigma] -> B[sigma] C[sigma]

    Parameters
    ----------
    left_term : any
        The non-terminal on the left of the rule (A here)
    right_term0 : any
        The first non-terminal on the right of the rule (B here)
    right_term1 : any
        The second non-terminal on the right of the rule (C here)
    """

    def __init__(self, left_term, right_term0, right_term1):
        self.left_term = left_term
        self.right_terms = (right_term0, right_term1)

    def is_duplication(self) -> bool:
        """Whether the rule is a duplication rule or not

        Returns
        ----------
        is_duplication : bool
            Whether the rule is a duplication rule or not
        """
        return True

    def get_right_terms(self) -> Iterable[Any]:
        """Gives the non-terminals on the right of the rule

        Returns
        ---------
        right_terms : iterable of any
            The right terms of the rule
        """
        return self.right_terms

    def get_left_term(self) -> Any:
        """Gives the non-terminal on the left of the rule

        Returns
        ---------
        left_term : any
            The left term of the rule
        """
        return self.left_term

    def get_non_terminals(self) -> Iterable[Any]:
        """Gives the set of non-terminals used in this rule

        Returns
        ---------
        non_terminals : iterable of any
            The non terminals used in this rule
        """
        return [self.left_term, self.right_terms[0], self.right_terms[1]]

    def get_terminals(self) -> AbstractSet[Any]:
        """Gets the terminals used in the rule

        Returns
        ----------
        terminals : set of any
            The terminals used in this rule
        """
        return {}

    def __repr__(self):
        """Gives a string representation of the rule, ignoring the sigmas"""
        return self.left_term + " -> " + self.right_terms[0] + \
            " " + self.right_terms[1]

    def __eq__(self, other):
        return other.is_duplication() and other.left_term == \
            self.left_term and other.get_right_terms() == self.get_right_terms()
