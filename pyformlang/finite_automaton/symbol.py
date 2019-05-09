"""
This module describe a symbol in a finite automaton.
"""


from typing import Any
from .finite_automaton_object import FiniteAutomatonObject


class Symbol(FiniteAutomatonObject): # pylint: disable=too-few-public-methods
    """ A symbol in a finite automaton

    Parameters
    ----------
    value : any
        The value of the symbol

    Attributes
    ----------

    Examples
    ----------
    >>> from pyformlang.finite_automaton import Symbol
    >>> Symbol("A")
    A

    See also
    ----------
    """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Symbol):
            return self._value == other.get_value()
        return False

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self._value)
        return self._hash
