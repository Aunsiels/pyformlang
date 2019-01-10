"""
Represents an object of a finite state automaton
"""

from typing import Any

class FiniteAutomatonObject(object): # pylint: disable=too-few-public-methods
    """ Represents an object in a finite state automaton

    Parameters
    ----------
    value: any
        The value of the object
    """

    def __init__(self, value: Any):
        self._value = value

    def __repr__(self) -> str:
        return str(self._value)

    def get_value(self) -> Any:
        """ Gets the value of the object

        Returns
        ---------
        value : any
            The value of the object
        """
        return self._value
