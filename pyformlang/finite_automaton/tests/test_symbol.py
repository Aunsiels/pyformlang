from pyformlang.finite_automaton import Symbol

def test_can_create():
    assert Symbol("") is not None
    assert Symbol(1) is not None

def test_repr():
    s1 = Symbol("ABC")
    assert str(s1) == "ABC"
    s2 = Symbol(1)
    assert str(s2) == "1"

def test_eq():
    s1 = Symbol("ABC")
    s2 = Symbol(1)
    s3 = Symbol("ABC")
    assert s1 == s3
    assert s2 != s3
    assert s1 != s2

def test_hash():
    s1 = hash(Symbol("ABC"))
    s2 = hash(Symbol(1))
    s3 = hash(Symbol("ABC"))
    assert isinstance(s1, int)
    assert s1 == s3
    assert s2 != s3
    assert s1 != s2
