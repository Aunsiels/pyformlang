=====
Usage
=====

Regular expression
==================

Pyformlang's Regex class implements the operators of textbooks, which deviate
slightly
from the operators in Python. For a representation closer to Python one,
please use the PythonRegex class.

* The concatenation can be represented either by a space or a dot (.)
* The union is represented either by | or +
* The Kleene star is represented by *
* The epsilon symbol can either be *epsilon* or $

It is also possible to use parentheses. All symbols except the space, .,
\|, +, \*, (, ), epsilon and $ can be part of the alphabet.
All other common regex operators (such as []) are syntactic sugar that can be
reduced to the previous operators. The class PythonRegex implements some of
them natively. Another main difference is that the alphabet is not reduced to
single characters as it is the case in Python. For example, *python* is a
single symbol in Pyformlang, whereas it is the concatenation of six symbols
in regular Python.

All special characters except epsilon can be escaped with a backslash (\
double backslash \\\\ in strings).

.. code-block:: python

    from pyformlang.regular_expression import Regex

    regex = Regex("abc|d")
    # Check if the symbol "abc" is accepted
    regex.accepts(["abc"])  # True
    # Check if the word composed of the symbols
    # "a", "b" and "c" is accepted
    regex.accepts(["a", "b", "c"])  # False
    # Check if the symbol "d" is accepted
    regex.accepts(["d"])  # True

    regex1 = Regex("a b")
    regex_concat = regex.concatenate(regex1)
    regex_concat.accepts(["d", "a", "b"])  # True

    print(regex_concat.get_tree_str())
    # Operator(Concatenation)
    #  Operator(Union)
    #   Symbol(abc)
    #   Symbol(d)
    #  Operator(Concatenation)
    #   Symbol(a)
    #   Symbol(b)

    # Give the equivalent finite-state automaton
    regex_concat.to_epsilon_nfa()

    # Python regular expressions wrapper
    from pyformlang.regular_expression import PythonRegex

    p_regex = PythonRegex("a+[cd]")
    p_regex.accepts(["a", "a", "d"])  # True
    # As the alphabet is composed of single characters, one
    # could also write
    p_regex.accepts("aad")  # True
    p_regex.accepts(["d"])  # False

Finite Automata
===============

pyformlang contains several finite automata, all of them being equivalent in the languages they can describe. In general, the states have to be represented by a *pyformlang.finite_automaton.State* object and the symbols by a *pyformlang.finite_automaton.Symbol*. When the class is not ambiguous, raw values can also be used. In addition, epsilon transitions are elements of the class: *pyformlang.finite_automaton.Epsilon*.

Deterministic Automata
----------------------

These represent deterministic automata, i.e. with only one possible next state possible at each stage and no epsilon transitions.

.. code-block:: python

    from pyformlang.finite_automaton import DeterministicFiniteAutomaton
    from pyformlang.finite_automaton import State
    from pyformlang.finite_automaton import Symbol

    # Declaration of the DFA
    dfa = DeterministicFiniteAutomaton()

    # Creation of the states
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    state3 = State(3)

    # Creation of the symbols
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")
    symb_d = Symbol("d")

    # Add a start state
    dfa.add_start_state(state0)

    # Add two final states
    dfa.add_final_state(state2)
    dfa.add_final_state(state3)

    # Create transitions
    dfa.add_transition(state0, symb_a, state1)
    dfa.add_transition(state1, symb_b, state1)
    dfa.add_transition(state1, symb_c, state2)
    dfa.add_transition(state1, symb_d, state3)

    # Check if a word is accepted
    dfa.accepts([symb_a, symb_b, symb_c])

Non Deterministic Automata
--------------------------

The representation of non deterministic automata, i.e. automata with possibly several next states at each stage but no epsilon transitions.

