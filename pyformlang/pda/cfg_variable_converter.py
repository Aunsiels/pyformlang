from pyformlang import cfg


class CFGVariableConverter(object):

    def __init__(self, states, stack_symbols):
        self._counter = 0
        self._inverse_states_d = dict()
        for i, state in enumerate(states):
            self._inverse_states_d[state] = i
            state.index_cfg_converter = i
        self._inverse_stack_symbol_d = dict()
        for i, symbol in enumerate(stack_symbols):
            self._inverse_stack_symbol_d[symbol] = i
            symbol.index_cfg_converter = i
        self._conversions = [[[(False, None) for _ in range(len(states))] for _ in range(len(stack_symbols))] for _ in
                             range(len(states))]

    def get_state_index(self, state):
        if state.index_cfg_converter is None:
            self.set_index_state(state)
        return state.index_cfg_converter

    def set_index_state(self, state):
        state.index_cfg_converter = self._inverse_states_d[state]

    def get_symbol_index(self, symbol):
        if symbol.index_cfg_converter is None:
            symbol.index_cfg_converter = self._inverse_stack_symbol_d[symbol]
        return symbol.index_cfg_converter

    def to_cfg_combined_variable(self, state0, stack_symbol, state1):
        """ Conversion used in the to_pda method """
        i_stack_symbol, i_state0, i_state1 = self._get_indexes(stack_symbol, state0, state1)
        prev = self._conversions[i_state0][i_stack_symbol][i_state1]
        if prev[1] is None:
            value = "[" + str(state0.get_value()) + "; " + str(stack_symbol.get_value()) + "; " + str(state1.get_value()) + "]"
            return self._create_new_variable(i_stack_symbol, i_state0, i_state1, prev, value=value)[1]
        return prev[1]

    def _create_new_variable(self, i_stack_symbol, i_state0, i_state1, prev, value=None):
        if value is None:
            value = self._counter
        temp = (prev[0], cfg.Variable(value))
        self._counter += 1
        self._conversions[i_state0][i_stack_symbol][i_state1] = temp
        return temp

    def set_valid(self, state0, stack_symbol, state1):
        i_stack_symbol, i_state0, i_state1 = self._get_indexes(stack_symbol, state0, state1)
        prev = self._conversions[i_state0][i_stack_symbol][i_state1]
        self._conversions[i_state0][i_stack_symbol][i_state1] = (True, prev[1])

    def is_valid_and_get(self, state0, stack_symbol, state1):
        i_state0 = state0.index_cfg_converter
        i_stack_symbol = stack_symbol.index_cfg_converter
        i_state1 = state1.index_cfg_converter
        current = self._conversions[i_state0][i_stack_symbol][i_state1]
        if not current[0]:
            return None
        if current[1] is None:
            return self._create_new_variable(i_stack_symbol, i_state0, i_state1, current)[1]
        else:
            return current[1]

    def _get_indexes(self, stack_symbol, state0, state1):
        i_state0 = self.get_state_index(state0)
        i_stack_symbol = self.get_symbol_index(stack_symbol)
        i_state1 = self.get_state_index(state1)
        return i_stack_symbol, i_state0, i_state1