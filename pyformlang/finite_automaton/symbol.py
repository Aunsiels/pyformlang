from typing import Any


class Symbol(object):
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

    def __init__(self, value: Any):
        self._value = value

    def __repr__(self) -> str:
        return str(self._value)

    def __eq__(self, other: Any) -> str:
        if isinstance(other, Symbol):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(self._value)
