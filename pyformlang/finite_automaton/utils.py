""" Utility for finite automata """

from typing import Iterable, Hashable

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
