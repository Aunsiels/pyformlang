""" Finite State Transducer """

from typing import Any, Iterable

from pyformlang.indexed_grammar import DuplicationRule, ProductionRule, EndRule,\
    ConsumptionRule, IndexedGrammar, Rules


class FST:
    """ Representation of a Finite State Transducer"""

    def __init__(self):
        self._states = set()  # Set of states
        self._input_symbols = set()  # Set of input symbols
        self._output_symbols = set()  # Set of output symnols
        # Dict from _states x _input_symbols U {epsilon} into a subset of _states X _output_symbols*
        self._delta = dict()
        self._start_states = set()
        self._final_states = set()  # _final_statesinal states

    @property
    def states(self):
        """ Get the states of the FST

        Returns
        ----------
        states : set of any
            The states
        """
        return self._states

    @property
    def input_symbols(self):
        """ Get the input symbols of the FST

        Returns
        ----------
        input_symbols : set of any
            The input symbols of the FST
        """
        return self._input_symbols

    @property
    def output_symbols(self):
        """ Get the output symbols of the FST

        Returns
        ----------
        output_symbols : set of any
            The output symbols of the FST
        """
        return self._output_symbols

    @property
    def start_states(self):
        """ Get the start states of the FST

        Returns
        ----------
        start_states : set of any
            The start states of the FST
        """
        return self._start_states

    @property
    def final_states(self):
        """ Get the final states of the FST

        Returns
        ----------
        final_states : set of any
            The final states of the FST
        """
        return self._final_states

    def get_number_transitions(self) -> int:
        """ Get the number of transitions in the FST

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        return sum([len(x) for x in self._delta.values()])

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

    def translate(self, input_word: Iterable[Any], max_length: int = -1) -> \
            Iterable[Any]:
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
        """ Compute the intersection with an other object

        Equivalent to:
          >> fst and indexed_grammar
        """
        rules = indexed_grammar.rules
        new_rules = []
        new_rules.append(EndRule("T", "epsilon"))
        self._extract_consumption_rules_intersection(rules, new_rules)
        self._extract_indexed_grammar_rules_intersection(rules, new_rules)
        self._extract_terminals_intersection(rules, new_rules)
        self._extract_epsilon_transitions_intersection(new_rules)
        self._extract_fst_delta_intersection(new_rules)
        self._extract_fst_epsilon_intersection(new_rules)
        self._extract_fst_duplication_rules_intersection(new_rules)
        rules = Rules(new_rules, rules.optim)
        return IndexedGrammar(rules).remove_useless_rules()

    def _extract_fst_duplication_rules_intersection(self, new_rules):
        for state_p in self._final_states:
            for start_state in self._start_states:
                new_rules.append(DuplicationRule(
                    "S",
                    str((start_state, "S", state_p)),
                    "T"))

    def _extract_fst_epsilon_intersection(self, new_rules):
        for state_p in self._states:
            new_rules.append(EndRule(
                str((state_p, "epsilon", state_p)),
                "epsilon"))

    def _extract_fst_delta_intersection(self, new_rules):
        for key in self._delta:
            state_p = key[0]
            terminal = key[1]
            for transition in self._delta[key]:
                state_q = transition[0]
                symbol = transition[1]
                new_rules.append(EndRule(str((state_p, terminal, state_q)),
                                         symbol))

    def _extract_epsilon_transitions_intersection(self, new_rules):
        for state_p in self._states:
            for state_q in self._states:
                for state_r in self._states:
                    new_rules.append(DuplicationRule(
                        str((state_p, "epsilon", state_q)),
                        str((state_p, "epsilon", state_r)),
                        str((state_r, "epsilon", state_q))))

    def _extract_indexed_grammar_rules_intersection(self, rules, new_rules):
        for rule in rules.rules:
            if rule.is_duplication():
                for state_p in self._states:
                    for state_q in self._states:
                        for state_r in self._states:
                            new_rules.append(DuplicationRule(
                                str((state_p, rule.left_term, state_q)),
                                str((state_p, rule.right_terms[0], state_r)),
                                str((state_r, rule.right_terms[1], state_q))))
            elif rule.is_production():
                for state_p in self._states:
                    for state_q in self._states:
                        new_rules.append(ProductionRule(
                            str((state_p, rule.left_term, state_q)),
                            str((state_p, rule.right_term, state_q)),
                            str(rule.production)))
            elif rule.is_end_rule():
                for state_p in self._states:
                    for state_q in self._states:
                        new_rules.append(DuplicationRule(
                            str((state_p, rule.left_term, state_q)),
                            str((state_p, rule.right_term, state_q)),
                            "T"))

    def _extract_terminals_intersection(self, rules, new_rules):
        terminals = rules.terminals
        for terminal in terminals:
            for state_p in self._states:
                for state_q in self._states:
                    for state_r in self._states:
                        new_rules.append(DuplicationRule(
                            str((state_p, terminal, state_q)),
                            str((state_p, "epsilon", state_r)),
                            str((state_r, terminal, state_q))))
                        new_rules.append(DuplicationRule(
                            str((state_p, terminal, state_q)),
                            str((state_p, terminal, state_r)),
                            str((state_r, "epsilon", state_q))))

    def _extract_consumption_rules_intersection(self, rules, new_rules):
        consumptions = rules.consumption_rules
        for consumption_rule in consumptions:
            for consumption in consumptions[consumption_rule]:
                for state_r in self._states:
                    for state_s in self._states:
                        new_rules.append(ConsumptionRule(
                            consumption.f_parameter,
                            str((state_r, consumption.left_term, state_s)),
                            str((state_r, consumption.right, state_s))))

    def __and__(self, other):
        return self.intersection(other)
