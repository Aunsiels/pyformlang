from pyformlang.finite_automaton import State

def test_can_create():
    assert State("") is not None
    assert State(1) is not None

def test_repr():
    s1 = State("ABC")
    assert str(s1) == "ABC"
    s2 = State(1)
    assert str(s2) == "1"

def test_eq():
    s1 = State("ABC")
    s2 = State(1)
    s3 = State("ABC")
    assert s1 == s3
    assert s2 != s3
    assert s1 != s2

def test_hash():
    s1 = hash(State("ABC"))
    s2 = hash(State(1))
    s3 = hash(State("ABC"))
    assert isinstance(s1, int)
    assert s1 == s3
    assert s2 != s3
    assert s1 != s2