.. code-block:: python

    from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
    from pyformlang.finite_automaton import State
    from pyformlang.finite_automaton import Symbol

    # Definition of the NFA
    nfa = NondeterministicFiniteAutomaton()

    # Declare the states
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    state3 = State(3)
    state4 = State(4)

    # Declare the symbols
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")
    symb_d = Symbol("d")

    # Add a start state
    nfa.add_start_state(state0)
    # Add a final state
    nfa.add_final_state(state4)
    nfa.add_final_state(state3)
    # Add the transitions
    nfa.add_transition(state0, symb_a, state1)
    nfa.add_transition(state1, symb_b, state1)
    nfa.add_transition(state1, symb_c, state2)
    nfa.add_transition(state1, symb_d, state3)
    nfa.add_transition(state1, symb_c, state4)
    nfa.add_transition(state1, symb_b, state4)

    # Check if a word is accepted
    nfa.accepts([symb_a, symb_b, symb_c])

    # Check if a NFA is deterministic
    nfa.is_deterministic() # False

    # Get the equivalent deterministic automaton
    dfa = nfa.to_deterministic()

Epsilon Non Deterministic Automata
----------------------------------

It represents a non deterministic automaton where epsilon transitions are allowed.

.. code-block:: python

    from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon

    # Declaration of the symbols and the states
    epsilon = Epsilon()
    plus = Symbol("+")
    minus = Symbol("-")
    point = Symbol(".")
    digits = [Symbol(x) for x in range(10)]
    states = [State("q" + str(x)) for x in range(6)]

    # Creattion of the Epsilon NFA
    enfa = EpsilonNFA()
    enfa.add_start_state(states[0])
    enfa.add_final_state(states[5])
    enfa.add_transition(states[0], epsilon, states[1])
    enfa.add_transition(states[0], plus, states[1])
    enfa.add_transition(states[0], minus, states[1])
    for digit in digits:
        enfa.add_transition(states[1], digit, states[1])
        enfa.add_transition(states[1], digit, states[4])
        enfa.add_transition(states[2], digit, states[3])
        enfa.add_transition(states[3], digit, states[3])
    enfa.add_transition(states[1], point, states[2])
    enfa.add_transition(states[4], point, states[3])
    enfa.add_transition(states[3], epsilon, states[5])

    # Checks if a word is accepted
    enfa.accepts([plus, digits[1], point, digits[9]])

Regex and Finite Automaton
==========================

As regex and finite automaton are equivalent, one can turn one into the other.

.. code-block:: python

    from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon

    enfa = EpsilonNFA()
    state0 = State(0)
    state1 = State(1)
    symb_a = Symbol("0")
    symb_b = Symbol("1")
    enfa.add_start_state(state0)
    enfa.add_final_state(state1)
    enfa.add_transition(state0, symb_a, state0)
    enfa.add_transition(state1, symb_b, state0)
    enfa.add_transition(state1, symb_b, state1)

    # Turn a finite automaton into a regex...
    regex = enfa.to_regex()
    # And turn it back into an epsilon non deterministic automaton
    enfa2 = regex.to_epsilon_nfa()

Context-Free Grammar
====================

We represent here context-free grammars. Like finite automata, one needs to use the classes *pyformlang.cfg.Variable* and *pyformlang.cfg.Terminal* to represent variables and terminals. The productions need to be represented as *pyformlang.cfg.Production*. In addition, epsilon terminals are members of *pyformlang.cfg.Epsilon*.

.. code-block:: python

    from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon

    # Creation of variables
    var_useless = Variable("USELESS")
    var_S = Variable("S")
    var_B = Variable("B")

    # Creation of terminals
    ter_a = Terminal("a")
    ter_b = Terminal("b")
    ter_c = Terminal("c")

    # Creation of productions
    p0 = Production(var_S, [ter_a, var_S, var_B])
    p1 = Production(var_useless, [ter_a, var_S, var_B])
    p2 = Production(var_S, [var_useless])
    p4 = Production(var_B, [ter_b])
    p5 = Production(var_useless, [])

    # Creation of the CFG
    cfg = CFG({var_useless, var_S}, {ter_a, ter_b}, var_S, {p0, p1, p2, p4, p5})

    # Check for containment
    cfg.contains([Epsilon()])
    cfg.contains([ter_a, ter_b])

Push-Down Automata
==================

