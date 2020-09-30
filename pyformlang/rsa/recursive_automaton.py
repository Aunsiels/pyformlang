"""
Representation of a recursive automaton
"""

from typing import AbstractSet

from pyformlang.finite_automaton.finite_automaton import to_symbol
from pyformlang.finite_automaton.symbol import Symbol
from pyformlang.rsa.box import Box
from pyformlang.regular_expression.regex import Regex


class RecursiveAutomaton:
    """ Represents a recursive automaton

    This class represents a recursive automaton.

    Parameters
    ----------
    labels : set of :class:`~pyformlang.finite_automaton.Symbol`, optional
        A finite set of labels for boxes
    initial_label : :class:`~pyformlang.finite_automaton.Symbol`, optional
        A start label for automaton
    boxes : set of :class:`~pyformlang.rsa.Box`, optional
        A finite set of boxes

    """

    def __init__(self,
                 labels: AbstractSet[Symbol] = None,
                 initial_label: Symbol = None,
                 boxes: AbstractSet[Box] = None):

        if labels is not None:
            labels = {to_symbol(x) for x in labels}
        self._labels = labels or set()

        if initial_label is not None:
            initial_label = to_symbol(initial_label)
            if initial_label not in self._labels:
                self._labels.add(initial_label)
        self._initial_label = initial_label or Symbol("")

        self._boxes = dict()
        if boxes is not None:
            for box in boxes:
                self._boxes.update({to_symbol(box.label): box})
                self._labels.add(box.label)

        for label in self._labels:
            box = self.get_box(label)
            if box is None:
                raise ValueError("RSA must have the same number of labels and DFAs")

    def get_box(self, label: Symbol):
        """ Box by label """

        label = to_symbol(label)
        if label in self._boxes:
            return self._boxes[label]

        return None

    def add_box(self, new_box: Box):
        """ Set a box

        Parameters
        -----------
        new_box : :class:`~pyformlang.rsa.Box`
            The new box

        """

        self._boxes.update({new_box.label: new_box})
        self._labels.add(to_symbol(new_box.label))

    def get_number_of_boxes(self):
        """ Size of set of boxes """

        return len(self._boxes)

    def change_initial_label(self, new_initial_label: Symbol):
        """ Set an initial label

        Parameters
        -----------
        new_initial_label : :class:`~pyformlang.finite_automaton.Symbol`
            The new initial label

        """

        new_initial_label = to_symbol(new_initial_label)
        if new_initial_label not in self._labels:
            raise ValueError("New initial label not in set of labels for boxes")

    @property
    def labels(self) -> set:
        """ The set of labels """

        return self._labels

    @property
    def boxes(self) -> dict:
        """ The set of boxes """

        return self._boxes

    @property
    def initial_label(self) -> Symbol:
        """ The initial label """

        return self._initial_label

    @classmethod
    def from_regex(cls, regex: str, initial_label: Symbol):
        """ Create a recursive automaton from regular expression

        Parameters
        -----------
        regex : str
            The regular expression
        initial_label : :class:`~pyformlang.finite_automaton.Symbol`
            A initial label for the recursive automaton

        Returns
        -----------
        rsa : :class:`~pyformlang.rsa.RecursiveAutomaton`
            The new recursive automaton
        """

        initial_label = Symbol(initial_label)
        box = Box(Regex(regex).to_epsilon_nfa(), initial_label)
        return RecursiveAutomaton({initial_label}, initial_label, {box})

    def is_equivalent_to(self, other):
        """ Check whether two recursive automata are equivalent

        Parameters
        ----------
        other : :class:`~pyformlang.rsa.RecursiveAutomaton`
            The input recursive automaton

        Returns
        ----------
        are_equivalent : bool
            Whether the two recursive automata are equivalent or not
        """

        if not isinstance(other, RecursiveAutomaton):
            return False

        if self._labels != other._labels:
            return False

        for label in self._labels:
            box_1 = self.get_box(label)
            box_2 = other.get_box(label)

            if not box_1.is_equivalent_to(box_2):
                return False

        return True
