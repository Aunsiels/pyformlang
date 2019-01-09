from pyformlang.finite_automaton import DeterministicFiniteAutomaton

def test_can_create():
    assert DeterministicFiniteAutomaton(None, None, None, None, None) \
        is not None
