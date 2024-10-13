"""
Represents an epsilon transition
"""

from typing import Any
from .symbol import Symbol


class Epsilon(Symbol):  # pylint: disable=too-few-public-methods
    """ An epsilon transition

    Examples
    --------

    >>> epsilon = Epsilon()

    """

    def __init__(self) -> None:
        super().__init__("epsilon")

    def __hash__(self) -> int:
        return hash("EPSILON TRANSITION")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Epsilon):
            return True
        return False
