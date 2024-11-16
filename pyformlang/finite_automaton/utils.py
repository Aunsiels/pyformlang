""" Utility for finite automata """

from typing import Dict, List, AbstractSet, Iterable, Optional, Hashable
from numpy import empty

from .state import State
from .symbol import Symbol
from .epsilon import Epsilon


def to_state(given: Hashable) -> State:
    """ Transforms the input into a state

    Parameters
    ----------
    given : any
        What we want to transform
    """
    if isinstance(given, State):
        return given
    return State(given)


def to_symbol(given: Hashable) -> Symbol:
    """ Transforms the input into a symbol

    Parameters
    ----------
    given : any
        What we want to transform
    """
    if isinstance(given, Symbol):
        return given
    if given in ("epsilon", "ɛ"):
        return Epsilon()
    return Symbol(given)


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
        if state is not None:
            values.append(str(state.value))
        else:
            values.append("TRASH")
    values = sorted(values)
    return State(";".join(values))


class PreviousTransitions:
    """
    Previous transitions for deterministic automata
    minimization algorithm.
    """

    def __init__(self,
                 states: AbstractSet[State],
                 symbols: AbstractSet[Symbol]) -> None:
        self._to_index_state: Dict[State, int] = {}
        for i, state in enumerate(states):
            self._to_index_state[state] = i + 1
        self._to_index_symbol: Dict[Symbol, int] = {}
        for i, symbol in enumerate(symbols):
            self._to_index_symbol[symbol] = i
        self._conversion = empty((len(states) + 1, len(symbols)),
                                 dtype=State)

    def add(self,
            next0: Optional[State],
            symbol: Symbol,
            state: State) -> None:
        """ Internal """
        i_next0 = self._to_index_state[next0] if next0 else 0
        i_symbol = self._to_index_symbol[symbol]
        if self._conversion[i_next0, i_symbol] is None:
            self._conversion[i_next0, i_symbol] = [state]
        else:
            self._conversion[i_next0, i_symbol].append(state)

    def get(self, next0: Optional[State], symbol: Symbol) -> List[State]:
        """ Internal """
        i_next0 = self._to_index_state[next0] if next0 else 0
        i_symbol = self._to_index_symbol[symbol]
        return self._conversion[i_next0, i_symbol] or []
