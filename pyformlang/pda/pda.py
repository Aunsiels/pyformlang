""" We represent here a pushdown automaton """

from typing import AbstractSet, List, Iterable, Any

from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon
from .transition_function import TransitionFunction
from .utils import to_state, to_symbol, to_stack_symbol
from pyformlang import finite_automaton
from pyformlang.regular_expression import Regex

class PDA(object):
    """ Representation of a pushdown automaton

    Parameters
    ----------
    states : set of :class:`~pyformlang.pda.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.pda.Symbol`, optional
        A finite set of input symbols
    stack_alphabet : set of :class:`~pyformlang.pda.StackSymbol`, optional
        A finite stack alphabet
    transition_function : :class:`~pyformlang.pda.TransitionFunction`, optional
        Takes as arguments a state, an input symbol and a stack symbol and returns \
            a state and a string of stack symbols push on the stacked to replace X
    start_state : :class:`~pyformlang.pda.State`, optional
        A start state, element of states
    start_stack_symbol : :class:`~pyformlang.pda.StackSymbol`, optional
        The stack is initialized with this stack symbol
    final_states : set of :class:`~pyformlang.pda.State`, optional
        A set of final or accepting states. It is a subset of states.
    """

    def __init__(self,
                 states: AbstractSet[State] = None,
                 input_symbols: AbstractSet[Symbol] = None,
                 stack_alphabet: AbstractSet[StackSymbol] = None,
                 transition_function: TransitionFunction = None,
                 start_state: State = None,
                 start_stack_symbol: StackSymbol = None,
                 final_states: AbstractSet[State] = None):
        if states is not None:
            states = set([to_state(x) for x in states])
        if input_symbols is not None:
            input_symbols = set([to_symbol(x) for x in input_symbols])
        if stack_alphabet is not None:
            stack_alphabet = set([to_stack_symbol(x) for x in stack_alphabet])
        if start_state is not None:
            start_state = to_state(start_state)
        if start_stack_symbol is not None:
            start_stack_symbol = to_stack_symbol(start_stack_symbol)
        if final_states is not None:
            final_states = set([to_state(x) for x in final_states])
        self._states = states or set()
        self._states = set(self._states)
        self._input_symbols = input_symbols or set()
        self._input_symbols = set(self._input_symbols)
        self._stack_alphabet = stack_alphabet or set()
        self._stack_alphabet = set(self._stack_alphabet)
        self._transition_function = transition_function or TransitionFunction()
        self._start_state = start_state
        if start_state is not None:
            self._states.add(start_state)
        self._start_stack_symbol = start_stack_symbol
        if start_stack_symbol is not None:
            self._stack_alphabet.add(start_stack_symbol)
        self._final_states = final_states or set()
        self._final_states = set(self._final_states)
        for state in self._final_states:
            self._states.add(state)

    def add_final_state(self, state: State):
        """ Adds a final state to the automaton

        Parameters
        ----------
        state : :class:`~pyformlang.pda.State`
            The state to add
        """
        state = to_state(state)
        self._final_states.add(state)

    def get_number_states(self) -> int:
        """ Gets the number of states

        Returns
        ----------
        n_states : int
            The number of states
        """
        return len(self._states)

    def get_number_final_states(self) -> int:
        """ Gets the number of final states

        Returns
        ----------
        n_states : int
            The number of final states
        """
        return len(self._final_states)

    def get_number_input_symbols(self) -> int:
        """ Gets the number of input symbols

        Returns
        ----------
        n_input_symbols : int
            The number of input symbols
        """
        return len(self._input_symbols)

    def get_number_stack_symbols(self) -> int:
        """ Gets the number of stack symbols

        Returns
        ----------
        n_stack_symbols : int
            The number of stack symbols
        """
        return len(self._stack_alphabet)

    def get_number_transitions(self) -> int:
        """ Gets the number of transitions in the PDA

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        return self._transition_function.get_number_transitions()

    def add_transition(self,
                       s_from: State,
                       input_symbol: Symbol,
                       stack_from: StackSymbol,
                       s_to: State,
                       stack_to: List[StackSymbol]):
        """ Add a transition to the PDA

        Parameters
        ----------
        s_from : :class:`~pyformlang.pda.State`
            The starting symbol
        input_symbol : :class:`~pyformlang.pda.Symbol`
            The input symbol
        stack_from : :class:`~pyformlang.pda.StackSymbol`
            The stack symbol of the transition
        s_to : :class:`~pyformlang.pda.State`
            The new state
        stack_to : list of :class:`~pyformlang.pda.StackSymbol`
            The string of stack symbol which replace the stack_from
        """
        s_from = to_state(s_from)
        input_symbol = to_symbol(input_symbol)
        stack_from = to_stack_symbol(stack_from)
        s_to = to_state(s_to)
        stack_to = [to_stack_symbol(x) for x in stack_to]
        self._states.add(s_from)
        self._states.add(s_to)
        if input_symbol != Epsilon():
            self._input_symbols.add(input_symbol)
        self._stack_alphabet.add(stack_from)
        for stack_symbol in stack_to:
            if stack_symbol != Epsilon():
                self._stack_alphabet.add(stack_symbol)
        self._transition_function.add_transition(s_from,
                                                 input_symbol,
                                                 stack_from,
                                                 s_to,
                                                 stack_to)

    def to_final_state(self) -> "PDA":
        """ Turns the current PDA empty stack to final state

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The new PDA which accepts by final state what was accepted by empty stack
        """
        new_start = get_next_free("#STARTTOFINAL#", State, self._states)
        new_end = get_next_free("#ENDTOFINAL#", State, self._states)
        new_stack_symbol = get_next_free("#BOTTOMTOFINAL#", StackSymbol, self._stack_alphabet)
        new_states = self._states.copy()
        new_states.add(new_start)
        new_states.add(new_end)
        new_stack_alphabet = self._stack_alphabet.copy()
        new_stack_alphabet.add(new_stack_symbol)
        new_tf = self._transition_function.copy()
        new_tf.add_transition(new_start, Epsilon(), new_stack_symbol,
                              self._start_state, (self._start_stack_symbol,
                                                  new_stack_symbol))
        for state in self._states:
            new_tf.add_transition(state, Epsilon(), new_stack_symbol,
                                  new_end, [])
        return PDA(new_states,
                   self._input_symbols.copy(),
                   new_stack_alphabet,
                   new_tf,
                   new_start,
                   new_stack_symbol,
                   {new_end})

    def to_empty_stack(self) -> "PDA":
        """ Turns the current PDA final state to empty stack

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The new PDA which accepts by empty stack what was accepted by final state
        """
        new_start = get_next_free("#STARTEMPTYS#", State, self._states)
        new_end = get_next_free("#ENDEMPTYS#", State, self._states)
        new_stack_symbol = get_next_free("#BOTTOMEMPTYS#", StackSymbol, self._stack_alphabet)
        new_states = self._states.copy()
        new_states.add(new_start)
        new_states.add(new_end)
        new_stack_alphabet = self._stack_alphabet.copy()
        new_stack_alphabet.add(new_stack_symbol)
        new_tf = self._transition_function.copy()
        new_tf.add_transition(new_start, Epsilon(), new_stack_symbol,
                              self._start_state, (self._start_stack_symbol,
                                                  new_stack_symbol))
        for state in self._final_states:
            for stack_symbol in new_stack_alphabet:
                new_tf.add_transition(state, Epsilon(), stack_symbol,
                                      new_end, [])
        for stack_symbol in new_stack_alphabet:
            new_tf.add_transition(new_end, Epsilon(), stack_symbol,
                                new_end, [])
        return PDA(new_states,
                   self._input_symbols.copy(),
                   new_stack_alphabet,
                   new_tf,
                   new_start,
                   new_stack_symbol)

    def _generate_all_rules(self, s_from: State, s_to: State,
                            ss_by: Iterable[StackSymbol]) -> Iterable[Iterable["cfg.Variable"]]:
        """ Generates the rules in the CFG conversion """
        if len(ss_by) == 0:
            return [[]]
        if len(ss_by) == 1:
            return [[to_cfg_combined_variable(s_from, ss_by[0], s_to)]]
        res = []
        for state in self._states:
            all_next = self._generate_all_rules(s_from, state, ss_by[:-1])
            current = to_cfg_combined_variable(state, ss_by[-1], s_to)
            for next_l in all_next:
                next_l.append(current)
            res += all_next
        return res

    def to_cfg(self) -> "cfg.CFG":
        """ Turns this PDA on empty stack accepting into a CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The equivalent CFG
        """
        from pyformlang import cfg
        start = cfg.Variable("#StartCFG#")
        productions = set()
        for state in self._states:
            productions.add(cfg.Production(start,
                                           [to_cfg_combined_variable(self._start_state,
                                                                     self._start_stack_symbol,
                                                                     state)]))
        states = self._states
        for transition in self._transition_function:
            for state in states:
                if len(transition[1][1]) == 0 and state != transition[1][0]:
                    continue
                head = to_cfg_combined_variable(transition[0][0],
                                                transition[0][2],
                                                state)
                bodies = self._generate_all_rules(transition[1][0],
                                                  state,
                                                  transition[1][1])
                if transition[0][1] != Epsilon():
                    to_prepend = cfg.Terminal(transition[0][1].get_value())
                    for i, body in enumerate(bodies):
                        bodies[i] = [to_prepend] + body
                for body in bodies:
                    productions.add(cfg.Production(head, body))
        return cfg.CFG(start_symbol=start, productions=productions)

    def intersection(self, other:Any) -> "PDA":
        """ Gets the intersection of the current PDA with something else

        Parameters
        ----------
        other : any
            The other part of the intersection

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The pda resulting of the intersection

        Raises
        ----------
        TODO
        """
        if isinstance(other, Regex):
            other = other.to_epsilon_nfa().to_deterministic()
        start_state_other = other.get_start_states()
        if len(start_state_other) == 0:
            return PDA()
        start_state_other = list(start_state_other)[0]
        final_state_other = other.get_final_states()
        start = to_pda_combined_state(self._start_state,
                                      start_state_other)
        pda = PDA(start_state=start,
                  start_stack_symbol=self._start_stack_symbol)
        symbols = self._input_symbols.copy()
        symbols.add(Epsilon())
        to_process=[(self._start_state, start_state_other)]
        processed={(self._start_state, start_state_other)}
        while to_process:
            state_in, state_dfa = to_process.pop()
            if state_in in self._final_states and state_dfa in final_state_other:
                pda.add_final_state(to_pda_combined_state(state_in, state_dfa))
            for symbol in symbols:
                if symbol == Epsilon():
                    symbol_dfa = finite_automaton.Epsilon()
                else:
                    symbol_dfa = finite_automaton.Symbol(symbol.get_value())
                if symbol == Epsilon():
                    next_states_dfa = [state_dfa]
                else:
                    next_states_dfa = other(state_dfa, symbol_dfa)
                if len(next_states_dfa) == 0:
                    continue
                for stack_symbol in self._stack_alphabet:
                    next_states_self = self._transition_function(state_in,
                                                                 symbol,
                                                                 stack_symbol)
                    for next_state, next_stack in next_states_self:
                        for next_state_dfa in next_states_dfa:
                            pda.add_transition(to_pda_combined_state(state_in,
                                                                     state_dfa),
                                               symbol,
                                               stack_symbol,
                                               to_pda_combined_state(next_state,
                                                                     next_state_dfa),
                                               next_stack)
                            if (next_state, next_state_dfa) not in processed:
                                to_process.append((next_state, next_state_dfa))
                                processed.add((next_state, next_state_dfa))
        return pda


def to_pda_combined_state(state_pda, state_other):
    """ To PDA state in the intersection function """
    return State(state_pda.get_value() + "###" + state_other.get_value())

def to_cfg_combined_variable(state0, stack_symbol, state1):
    """ Convertion used in the to_pda method """
    from pyformlang import cfg
    return cfg.Variable(str(state0.get_value()) + "#!#" +
                        str(stack_symbol.get_value()) + "#!#" +
                        str(state1.get_value()))

def get_next_free(prefix, type_generating, to_check):
    """ Get free next state or symbol """
    idx = 0
    new_var = type_generating(prefix)
    while new_var in to_check:
        new_var = type_generating(prefix + str(idx))
        idx += 1
    return new_var
