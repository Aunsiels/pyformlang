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

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)

    def __eq__(self, other):
        if isinstance(other, State):
            return self._value == other._value
        return False

    def __neq__(self, other):
        if isinstance(other, State):
            return self._value != other._value
        return True

    def __hash__(self):
        return hash(self._value)
