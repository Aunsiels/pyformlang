""" An object in a CFG (Variable and Terminal)"""

from typing import Any


class CFGObject(object): # pylint: disable=too-few-public-methods
    """ An object in a CFG

    Parameters
    -----------
    value : any
        The value of the object
    """

    def __init__(self, value : Any):
        self._value = value
        self._hash = None

    def get_value(self) -> Any:
        return self._value
