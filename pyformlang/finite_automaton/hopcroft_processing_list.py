""" A representation for Hopcroft minimization algorithm
For internal usage
"""

from typing import Dict, List, Set, Tuple
from numpy import zeros

from .symbol import Symbol


class HopcroftProcessingList:
    """ A representation for Hopcroft minimization algorithm
    For internal usage
    """

    def __init__(self, n_states: int, symbols: Set[Symbol]) -> None:
        self._reverse_symbols: Dict[Symbol, int] = {}
        for i, symbol in enumerate(symbols):
            self._reverse_symbols[symbol] = i
        self._inclusion = zeros((n_states, len(symbols)), dtype=bool)
        self._elements: List[Tuple[int, Symbol]] = []

    def is_empty(self) -> bool:
        """Check if empty"""
        return len(self._elements) == 0

    def contains(self, class_name: int, symbol: Symbol) -> bool:
        """ Check containment """
        i_symbol = self._reverse_symbols[symbol]
        return self._inclusion[class_name, i_symbol]

    def insert(self, class_name: int, symbol: Symbol) -> None:
        """ Insert new element """
        i_symbol = self._reverse_symbols[symbol]
        self._inclusion[class_name, i_symbol] = True
        self._elements.append((class_name, symbol))

    def pop(self) -> Tuple[int, Symbol]:
        """ Pop an element """
        res = self._elements.pop()
        i_symbol = self._reverse_symbols[res[1]]
        self._inclusion[res[0], i_symbol] = False
        return res
