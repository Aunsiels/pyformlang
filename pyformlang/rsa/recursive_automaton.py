from typing import AbstractSet

from pyformlang.finite_automaton.finite_automaton import to_symbol
from pyformlang.finite_automaton.symbol import Symbol
from pyformlang.rsa.box import Box


# TODO: add description

class RecursiveAutomaton:

    def __init__(self,
                 new_labels: AbstractSet[Symbol] = None,
                 new_initial_label: Symbol = None,
                 new_boxes: AbstractSet[Box] = None):
        # TODO: update tests

        if new_labels is not None:
            new_labels = {to_symbol(x) for x in new_labels}
        self._labels = new_labels or set()

        if new_initial_label is not None:
            new_initial_label = to_symbol(new_initial_label)
            if new_initial_label not in self._labels:
                self._labels.add(new_initial_label)
        self._initial_label = new_initial_label or Symbol("")

        self._boxes = new_boxes or set()

        for label in self._labels:
            box = self.get_box(label)
            if box is None:
                raise ValueError("RSA must have the same number of labels and NFAs")

        for box in self._boxes:
            if box.label() not in self._labels:
                self._labels.add(box.label())

    def get_box(self, label: Symbol):
        # TODO: create tests

        for box in self._boxes:
            if box.label() == label:
                return box

        return None

    def add_box(self, new_box: Box):
        if new_box.label() in self._labels:
            # TODO: create test for this case
            self._boxes.discard(new_box)
        else:
            self._labels.add(new_box.label())

        self._boxes.add(new_box)

    def change_initial_label(self, new_initial_label: Symbol):
        # TODO: create tests
        new_initial_label = Symbol(new_initial_label)
        if new_initial_label not in self._labels:
            raise ValueError("New initial label not in set of labels for boxes")

    def labels(self) -> set:
        # TODO: create tests
        return self._labels

    def boxes(self) -> set:
        # TODO: create tests
        return self._boxes

    def initial_label(self) -> Symbol:
        # TODO: create tests
        return self._initial_label
