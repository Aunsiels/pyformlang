from pyformlang.finite_automaton.epsilon_nfa import EpsilonNFA
from pyformlang.finite_automaton.finite_automaton import to_symbol
from pyformlang.finite_automaton.symbol import Symbol


# TODO: add description

class Box:
    def __init__(self, nfa: EpsilonNFA = None, label: Symbol = None):
        if nfa is not None:
            nfa = nfa.minimize()
        self._nfa = nfa or EpsilonNFA()

        if label is not None:
            label = to_symbol(label)
        self._label = label or Symbol("")

    def change_label(self, label: Symbol):
        self._label = label

    def change_nfa(self, nfa: EpsilonNFA):
        nfa = nfa.minimize()
        self._nfa = nfa

    def nfa(self):
        return self._nfa

    def label(self):
        return self._label

    def __eq__(self, other):
        if other is Box:
            return self._label == other._label
        return self == other
