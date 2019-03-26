""" A StackSymbol in a pushdown automaton """

class StackSymbol(object):
    """ A StackSymbol in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __init__(self, value):
        self._value = value

    def __hash__(self):
        return hash(str(self._value))

    def get_value(self):
        """ Returns the value of the stack symbol

        Returns
        ----------
        value: The value
            any
        """
        return self._value

    def __eq__(self, other):
        if isinstance(other, StackSymbol):
            return self._value == other.get_value()
        return False

    def __repr__(self):
        return "StackSymbol(" + str(self._value) + ")"
