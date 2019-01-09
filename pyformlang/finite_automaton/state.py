from typing import Any


class State(object):
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

    def __init__(self, value: Any):
        self._value = value

    def __repr__(self) -> str:
        return str(self._value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, State):
            return self._value == other._value
        return False

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, State):
            return self._value != other._value
        return True

    def __hash__(self) -> int:
        return hash(self._value)
