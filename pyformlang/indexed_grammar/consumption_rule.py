"""
Representation of a consumption rule, i.e. a rule that consumes something on the
stack
"""

from typing import Any, Iterable, AbstractSet

from .reduced_rule import ReducedRule


class ConsumptionRule(ReducedRule):
    """ Contains a representation of a consumption rule, i.e. a rule of the form:
            C[ r sigma] -> B[sigma]

    Parameters
    ----------
    f : any
        The consumed symbol
    left : any
        The non terminal on the left (here C)
    right : any
        The non terminal on the right (here B)
    """

    def __init__(self, f : Any, left : Any, right : Any):
        self.f = f
        self.right = right
        self.left_term = left

    def is_consumption(self) -> bool:
        """Whether the rule is a consumption rule or not

        Returns
        ----------
        is_consumption : bool
            Whether the rule is a consumption rule or not
        """
        return True

    def get_f(self) -> Any:
        """Gets the symbol which is consumed

        Returns
        ----------
        f : any
            The symbol being consumed by the rule
        """
        return self.f

    def get_right(self) -> Any:
        """Gets the symbole on the right of the rule

        right : any
            The right symbol
        """
        return self.right

    def get_left_term(self) -> Any:
        """Gets the symbol on the left of the rule

        left : any
            The left symbol of the rule
        """
        return self.left_term

    def get_non_terminals(self) -> Iterable[Any]:
        """Gets the non-terminals used in the rule

        non_terminals : iterable of any
            The non_terminals used in the rule
        """
        return [self.left_term, self.right]

    def get_terminals(self) -> AbstractSet[Any]:
        """Gets the terminals used in the rule

        terminals : set of any
            The terminals used in the rule
        """
        return {self.f}

    def __repr__(self):
        return self.left_term + " [ " + self.f + " ] -> " + self.right

    def __eq__(self, other):
        return other.is_consumption() and other.get_left_term() == \
            self.get_left_term() and other.get_right() == self.get_right() and\
            other.get_f() == self.get_f()
