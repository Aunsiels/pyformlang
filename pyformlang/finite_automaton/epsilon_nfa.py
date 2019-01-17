"""
Nondeterminsitic Automaton with epsilon transitions
"""

from typing import Set, Iterable, AbstractSet

from pyformlang import finite_automaton, regular_expression

from .epsilon import Epsilon
from .state import State
from .symbol import Symbol
from .nondeterministic_transition_function import NondeterministicTransitionFunction


class EpsilonNFA(object):
    """ Represents an epsilon NFA


    Parameters
    ----------
    states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`, optional
        A finite set of input symbols
    transition_function : :class:`~pyformlang.finite_automaton.NondeterministicTransitionFunction`\
, optional
        Takes as arguments a state and an input symbol and returns a state.
    start_state : :class:`~pyformlang.finite_automaton.State`, optional
        A start state, element of states
    final_states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A set of final or accepting states. It is a subset of states.

    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 states: AbstractSet[State] = None,
                 input_symbols: AbstractSet[Symbol] = None,
                 transition_function: NondeterministicTransitionFunction = None,
                 start_state: AbstractSet[State] = None,
                 final_states: AbstractSet[State] = None):
        self._states = states or set()
        self._input_symbols = input_symbols or set()
        self._transition_function = transition_function or \
            NondeterministicTransitionFunction()
        self._start_state = start_state or set()
        self._final_states = final_states or set()
        for state in self._final_states:
            if state is not None and state not in self._states:
                self._states.add(start_state)
        for state in self._start_state:
            if state is not None and state not in self._states:
                self._states.add(state)

    def add_transition(self, s_from: State, symb_by: Symbol, s_to: State) -> int:
        """ Adds a transition to the nfa

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        symb_by : :class:`~pyformlang.finite_automaton.Symbol`
            The transition symbol
        s_to : :class:`~pyformlang.finite_automaton.State`
            The destination state


        Returns
        --------
        done : int
            Always 1

        Raises
        --------
        DuplicateTransitionError
            If the transition already exists
        """
        self._states.add(s_from)
        self._states.add(s_to)
        if symb_by != Epsilon():
            self._input_symbols.add(symb_by)
        return self._transition_function.add_transition(s_from, symb_by, s_to)

    def remove_transition(self, s_from: State, symb_by: Symbol, s_to: State) -> int:
        """ Remove a transition of the nfa

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        symb_by : :class:`~pyformlang.finite_automaton.Symbol`
            The transition symbol
        s_to : :class:`~pyformlang.finite_automaton.State`
            The destination state


        Returns
        --------
        done : int
            1 if the transition existed, 0 otherwise
        """
        return self._transition_function.remove_transition(s_from,
                                                           symb_by,
                                                           s_to)

    def get_number_states(self) -> int:
        """ Gives the total number of states

        Returns
        ----------
        number_states : int
            The number of states
        """
        return len(self._states)

    def get_number_transitions(self) -> int:
        """ Gives the number of transitions

        Returns
        ----------
        n_transitions : int
            The number of deterministic transitions

        """
        return self._transition_function.get_number_transitions()

    def get_number_symbols(self) -> int:
        """ Gives the total number of symbols

        Returns
        ----------
        number_symbols : int
            The number of symbols
        """
        return len(self._input_symbols)

    def get_number_final_states(self) -> int:
        """ Gives the number of final states

        Returns
        ----------
        number_final_states : int
            The number of final states
        """
        return len(self._final_states)

    def add_start_state(self, state: State) -> int:
        """ Set an initial state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The new initial state

        Returns
        ----------
        done : int
            1 is correctly added
        """
        self._start_state.add(state)
        self._states.add(state)
        return 1

    def remove_start_state(self, state: State) -> int:
        """ remove an initial state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The new initial state

        Returns
        ----------
        done : int
            1 is correctly added
        """
        if state in self._start_state:
            self._start_state.remove(state)
            return 1
        return 0

    def add_final_state(self, state: State) -> int:
        """ Adds a new final state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            A new final state

        Returns
        ----------
        done : int
            1 is correctly added
        """
        self._final_states.add(state)
        self._states.add(state)
        return 1

    def remove_final_state(self, state: State) -> int:
        """ Remove a final state

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            A final state to remove

        Returns
        ----------
        done : int
            0 if it was not a final state, 1 otherwise
        """
        if self.is_final_state(state):
            self._final_states.remove(state)
            return 1
        return 0

    def is_final_state(self, state: State) -> bool:
        """ Checks if a state is final

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The state to check

        Returns
        ----------
        is_final : bool
            Whether the state is final or not
        """
        return state in self._final_states

    def _get_next_states_iterable(self,
                                  current_states: Iterable[State],
                                  symbol: Symbol) \
            -> Set[State]:
        """ Gives the set of next states, starting from a set of states

        Parameters
        ----------
        current_states : iterable of :class:`~pyformlang.finite_automaton.State`
            The considered list of states
        symbol : Symbol
            The symbol of the link

        Returns
        ----------
        next_states : set of :class:`~pyformlang.finite_automaton.State`
            The next of resulting states
        """
        next_states = set()
        for current_state in current_states:
            next_states_temp = self._transition_function(current_state,
                                                         symbol)
            next_states = next_states.union(next_states_temp)
        return next_states

    def accepts(self, word: Iterable[Symbol]) -> bool:
        """ Checks whether the epsilon nfa accepts a given word

        Parameters
        ----------
        word : iterable of :class:`~pyformlang.finite_automaton.Symbol`
            A sequence of input symbols

        Returns
        ----------
        is_accepted : bool
            Whether the word is accepted or not
        """
        current_states = self.eclose_iterable(self._start_state)
        for symbol in word:
            if symbol == Epsilon():
                continue
            next_states = self._get_next_states_iterable(current_states, symbol)
            current_states = self.eclose_iterable(next_states)
        return any([self.is_final_state(x) for x in current_states])

    def eclose_iterable(self, states: Iterable[State]) -> Set[State]:
        """ Compute the epsilon closure of a collection of states

        Parameters
        ----------
        state : iterable of :class:`~pyformlang.finite_automaton.State`
            The source states

        Returns
        ---------
        states : set of :class:`~pyformlang.finite_automaton.State`
            The epsilon closure of the source state
        """
        res = set()
        for state in states:
            res = res.union(self.eclose(state))
        return res

    def eclose(self, state: State) -> Set[State]:
        """ Compute the epsilon closure of a state

        Parameters
        ----------
        state : :class:`~pyformlang.finite_automaton.State`
            The source state

        Returns
        ---------
        states : set of :class:`~pyformlang.finite_automaton.State`
            The epsilon closure of the source state
        """
        to_process = [state]
        processed = {state}
        while to_process:
            current = to_process.pop()
            connected = self._transition_function(current, Epsilon())
            for conn_state in connected:
                if conn_state not in processed:
                    processed.add(conn_state)
                    to_process.append(conn_state)
        return processed

    def is_deterministic(self) -> bool:
        """ Checks whether an automaton is deterministic

        Returns
        ----------
        is_deterministic : bool
           Whether the automaton is deterministic
        """
        return len(self._start_state) <= 1 and \
            self._transition_function.is_deterministic() and \
            all([{x} == self.eclose(x) for x in self._states])

    def _to_deterministic_internal(self, eclose: bool) -> "DeterministicFiniteAutomaton":
        """ Transforms the epsilon-nfa into a dfa

        Parameters
        ----------
        eclose : bool
            Whether to use the epsilon closure or not

        Returns
        ----------
        dfa : :class:`~pyformlang.deterministic_finite_automaton.DeterministicFiniteAutomaton`
            A dfa equivalent to the current nfa
        """
        dfa = finite_automaton.DeterministicFiniteAutomaton()
        # Add Eclose
        if eclose:
            start_eclose = self.eclose_iterable(self._start_state)
        else:
            start_eclose = self._start_state
        start_state = to_single_state(start_eclose)
        dfa.add_start_state(start_state)
        to_process = [start_eclose]
        processed = {start_state}
        while to_process:
            current = to_process.pop()
            s_from = to_single_state(current)
            for symb in self._input_symbols:
                all_trans = [self._transition_function(x, symb) for x in current]
                state = set()
                for trans in all_trans:
                    state = state.union(trans)
                if not state:
                    continue
                # Eclose added
                if eclose:
                    state = self.eclose_iterable(state)
                state_merged = to_single_state(state)
                dfa.add_transition(s_from, symb, state_merged)
                if state_merged not in processed:
                    processed.add(state_merged)
                    to_process.append(state)
            for state in current:
                if state in self._final_states:
                    dfa.add_final_state(s_from)
        return dfa

    def to_deterministic(self) -> "DeterministicFiniteAutomaton":
        """ Transforms the epsilon-nfa into a dfa

        Returns
        ----------
        dfa : :class:`~pyformlang.deterministic_finite_automaton.DeterministicFiniteAutomaton`
            A dfa equivalent to the current nfa
        """
        return self._to_deterministic_internal(True)

    def copy(self) -> "EpsilonNFA":
        """ Copies the current Epsilon NFA

        Returns
        ----------
        enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
            A copy of the current Epsilon NFA
        """
        enfa = EpsilonNFA()
        for start in self._start_state:
            enfa.add_start_state(start)
        for final in self._final_states:
            enfa.add_final_state(final)
        for state in self._states:
            for symbol in self._input_symbols:
                states = self._transition_function(state, symbol)
                for state_to in states:
                    enfa.add_transition(state, symbol, state_to)
            states = self._transition_function(state, Epsilon())
            for state_to in states:
                enfa.add_transition(state, Epsilon(), state_to)
        return enfa

    def to_regex(self) -> regular_expression.Regex:
        """ Tranforms the EpsilonNFA to a regular expression

        Returns
        ----------
        regex : :class:`~pyformlang.regular_expression.Regex`
            A regular expression equivalent to the current Epsilon NFA
        """
        enfas = [self.copy() for _ in self._final_states]
        for i in range(len(self._final_states)):
            for j in range(len(self._final_states)):
                if i != j:
                    enfas[j].remove_final_state(self._final_states[i])
        for enfa in enfas:
            enfa.create_or_transitions()

    def remove_state(self, state):
        """ Removes a given state from the epsilon NFA

        CAREFUL: This method modifies the current automaton, for internal usage
        only!

        The function create_or_transitions is supposed to be called before
        calling this function

        Parameters
        ----------
        state : :class:`~pyformlang.finite_automaton.State`
            The state to remove

        """
        # First compute all endings
        out_transitions = dict()
        for symbol in self._input_symbols:
            out_states = self._transition_function(state, symbol).copy()
            for out_state in out_states:
                out_transitions[out_state] = symbol.get_value()
                self.remove_transition(state, symbol, out_state)
        if state in out_transitions:
            to_itself = "(" + out_transitions[state] + ")*"
            del out_transitions[state]
            for out_state in out_transitions:
                out_transitions[out_state] = to_itself + "." + out_transitions[out_state]
        input_symbols = self._input_symbols.copy()
        for in_state in self._states:
            if in_state == state:
                continue
            for symbol in input_symbols:
                out_states = self._transition_function(in_state, symbol)
                if state not in out_states:
                    continue
                symbol_str = "(" + symbol.get_value() + ")"
                self.remove_transition(in_state, symbol, state)
                for out_state in out_transitions:
                    new_symbol = Symbol(symbol_str + "." + out_transitions[out_state])
                    self.add_transition(in_state, new_symbol, out_state)
        self._states.remove(state)
        # We make sure the automaton has the good structure
        self.create_or_transitions()


    def create_or_transitions(self):
        """ Creates a OR transition instead of several connections

        CAREFUL: This method modifies the automaton and is designed for internal
        use only!
        """
        for state in self._states:
            new_transitions = dict()
            input_symbols = self._input_symbols.copy()
            for symbol in input_symbols:
                out_states = self._transition_function(state, symbol)
                out_states = out_states.copy()
                symbol_str = symbol.get_value()
                for out_state in out_states:
                    self.remove_transition(state, symbol, out_state)
                    base = new_transitions.setdefault(out_state, "")
                    if "+" in symbol_str:
                        symbol_str = "(" + symbol_str + ")"
                    new_transitions[out_state] = base + "+" + symbol_str
            for out_state in new_transitions:
                self.add_transition(state,
                                    Symbol(new_transitions[out_state]),
                                    out_state)



def to_single_state(l_states: Iterable[State]) -> State:
    """ Merge a list of states

    Parameters
    ----------
    l_states : list of :class:`~pyformlang.finite_automaton.State`
        A list of states

    Returns
    ----------
    state : :class:`~pyformlang.finite_automaton.State`
        The merged state
    """
    values = []
    for state in l_states:
        values.append(str(state.get_value()))
    values = sorted(values)
    return State("; ".join(values))
