import numpy as np


class HopcroftProcessingList(object):

    def __init__(self, n_states, symbols):
        self._reverse_symbols = dict()
        for i, symbol in enumerate(symbols):
            self._reverse_symbols[symbol] = i
        self._inclusion = np.zeros((n_states, len(symbols)), dtype=bool)
        self._elements = []

    def is_empty(self):
        return len(self._elements) == 0

    def contains(self, class_name, symbol):
        i_symbol = self._reverse_symbols[symbol]
        return self._inclusion[class_name, i_symbol]

    def insert(self, class_name, symbol):
        i_symbol = self._reverse_symbols[symbol]
        self._inclusion[class_name, i_symbol] = True
        self._elements.append((class_name, symbol))

    def pop(self):
        res = self._elements.pop()
        i_symbol = self._reverse_symbols[res[1]]
        self._inclusion[res[0], i_symbol] = False
        return res