For a Push-Down Automata, there are there objects: *pyformlang.pda.State* which represents a state, *pyformlang.pda.Symbol* which represents a symbol and *pyformlang.pda.StackSymbol* which represents a stack symbol.

PDA can either accept by final state or by empty stack. Function are provided to transform one kind into the other.

.. code-block:: python

    from pyformlang.pda import PDA, State, StackSymbol, Symbol, Epsilon

    # Declare states
    q = State("#STARTTOFINAL#")
    q0 = State("q0")

    # Declare symbols
    e = Symbol("e")
    i = Symbol("i")

    # Declare stack symbols
    Z = StackSymbol("Z")
    Z0 = StackSymbol("Z0")

    # Create the PDA
    pda = PDA(states={q, q0},
              input_symbols={i, e},
              stack_alphabet={Z, Z0},
              start_state=q,
              start_stack_symbol=Z0,
              final_states={q0})

    # Add transitions
    pda.add_transition(q, i, Z, q, (Z, Z))
    pda.add_transition(q, i, Z0, q, (Z, Z0))
    pda.add_transition(q, e, Z, q, [])
    pda.add_transition(q, Epsilon(), Z0, q0, [])

    # Transformation to a PDA accepting by empty stack
    pda_empty_stack = pda.to_empty_stack()
    # Transformation to a PDA accepting by final state
    pda_final_state = pda_empty_stack.to_final_state()

CFG and PDA
===========

As CFG and PDA are equivalent, one can turn one into the other, but needs to be careful about whether the PDA accepts on empty stack and final state. The conversions between CFG and PDA are done when the PDA is accepting by empty stack

.. code-block:: python

    from pyformlang.cfg import Production, Variable, Terminal, CFG

    ter_a = Terminal("a")
    ter_b = Terminal("b")
    ter_c = Terminal("c")
    var_S = Variable("S")
    productions = {Production(var_S, [ter_a, var_S, ter_b]),
                   Production(var_S, [ter_c])}
    cfg = CFG(productions=productions, start_symbol=var_S)

    # Convert into a PDA accepting by final state
    pda_empty_stack = cfg.to_pda()
    # Go to final state
    pda_final_state = pda_empty_stack.to_final_state()
    # Go back to empty stack, necessary to transform into a CFG
    pda_empty_stack = pda_final_state.to_empty_stack()
    # Transform the PDA into a CFG
    cfg = pda_empty_stack.to_cfg()

Indexed Grammars
================

Indexed grammars are grammars which have a stack which can be duplicated. In an indexed grammar, rules can take 4 forms (sigma is the stack):

* *EndRule*: This simply turns a Variable into a terminal, for example A[sigma]->a
* *ProductionRule*: We push something on the stack, for example A[sigma]->B[f sigma]
* *ConsumptionRule*: We consume something from the stack, for example A[f sigma] -> C[sigma]
* *DuplicationRule*: We duplicate the stack, for example A[sigma] -> B[sigma] C[sigma]

.. code-block:: python

    from pyformlang.indexed_grammar import Rules
    from pyformlang.indexed_grammar import ConsumptionRule
    from pyformlang.indexed_grammar import EndRule
    from pyformlang.indexed_grammar import ProductionRule
    from pyformlang.indexed_grammar import DuplicationRule
    from pyformlang.indexed_grammar import IndexedGrammar

    l_rules = []

    # Initialization rules
    l_rules.append(ProductionRule("S", "Cinit", "end"))
    l_rules.append(ProductionRule("Cinit", "C", "b"))
    l_rules.append(ConsumptionRule("end", "C", "T"))
    l_rules.append(EndRule("T", "epsilon"))

    # C[cm sigma] -> cm C[sigma]
    l_rules.append(ConsumptionRule("cm", "C", "B0"))
    l_rules.append(DuplicationRule("B0", "A0", "C"))
    l_rules.append(EndRule("A0", "cm"))

    rules = Rules(l_rules)
    i_grammar = IndexedGrammar(rules)
    self.assertTrue(i_grammar.is_empty())
