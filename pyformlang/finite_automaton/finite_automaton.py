""" A general finite automaton representation """

from typing import Set, List, Any

import networkx as nx

from .epsilon import Epsilon
from .state import State
from .symbol import Symbol


class FiniteAutomaton(object):
    """ Represents a general finite automaton


    Attributes
    ----------
    _states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A finite set of states
    _input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`, optional
        A finite set of input symbols
    _transition_function : :class:`~pyformlang.finite_automaton.NondeterministicTransitionFunction`\
, optional
        Takes as arguments a state and an input symbol and returns a state.
    _start_state : set of :class:`~pyformlang.finite_automaton.State`, optional
        A start state, element of states
    _final_states : set of :class:`~pyformlang.finite_automaton.State`, optional
        A set of final or accepting states. It is a subset of states.
    """

    def __init__(self):
        self._states = set()
        self._input_symbols = set()
        self._transition_function = None
        self._start_state = set()
        self._final_states = set()

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
        s_from = to_state(s_from)
        symb_by = to_symbol(symb_by)
        s_to = to_state(s_to)
        temp = self._transition_function.add_transition(s_from, symb_by, s_to)
        self._states.add(s_from)
        self._states.add(s_to)
        if symb_by != Epsilon():
            self._input_symbols.add(symb_by)
        return temp

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
        s_from = to_state(s_from)
        symb_by = to_symbol(symb_by)
        s_to = to_state(s_to)
        return self._transition_function.remove_transition(s_from,
                                                           symb_by,
                                                           s_to)

    @property
    def states(self):
        """ Gives the states

        Returns
        ----------
        states : set of :class:`~pyformlang.finite_automaton.State`
            The states
        """
        return self._states

    def get_number_transitions(self) -> int:
        """ Gives the number of transitions

        Returns
        ----------
        n_transitions : int
            The number of deterministic transitions

        """
        return self._transition_function.get_number_transitions()

    @property
    def symbols(self):
        return self._input_symbols

    @property
    def final_states(self):
        return self._final_states

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
        state = to_state(state)
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
        state = to_state(state)
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
        state = to_state(state)
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
        state = to_state(state)
        if self.is_final_state(state):
            self._final_states.remove(state)
            return 1
        return 0

    def __call__(self, state: State, symbol: Symbol=None) -> List[State]:
        """ Gives the states obtained after calling a symbol on a state
        Calls the transition function

        Parameters
        -----------
        state : :class:`~pyformlang.finite_automaton.State`
            The source state
        symbol : :class:`~pyformlang.finite_automaton.Symbol`
            The symbol, optional if we want all transitions

        Returns
        ----------
        states : list of :class:`~pyformlang.finite_automaton.State`
            The next states
        """
        # pylint: disable=not-callable
        state = to_state(state)
        if symbol is not None:
            symbol = to_symbol(symbol)
        return self._transition_function(state, symbol)

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
        state = to_state(state)
        return state in self._final_states

    @property
    def start_states(self):
        return self._start_state

    def add_symbol(self, symbol: Symbol):
        """ Add a symbol

        Parameters
        -----------
        symbol : :class:`~pyformlang.finite_automaton.Symbol`
            The symbol
        """
        symbol = to_symbol(symbol)
        self._input_symbols.add(symbol)

    def to_fst(self) -> "FST":
        """ Turns the finite automaton into a finite state transducer

        The transducers accepts only the words in the language of the automaton\
            and output the input word

        Returns
        ----------
        fst : :class:`~pyformlang.fst.FST`
            The equivalent FST
        """
        from pyformlang.fst import FST
        fst = FST()
        for start_state in self._start_state:
            fst.add_start_state(start_state.value)
        for final_state in self._final_states:
            fst.add_final_state(final_state.value)
        for s_from, symb_by, s_to in self._transition_function.get_edges():
            fst.add_transition(s_from.value,
                               symb_by.value,
                               s_to.value,
                               [symb_by.value])
        return fst

    def is_acyclic(self) -> bool:
        to_process = []
        for state in self._start_state:
            to_process.append((state, set()))
        while to_process:
            current, visited = to_process.pop()
            if current in visited:
                return False
            visited.add(current)
            for symbol in self._input_symbols:
                for state in self(current, symbol):
                    to_process.append((state, visited.copy()))
            # Epsilon
            for state in self(current, Epsilon()):
                to_process.append((state, visited.copy()))
        return True

    def to_networkx(self) -> nx.MultiDiGraph:
        graph = nx.MultiDiGraph()
        for state in self._states:
            graph.add_node(state.value,
                           is_start=state in self.start_states,
                           is_final=state in self.final_states)
        graph.add_nodes_from([x.value for x in self._states])
        for s_from, symbol, s_to in self._transition_function.get_edges():
            graph.add_edge(s_from.value, s_to.value, name=symbol.value)
        return graph

    @classmethod
    def from_networkx(cls, graph):
        from pyformlang.finite_automaton import EpsilonNFA
        enfa = EpsilonNFA()
        for s_from in graph:
            for s_to in graph[s_from]:
                for transition in graph[s_from][s_to].values():
                    enfa.add_transition(s_from, transition["name"], s_to)
        for node in graph.nodes:
            if graph.nodes[node].get("is_start", False):
                enfa.add_start_state(node)
            if graph.nodes[node].get("is_final", False):
                enfa.add_final_state(node)
        return enfa

    def is_equivalent_to(self, other):
        self_dfa = self.to_deterministic()
        return self_dfa.is_equivalent_to(other)

    def to_deterministic(self):
        raise NotImplementedError

    def is_deterministic(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.is_equivalent_to(other)

    def __len__(self):
        """Number of transitions"""
        return len(self._transition_function)

    def __iter__(self):
        yield from self._transition_function.get_edges()

    def to_dict(self):
        return self._transition_function.to_dict()


def to_state(given: Any) -> State:
    """ Transforms the input into a state

    Parameters
    ----------
    given : any
        What we want to transform
    """
    if given is None:
        return None
    if isinstance(given, State):
        return given
    return State(given)


def to_symbol(given: Any) -> Symbol:
    """ Transforms the input into a symbol

    Parameters
    ----------
    given : any
        What we want to transform
    """
    if isinstance(given, Symbol):
        return given
    if given == "epsilon":
        return Epsilon()
    return Symbol(given)
