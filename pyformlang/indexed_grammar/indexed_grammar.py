"""
Representation of an indexed grammar
"""

from typing import Any, Iterable, AbstractSet

from .duplication_rule import DuplicationRule
from .production_rule import ProductionRule
from .rules import Rules

class IndexedGrammar(object):
    """ Describes an indexed grammar.

    Parameters
    ----------
    rules : :class:`~pyformlang.indexed_grammar.Rules`
        The rules of the grammar, in reduced form put into a Rule
    start_variable : Any, optional
        The start symbol of the indexed grammar
    """

    def __init__(self,
                 rules: Rules,
                 start_variable: Any="S"):
        self.rules = rules
        self.start_variable=start_variable
        # Precompute all non-terminals
        self.non_terminals = rules.get_non_terminals()
        self.non_terminals.append(self.start_variable)
        self.non_terminals = set(self.non_terminals)
        # We cache the marked items in case of future update of the query
        self.marked = dict()
        # Initialize the marked symboles
        # Mark the identity
        for A in self.non_terminals:
            self.marked[A] = set()
            temp = frozenset({A})
            self.marked[A].add(temp)
        # Mark all end symboles
        for A in self.non_terminals:
            if exists(self.rules.get_rules(),
                      lambda x: x.is_end_rule() and x.left_term == A):
                self.marked[A].add(frozenset())

    def get_terminals(self) -> Iterable[Any]:
        """Get all the terminals in the grammar

        Returns
        ----------
        terminals : iterable of any
            The terminals used in the rules
        """
        return self.rules.get_terminals()

    def _duplication_processing(self, rule: DuplicationRule):
        """Processes a duplication rule

        Parameters
        ----------
        rule : :class:`~pyformlang.indexed_grammar.DuplicationRule`
            The duplication rule to process
        """
        was_modified = False
        need_stop = False
        right_term_marked0 = []
        for x in self.marked[rule.get_right_terms()[0]]:
            right_term_marked1 = []
            for y in self.marked[rule.get_right_terms()[1]]:
                if x <= y:
                    temp = y
                elif y <= x:
                    temp = x
                else:
                    temp = x.union(y)
                # Check if it was marked before
                if temp not in self.marked[rule.left_term]:
                    was_modified = True
                    if rule.left_term == rule.get_right_terms()[0]:
                        right_term_marked0.append(temp)
                    elif rule.left_term == rule.get_right_terms()[1]:
                        right_term_marked1.append(temp)
                    else:
                        self.marked[rule.left_term].add(temp)
                    # Stop condition, no need to continuer
                    if rule.left_term == self.start_variable and len(temp) == 0:
                        need_stop = True
            for temp in right_term_marked1:
                self.marked[rule.get_right_terms()[1]].add(temp)
        for temp in right_term_marked0:
            self.marked[rule.get_right_terms()[0]].add(temp)

        return (was_modified, need_stop)

    def _production_process(self, rule: ProductionRule):
        """Processes a production rule

        Parameters
        ----------
        rule : :class:`~pyformlang.indexed_grammar.ProductionRule`
            The production rule to process
        """
        was_modified = False
        # f_rules contains the consumption rules associated with
        # the current production symbol
        f_rules = self.rules.get_consumption_rules().setdefault(
            rule.get_production(), [])
        # l_rules contains the left symbol plus what is marked on
        # the right side
        l_temp = [(x.left_term,
                  self.marked[x.get_right()]) for x in f_rules]
        marked_symbols = [x.left_term for x in f_rules]
        # Process all combinations of consumption rule
        was_modified |= addrec_bis(l_temp,
                                   self.marked[rule.left_term],
                                   self.marked[rule.get_right_term()])
        # End condition
        if frozenset() in self.marked[self.start_variable]:
            return (was_modified, True)
        # Is it useful?
        if rule.get_right_term() in marked_symbols:
            for s in l_temp:
                if rule.get_right_term() == s[0]:
                    for sc in s[1]:
                        if sc not in\
                                self.marked[rule.left_term]:
                            was_modified = True
                            self.marked[rule.left_term].add(sc)
                            if rule.left_term == self.start_variable and len(sc) == 0:
                                return (was_modified, True)
        # Edge case
        if frozenset() in self.marked[rule.get_right_term()]:
            if frozenset() not in self.marked[rule.left_term]:
                was_modified = True
                self.marked[rule.left_term].add(frozenset())
        return (was_modified, False)

    def is_empty(self) -> bool:
        """Checks whether the grammar generates a word or not

        Returns
        ----------
        is_empty : bool
            Whether the grammar is empty or not
        """
        # To know when no more modification are done
        was_modified = True
        while was_modified:
            was_modified = False
            for rule in self.rules.get_rules():
                # If we have a duplication rule, we mark all combinations of
                # the sets marked on the right side for the symbole on the left
                # side
                if rule.is_duplication():
                    dup_res = self._duplication_processing(rule)
                    was_modified |= dup_res[0]
                    if dup_res[1]:
                        return False
                elif rule.is_production():
                    prod_res = self._production_process(rule)
                    if prod_res[1]:
                        return False
                    was_modified |= prod_res[0]
        if frozenset() in self.marked[self.start_variable]:
            return False
        return True

    def get_reachable_non_terminals(self) -> AbstractSet[Any]:
        """ Get the reachable symbols

        Returns
        ----------
        reachables : set of any
            The reachable symbols from the start state
        """
        # Preprocess
        reachable_from = dict()
        consumption_rules = self.rules.get_consumption_rules()
        for rule in self.rules.get_rules():
            if rule.is_duplication():
                left = rule.left_term
                right0 = rule.get_right_terms()[0]
                right1 = rule.get_right_terms()[1]
                if left in reachable_from:
                    reachable_from[left].add(right0)
                    reachable_from[left].add(right1)
                else:
                    reachable_from[left] = {right0, right1}
            if rule.is_production():
                left = rule.left_term
                right = rule.get_right_term()
                if left in reachable_from:
                    reachable_from[left].add(right)
                else:
                    reachable_from[left] = {right}
        for key in consumption_rules:
            for rule in consumption_rules[key]:
                left = rule.left_term
                right = rule.get_right()
                if left in reachable_from:
                    reachable_from[left].add(right)
                else:
                    reachable_from[left] = {right}
        # Processing
        to_process = [self.start_variable]
        reachables = {self.start_variable}
        while to_process:
            current = to_process.pop()
            for symbol in reachable_from.get(current, []):
                if symbol not in reachables:
                    reachables.add(symbol)
                    to_process.append(symbol)
        return reachables

    def get_generating_non_terminals(self) -> AbstractSet[Any]:
        """ Get the generating symbols

        Returns
        ----------
        generating : set of any
            The generating symbols from the start state
        """
        # Preprocess
        generating_from = dict()
        duplication_pointer = dict()
        generating = set()
        to_process = []
        consumption_rules = self.rules.get_consumption_rules()
        for rule in self.rules.get_rules():
            if rule.is_duplication():
                left = rule.left_term
                right0 = rule.get_right_terms()[0]
                right1 = rule.get_right_terms()[1]
                temp = [left, 2]
                if right0 in duplication_pointer:
                    duplication_pointer[right0].append(temp)
                else:
                    duplication_pointer[right0] = [temp]
                if right1 in duplication_pointer:
                    duplication_pointer[right1].append(temp)
                else:
                    duplication_pointer[right1] = [temp]
            if rule.is_production():
                left = rule.left_term
                right = rule.get_right_term()
                if right in generating_from:
                    generating_from[right].add(left)
                else:
                    generating_from[right] = {left}
            if rule.is_end_rule():
                left = rule.left_term
                if left not in generating:
                    generating.add(left)
                    to_process.append(left)
        for key in consumption_rules:
            for rule in consumption_rules[key]:
                left = rule.left_term
                right = rule.get_right()
                if right in generating_from:
                    generating_from[right].add(left)
                else:
                    generating_from[right] = {left}
        # Processing
        while to_process:
            current = to_process.pop()
            for symbol in generating_from.get(current, []):
                if symbol not in generating:
                    generating.add(symbol)
                    to_process.append(symbol)
            for duplication in duplication_pointer.get(current, []):
                duplication[1] -= 1
                if duplication[1] == 0:
                    if duplication[0] not in generating:
                        generating.add(duplication[0])
                        to_process.append(duplication[0])
        return generating

    def remove_useless_rules(self) -> "IndexedGrammar":
        """ Remove useless rules in the grammar

        More precisely, we remove rules which do not contain only generating or reachable \
            non terminals.

        Returns
        ----------
        i_grammar : :class:`~pyformlang.indexed_grammar.IndexedGrammar`
            The indexed grammar which useless rules
        """
        l_rules = []
        generating = self.get_generating_non_terminals()
        reachables = self.get_reachable_non_terminals()
        consumption_rules = self.rules.get_consumption_rules()
        for rule in self.rules.get_rules():
            if rule.is_duplication():
                left = rule.left_term
                right0 = rule.get_right_terms()[0]
                right1 = rule.get_right_terms()[1]
                if all([x in generating and x in reachables for x in [left, right0, right1]]):
                    l_rules.append(rule)
            if rule.is_production():
                left = rule.left_term
                right = rule.get_right_term()
                if all([x in generating and x in reachables for x in [left, right]]):
                    l_rules.append(rule)
            if rule.is_end_rule():
                left = rule.left_term
                if left in generating and left in reachables:
                    l_rules.append(rule)
        for key in consumption_rules:
            for rule in consumption_rules[key]:
                left = rule.left_term
                right = rule.get_right()
                if all([x in generating and x in reachables for x in [left, right]]):
                    l_rules.append(rule)
        rules = Rules(l_rules, self.rules.optim)
        return IndexedGrammar(rules)

    def intersection(self, other: Any) -> "IndexedGrammar":
        """ Computes the intersection of the current indexed grammar with the other object

        Parameters
        ----------
        other : any
            The object to intersect with

        Returns
        ----------
        i_grammar : :class:`~pyformlang.indexed_grammar.IndexedGrammar`
            The indexed grammar which useless rules
        """
        import pyformlang
        if isinstance(other, pyformlang.regular_expression.Regex):
            other = other.to_epsilon_nfa()
        if isinstance(other, pyformlang.finite_automaton.FiniteAutomaton):
            fst = other.to_fst()
            return fst.intersection(self)


