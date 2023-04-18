from typing import Iterable, AbstractSet

from pyformlang.cfg import CFG, Terminal, Epsilon, Variable
from pyformlang.cfg.utils import to_terminal
from pyformlang.fcfg.feature_production import FeatureProduction
from pyformlang.fcfg.feature_structure import FeatureStructure, FeatureStructuresNotCompatibleException
from pyformlang.fcfg.state import State, StateProcessed


class FCFG(CFG):

    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: Iterable[FeatureProduction] = None):
        super().__init__(variables, terminals, start_symbol, productions)

    def predictor(self, state, chart, processed):
        # We have an incomplete state and the next token is a variable
        # We must ask to process the variable with another rule
        end_idx = state.positions[1]
        next_var = state.production.body[state.positions[2]]
        for production in self.productions:
            if production.head == next_var:
                new_state = State(production, (end_idx, end_idx, 0), production.features)
                if processed.add(end_idx, new_state):
                    chart[end_idx].append(new_state)

    def scanner(self, state, chart, processed):
        # We have an incomplete state and the next token is the word given as input
        # We move the end token and the dot token by one.
        end_idx = state.positions[1]
        new_state = State(state.production, (state.positions[0], end_idx + 1, state.positions[2] + 1),
                          state.feature_stucture)
        if processed.add(end_idx + 1, new_state):
            chart[end_idx + 1].append(new_state)

    def completer(self, state, chart, processed):
        # We have a complete state. We must check if it helps to move another state forward.
        begin_idx = state.positions[0]
        head = state.production.head
        for next_state in processed.generator(begin_idx):
            # next_state[1][1] == begin_idx always true
            if next_state.is_incomplete() and next_state.production.body[next_state.positions[2]] == head:
                try:
                    copy_left = state.feature_stucture.copy()
                    copy_left = copy_left.get_feature_by_path(["head"])
                    copy_right = next_state.feature_stucture.copy()
                    copy_right_considered = copy_right.get_feature_by_path([str(next_state.positions[2])])
                    copy_right_considered.unify(copy_left)
                except FeatureStructuresNotCompatibleException:
                    continue
                new_state = State(next_state.production,
                                  (next_state.positions[0], state.positions[1], next_state.positions[2] + 1),
                                  copy_right)
                if processed.add(state.positions[1], new_state):
                    chart[state.positions[1]].append(new_state)

    def contains(self, word: Iterable[Terminal]) -> bool:
        word = [to_terminal(x) for x in word if x != Epsilon()]
        chart = [[] for _ in range(len(word) + 1)]
        # Processed[i] contains all production rule that are currently working until i.
        processed = StateProcessed(len(word) + 1)
        gamma = Variable("Gamma")
        dummy_rule = FeatureProduction(gamma, [self.start_symbol], FeatureStructure(), [FeatureStructure()])
        # State = (rule, [begin, end, dot position, diag)
        first_state = State(dummy_rule, (0, 0, 0), dummy_rule.features)
        chart[0].append(first_state)
        processed.add(0, first_state)
        for i in range(len(chart) - 1):
            while chart[i]:
                state = chart[i].pop()
                if state.is_incomplete() and state.next_is_variable():
                    self.predictor(state, chart, processed)
                elif state.is_incomplete():
                    if state.next_is_word(word[i]):
                        self.scanner(state, chart, processed)
                else:
                    self.completer(state, chart, processed)
        while chart[len(chart) - 1]:
            state = chart[len(chart) - 1].pop()
            if not state.is_incomplete():
                self.completer(state, chart, processed)
        for state in processed.generator(len(word)):
            if state.positions[0] == 0 and not state.is_incomplete() and state.production.head == self.start_symbol:
                return True
        return False
