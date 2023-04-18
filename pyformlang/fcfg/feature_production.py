from typing import List

from pyformlang.cfg import Production, Variable
from pyformlang.cfg.cfg_object import CFGObject
from pyformlang.fcfg.feature_structure import FeatureStructure


class FeatureProduction(Production):

    def __init__(self, head: Variable, body: List[CFGObject], head_feature, body_features, filtering=True):
        super().__init__(head, body, filtering)
        self._features = FeatureStructure()
        self._features.add_content("head", head_feature)
        for i, fs in enumerate(body_features):
            self._features.add_content(str(i), fs)

    @property
    def features(self):
        return self._features
