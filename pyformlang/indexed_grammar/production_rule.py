"""
Represents a production rule, i.e. a rule that pushed on the stack
"""

from typing import Any, Iterable, AbstractSet

from .reduced_rule import ReducedRule


class ProductionRule(ReducedRule):
    """Represents a production rule, i.e. a rule of the form:
        A[sigma] -> B[r sigma]

    Parameters
    ----------
    left : any
        The non-terminal on the left side of the rule, A here
    right : any
        The non-terminal on the right side of the rule, B here
    prod : any
        The terminal used in the rule, "r" here
    """

    def __init__(self, left, right, prod):
        self.production = prod
        self.left_term = left
        self.right_term = right

    def is_production(self) -> bool:
        """Whether the rule is a production rule or not

        Returns
        ----------
        is_production : bool
            Whether the rule is a production rule or not
        """
        return True

    def get_production(self) -> Any:
        """Gets the terminal used in the production

        Returns
        ----------
        production : any
            The production used in this rule
        """
        return self.production

    def get_left_term(self) -> Any:
        """Gets the non-terminal on the left side of the rule

        Returns
        ----------
        left_term : any
            The left term of this rule
        """
        return self.left_term

    def get_right_term(self) -> Any:
        """Gets the non-terminal on the right side of the rule

        Returns
        ----------
        right_term : any
            The right term used in this rule
        """
        return self.right_term

    def get_non_terminals(self) -> Iterable[Any]:
        """Gets the non-terminals used in the rule

        Returns
        ----------
        non_terminals : any
            The non terminals used in this rules
        """
        return [self.left_term, self.right_term]

    def get_terminals(self) -> AbstractSet[Any]:
        """Gets the terminals used in the rule

        Returns
        ----------
        terminals : any
            The terminals used in this rule
        """
        return {self.production}

    def __repr__(self):
        """Gets the string representation of the rule"""
        return self.left_term + " -> " + \
            self.right_term + "[ " + self.production + " ]"

    def __eq__(self, other):
        return other.is_production() and other.get_left_term() == \
            self.get_left_term() and other.get_right_term() == self.get_right_term()\
            and other.get_production() == self.get_production()
