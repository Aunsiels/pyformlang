class DeterministicFiniteAutomaton(object):
    """ Represents a deterministic finite automaton

    This class represents a deterministic finite automaton.

    Parameters
    ----------
    states : set of :class:`~pyformlang.finite_automaton.State`.
        A finite set of states
    input_symbols : set of :class:`~pyformlang.finite_automaton.Symbol`
        A finite set of input symbols
    transition_function : :class:`~pyformlang.finite_automaton.TransitionFunction`
        Takes as arguments a state and an input symbol and returns a state.
    start_state : :class:`~pyformlang.finite_automaton.State`
        A start state, element of states
    final_states : set of :class:`~pyformlang.finite_automaton.State`
        A set of final or accepting states. It is a subset of states.

    """

    def __init__(self, states, input_symbols, transition_function,
                 start_state, final_states):
        self._state = states
        self._input_symbols = input_symbols
        self._transition_function = transition_function
        self._start_state = start_state
        self._final_states = final_states
