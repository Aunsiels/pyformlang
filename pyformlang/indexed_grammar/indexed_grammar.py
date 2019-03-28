"""
Representation of an indexed grammar
"""

from typing import Any, Iterable

from .duplication_rule import DuplicationRule
from .production_rule import ProductionRule
from .rules import Rules

class IndexedGrammar(object):
    """ Describes an indexed grammar.

    Parameters
    ----------
    rules : :class:`~pyformlang.indexed_grammar.Rules`
        The rules of the grammar, in reduced form put into a Rule
    """

    def __init__(self, rules: Rules):
        self.rules = rules
        # Precompute all non-terminals
        self.non_terminals = rules.get_non_terminals()
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
                      lambda x: x.is_end_rule() and x.get_left_term() == A):
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
                temp = x.union(y)
                # Check if it was marked before
                if temp not in self.marked[rule.get_left_term()]:
                    was_modified = True
                    if rule.get_left_term() == rule.get_right_terms()[0]:
                        right_term_marked0.append(temp)
                    elif rule.get_left_term() == rule.get_right_terms()[1]:
                        right_term_marked1.append(temp)
                    else:
                        self.marked[rule.get_left_term()].add(temp)
                    # Stop condition, no need to continuer
                    if rule.get_left_term() == "S" and len(temp) == 0:
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
        l_temp = [(x.get_left_term(),
                  self.marked[x.get_right()]) for x in f_rules]
        marked_symbols = [x.get_left_term() for x in f_rules]
        # Process all combinations of consumption rule
        was_modified |= addrec_bis(l_temp,
                                   self.marked[rule.get_left_term()],
                                   self.marked[rule.get_right_term()])
        # End condition
        if frozenset() in self.marked["S"]:
            return (was_modified, True)
        if rule.get_right_term() in marked_symbols:
            for s in l_temp:
                if rule.get_right_term() == s[0]:
                    for sc in s[1]:
                        if sc not in\
                                self.marked[rule.get_left_term()]:
                            was_modified = True
                            self.marked[rule.get_left_term()].add(sc)
                            if rule.get_left_term() == "S" and len(sc) == 0:
                                return (was_modified, True)
        # Edge case
        if frozenset() in self.marked[rule.get_right_term()]:
            if frozenset() not in self.marked[rule.get_left_term()]:
                was_modified = True
                self.marked[rule.get_left_term()].add(frozenset())
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
        return True


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


def addrec_ter(l_sets, markedLeft, markedRight, temp=frozenset(),
               temp_in=frozenset()):
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
    :param temp: Contains the union of all sets considered up to that point
    :param temp_in: Contains the non-terminals on the left of consumption
    rules which have been considered up to that point
    :return Whether an element was actually marked
    """
    # End condition, nothing left to process
    if len(l_sets) == 0:
        # Check if at least one non-terminal was considered, then if the set
        # of non-terminals considered is marked of the right non-terminal in
        # the production rule, then if a new set is marked or not
        if temp not in markedLeft:
            markedLeft.add(temp)
            return True
        return False
    res = False
    if l_sets[0][0] in temp_in or \
            exists(l_sets[1:], lambda x: x[0] == l_sets[0][0]):
        res |= addrec_ter(l_sets[1:], markedLeft, markedRight, temp, temp_in)
    if l_sets[0][0] not in temp_in:
        # For all sets which were marked for the current comsumption rule
        for s in l_sets[0][1]:
            res |= addrec_ter(l_sets[1:], markedLeft, markedRight,
                              temp.union(s),
                              temp_in.union({l_sets[0][0]}))
    return res