def exists(l, f):
    """exists
    Check whether at least an element x of l is True for f(x)
    :param l: A list of elements to test
    :param f: The checking function (takes one parameter and return a
    boolean)
    """
    for x in l:
        if f(x):
            return True
    return False


def addrec_bis(l_sets, markedLeft, markedRight):
    """addrec_bis
    Optimized version of addrec
    :param l_sets: a list containing tuples (C, M) where:
        * C is a non-terminal on the left of a consumption rule
        * M is the set of the marked set for the right non-terminal in the
        production rule
    :param markedLeft: Sets which are marked for the non-terminal on the
    left of the production rule
    :param markedRight: Sets which are marked for the non-terminal on the
    right of the production rule
    """
    was_modified = False
    for s in list(markedRight):
        l_temp = [x for x in l_sets if x[0] in s]
        s_temp = [x[0] for x in l_temp]
        # At least one symbol to consider
        if frozenset(s_temp) == s and len(s) > 0:
            was_modified |= addrec_ter(l_temp, markedLeft, markedRight)
    return was_modified


def addrec_ter(l_sets, markedLeft, markedRight):
    """addrec
    Explores all possible combination of consumption rules to mark a
    production rule.
    :param l_sets: a list containing tuples (C, M) where:
        * C is a non-terminal on the left of a consumption rule
        * M is the set of the marked set for the right non-terminal in the
        production rule
    :param markedLeft: Sets which are marked for the non-terminal on the
    left of the production rule
    :param markedRight: Sets which are marked for the non-terminal on the
    right of the production rule
    :return Whether an element was actually marked
    """
    # End condition, nothing left to process
    temp_in = [x[0] for x in l_sets]
    exists_after = [exists(l_sets[index + 1:], lambda x: x[0] == l_sets[index][0])
                    for index in range(len(l_sets))]
    exists_before = [l_sets[index][0] in temp_in[:index]
                     for index in range(len(l_sets))]
    marked_sets = [l_sets[index][1] for index in range(len(l_sets))]
    marked_sets = [sorted(x, key=lambda x: -len(x)) for x in marked_sets]
    # Try to optimize by having an order of the sets
    zipped = zip(exists_after, exists_before, marked_sets)
    sorted_zip = sorted(zipped, key=lambda x: -len(x[2]))
    exists_after, exists_before, marked_sets = zip(*sorted_zip)
    res = False
    # contains tuples of index, temp_set
    to_process = []
    to_process.append((0, frozenset()))
    done = set()
    while to_process:
        index, new_temp = to_process.pop()
        if index >= len(l_sets):
            # Check if at least one non-terminal was considered, then if the set
            # of non-terminals considered is marked of the right non-terminal in
            # the production rule, then if a new set is marked or not
            if new_temp not in markedLeft:
                markedLeft.add(new_temp)
                res = True
            continue
        if exists_before[index] or exists_after[index]:
            to_append = (index + 1, new_temp)
            to_process.append(to_append)
        if not exists_before[index]:
            # For all sets which were marked for the current comsumption rule
            for s in marked_sets[index]:
                if s <= new_temp:
                    to_append = (index + 1, new_temp)
                elif new_temp <= s:
                    to_append = (index + 1, s)
                else:
                    to_append = (index + 1, new_temp.union(s))
                if to_append not in done:
                    done.add(to_append)
                    to_process.append(to_append)
    return res
