"""
General transition function representation
"""

from typing import Dict, Set, Tuple, Iterable, Iterator
from abc import abstractmethod

from .state import State
from .symbol import Symbol


class TransitionFunction(Iterable[Tuple[State, Symbol, State]]):
    """ General transition function representation """

    @abstractmethod
    def add_transition(self,
                       s_from: State,
                       symb_by: Symbol,
                       s_to: State) -> int:
        """ Adds a new transition to the function """
        raise NotImplementedError

    @abstractmethod
    def remove_transition(self,
                          s_from: State,
                          symb_by: Symbol,
                          s_to: State) -> int:
        """ Removes a transition from the function """
        raise NotImplementedError

    @abstractmethod
    def get_number_transitions(self) -> int:
        """ Gives the number of transitions described by the function """
        raise NotImplementedError

    def __len__(self) -> int:
        return self.get_number_transitions()

    @abstractmethod
    def __call__(self, s_from: State, symb_by: Symbol) -> Set[State]:
        """
        Calls the transition function
        as a real function for given state and symbol.
        """
        raise NotImplementedError

    def __contains__(self, transition: Tuple[State, Symbol, State]) -> bool:
        """ Whether the given transition is present in the function """
        s_from, symb_by, s_to = transition
        return s_to in self(s_from, symb_by)

    @abstractmethod
    def get_transitions_from(self, s_from: State) \
            -> Iterable[Tuple[Symbol, State]]:
        """ Gets transitions from the given state """
        raise NotImplementedError

    def get_next_states_from(self, s_from: State) -> Set[State]:
        """ Gets a set of states that are next to the given one """
        next_states = set()
        for _, next_state in self.get_transitions_from(s_from):
            next_states.add(next_state)
        return next_states

    @abstractmethod
    def get_edges(self) -> Iterable[Tuple[State, Symbol, State]]:
        """ Gets the edges """
        raise NotImplementedError

    def __iter__(self) -> Iterator[Tuple[State, Symbol, State]]:
        yield from self.get_edges()

    @abstractmethod
    def to_dict(self) -> Dict[State, Dict[Symbol, Set[State]]]:
        """ Gets the dictionary representation of the transition function """
        raise NotImplementedError

    @abstractmethod
    def is_deterministic(self) -> bool:
        """ Whether the transition function is deterministic """
        raise NotImplementedError
