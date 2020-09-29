"""
Representation of a box for recursive automaton
"""

from pyformlang.finite_automaton.epsilon_nfa import EpsilonNFA
from pyformlang.finite_automaton.finite_automaton import to_symbol
from pyformlang.finite_automaton.symbol import Symbol


class Box:
    """ Represents a box for recursive automaton

    This class represents a box for recursive automaton

    Parameters
    ----------
    enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
        A epsilon nfa
    label : :class:`~pyformlang.finite_automaton.Symbol`
        A label for epsilon nfa

    """

    def __init__(self, enfa: EpsilonNFA = None, label: Symbol = None):
        if enfa is not None:
            enfa = enfa.minimize()
        self._dfa = enfa or EpsilonNFA()

        if label is not None:
            label = to_symbol(label)
        self._label = label or Symbol("")

    def change_label(self, label: Symbol):
        """ Set a new label

        Parameters
        -----------
        label : :class:`~pyformlang.finite_automaton.Symbol`
            The new label for automaton

        Returns
        -----------
        done : int
            1 is correctly added
        """
        self._label = label

        return 1

    def change_dfa(self, enfa: EpsilonNFA):
        """ Set an epsilon finite automaton

        Parameters
        -----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            The new epsilon finite automaton

        Returns
        -----------
        done : int
            1 is correctly added
        """
        enfa = enfa.minimize()
        self._dfa = enfa

        return 1

    def dfa(self):
        """ Box's dfa """
        return self._dfa

    def label(self):
        """ Box's label """
        return self._label

    def start_state(self):
        """ The start state """
        return self._dfa.start_states

    def final_states(self):
        """ The final states """
        return self._dfa.final_states

    def is_equivalent_to(self, other):
        """ Check whether two boxes are equivalent

        Parameters
        ----------
        other : :class:`~pyformlang.rsa.Box`
            A sequence of input symbols

        Returns
        ----------
        are_equivalent : bool
            Whether the two boxes are equivalent or not
        """

        if not isinstance(other, Box):
            return False

        if self._dfa.is_equivalent_to(other.dfa()) and self._label == other.label():
            return True

        return False
