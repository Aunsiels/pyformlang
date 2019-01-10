"""
Representation of a state in a finite state automaton
"""

from typing import Any
from .finite_automaton_object import FiniteAutomatonObject


class State(FiniteAutomatonObject): # pylint: disable=too-few-public-methods
    """ A state in a finite automaton

    Parameters
    ----------
    value : any
        The value of the state

    Attributes
    ----------

    Examples
    ----------
    >>> from pyformlang.finite_automaton import State
    >>> State("A")
    A

    See also
    ----------
    """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, State):
            return self._value == other.get_value()
        return False

    def __hash__(self) -> int:
        return hash(self._value)
