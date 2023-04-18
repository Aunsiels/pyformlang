from typing import Tuple

from pyformlang.cfg import Variable
from pyformlang.fcfg.feature_production import FeatureProduction
from pyformlang.fcfg.feature_structure import FeatureStructure


class State:

    def __init__(self,
                 production: FeatureProduction,
                 positions: Tuple[int, int, int],
                 feature_stucture: FeatureStructure):
        self.production = production
        self.positions = positions
        self.feature_stucture = feature_stucture

    def get_key(self):
        return self.production, self.positions

    def is_incomplete(self):
        return self.positions[2] < len(self.production.body)

    def next_is_variable(self):
        return isinstance(self.production.body[self.positions[2]], Variable)

    def next_is_word(self, word):
        return self.production.body[self.positions[2]] == word


class StateProcessed:

    def __init__(self, size: int):
        self.processed = [dict() for _ in range(size)]

    def add(self, i: int, element: State):
        key = element.get_key()
        if key not in self.processed[i]:
            self.processed[i][key] = []
        for other in self.processed[i][key]:
            if other.feature_stucture.subsumes(element.feature_stucture):
                return False
        self.processed[i][key].append(element)
        return True

    def generator(self, i: int):
        for states in self.processed[i].values():
            for state in states:
                yield state
