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

    def __repr__(self):
        res = [self.head.to_text()]
        cond_head = str(self._features.get_feature_by_path(["head"]))
        if cond_head:
            res.append("[" + cond_head + "]")
        res.append("->")
        for i, body_part in enumerate(self.body):
            res.append(body_part.to_text())
            body_part_cond = str(self._features.get_feature_by_path([str(i)]))
            if body_part_cond:
                res.append("[" + body_part_cond + "]")
        return " ".join(res)
