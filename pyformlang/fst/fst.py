""" Finite State Transducer """

from typing import Any, Iterable

from pyformlang.indexed_grammar import DuplicationRule, ProductionRule, EndRule,\
    ConsumptionRule, IndexedGrammar, Rules

class FST(object):
    """ Representation of a Finite State Transducer"""

    def __init__(self):
        self._states = set()  # Set of states
        self._input_symbols = set()  # Set of input symbols
        self._output_symbols = set()  # Set of output symnols
        # Dict from _states x _input_symbols U {epsilon} into a subset of _states X _output_symbols*
        self._delta = dict()
        self._start_states = set()
        self._final_states = set()  # _final_statesinal states

    def get_number_states(self) -> int:
        """ Get the number of states in the FST

        Returns
        ----------
        n_states : int
            The number of states
        """
        return len(self._states)

    def get_number_final_states(self) -> int:
        """ Get the number of final states in the FST

        Returns
        ----------
        n_final_states : int
            The number of final states
        """
        return len(self._final_states)

    def get_number_input_symbols(self) -> int:
        """ Get the number of input symbols in the FST

        Returns
        ----------
        n_input_symbols : int
            The number of input symbols
        """
        return len(self._input_symbols)

    def get_number_output_symbols(self) -> int:
        """ Get the number of output symbols in the FST

        Returns
        ----------
        n_output_symbols : int
            The number of output symbols
        """
        return len(self._output_symbols)

    def get_number_transitions(self) -> int:
        """ Get the number of transitions in the FST

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        return sum([len(x) for x in self._delta.values()])

    def get_number_start_states(self) -> int:
        """ Get the number of start states in the FST

        Returns
        ----------
        n_start_states : int
            The number of start states
        """
        return len(self._start_states)


    def add_transition(self, s_from: Any,
                       input_symbol: Any,
                       s_to: Any,
                       output_symbols: Iterable[Any]):
        """ Add a transition to the FST

        Parameters
        -----------
        s_from : any
            The source state
        input_symbol : any
            The symbol to read
        s_to : any
            The destination state
        output_symbols : iterable of Any
            The symbols to output
        """
        self._states.add(s_from)
        self._states.add(s_to)
        if input_symbol != "epsilon":
            self._input_symbols.add(input_symbol)
        for output_symbol in output_symbols:
            if output_symbol != "epsilon":
                self._output_symbols.add(output_symbol)
        head = (s_from, input_symbol)
        if head in self._delta:
            self._delta[head].append((s_to, output_symbols))
        else:
            self._delta[head] = [(s_to, output_symbols)]

    def add_start_state(self, start_state: Any):
        """ Add a start state

        Parameters
        ----------
        start_state : any
            The start state
        """
        self._states.add(start_state)
        self._start_states.add(start_state)

    def add_final_state(self, final_state: Any):
        """ Add a final state

        Parameters
        ----------
        final_state : any
            The final state to add
        """
        self._final_states.add(final_state)
        self._states.add(final_state)

    def translate(self, input_word: Iterable[Any], max_length: int=-1) -> Iterable[Any]:
        """ Translate a string into another using the FST

        Parameters
        ----------
        input_word : iterable of any
            The word to translate
        max_length : int, optional
            The maximum size of the output word, to prevent infinite generation due to\
                epsilon transitions

        Returns
        ----------
        output_word : iterable of any
            The translation of the input word
        """
        # (remaining in the input, generated so far, current_state)
        to_process = []
        for start_state in self._start_states:
            to_process.append((input_word, [], start_state))
        while to_process:
            remaining, generated, current_state = to_process.pop()
            if len(remaining) == 0 and current_state in self._final_states:
                yield generated
            # We try to read an input
            if len(remaining) != 0:
                for next_state, output_string in self._delta.get((current_state, remaining[0]),
                                                                 []):
                    to_process.append((remaining[1:], generated + output_string, next_state))
            # We try to read an epsilon transition
            if max_length == -1 or len(generated) < max_length:
                for next_state, output_string in self._delta.get((current_state, "epsilon"),
                                                                 []):
                    to_process.append((remaining, generated + output_string, next_state))

    def intersection(self, indexed_grammar):
        """ Compute the intersection with an other object """
        rules = indexed_grammar.rules
        new_rules = []
        terminals = rules.get_terminals()
        new_rules.append(EndRule("T", "epsilon"))
        consumptions = rules.get_consumption_rules()
        for f in consumptions:
            for consumption in consumptions[f]:
                for r in self._states:
                    for s in self._states:
                        new_rules.append(ConsumptionRule(
                            consumption.get_f(),
                            str((r, consumption.get_left_term(), s)),
                            str((r, consumption.get_right(), s))))
        for rule in rules.get_rules():
            if rule.is_duplication():
                for p in self._states:
                    for q in self._states:
                        for r in self._states:
                            new_rules.append(DuplicationRule(
                                str((p, rule.get_left_term(), q)),
                                str((p, rule.get_right_terms()[0], r)),
                                str((r, rule.get_right_terms()[1], q))))
            elif rule.is_production():
                for p in self._states:
                    for q in self._states:
                        new_rules.append(ProductionRule(
                            str((p, rule.get_left_term(), q)),
                            str((p, rule.get_right_term(), q)),
                            str(rule.get_production())))
            elif rule.is_end_rule():
                for p in self._states:
                    for q in self._states:
                        new_rules.append(DuplicationRule(
                            str((p, rule.get_left_term(), q)),
                            str((p, rule.get_right_term(), q)),
                            "T"))
        for a in terminals:
            for p in self._states:
                for q in self._states:
                    for r in self._states:
                        new_rules.append(DuplicationRule(
                            str((p, a, q)),
                            str((p, "epsilon", r)),
                            str((r, a, q))))
                        new_rules.append(DuplicationRule(
                            str((p, a, q)),
                            str((p, a, r)),
                            str((r, "epsilon", q))))
        for p in self._states:
            for q in self._states:
                for r in self._states:
                    new_rules.append(DuplicationRule(
                        str((p, "epsilon", q)),
                        str((p, "epsilon", r)),
                        str((r, "epsilon", q))))
        for key in self._delta:
            p = key[0]
            a = key[1]
            for transition in self._delta[key]:
                q = transition[0]
                x = transition[1]
                new_rules.append(EndRule(
                    str((p, a, q)),
                    x))
        for p in self._states:
            new_rules.append(EndRule(
                str((p, "epsilon", p)),
                "epsilon"))
        for p in self._final_states:
            for start_state in self._start_states:
                new_rules.append(DuplicationRule(
                    "S",
                    str((start_state, "S", p)),
                    "T"))
        rules = Rules(new_rules, rules.optim)
        return IndexedGrammar(rules).remove_useless_rules()
