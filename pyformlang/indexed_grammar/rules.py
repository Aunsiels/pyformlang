"""
Representations of rules in a indexed grammar
"""

from typing import Iterable, Dict, Any

from .production_rule import ProductionRule
from .consumption_rule import ConsumptionRule
from .rule_ordering import RuleOrdering
from .reduced_rule import ReducedRule


class Rules(object):
    """Store a set of rules and manipulate them

    Parameters
    ----------
    rules : iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
        A list of all the rules
    optim : int
        Optimization of the order of the rules
        0 -> given order
        1 -> reverse order
        2 -> order by core number
        3 -> reverse order of core number
        4 -> reverse order by arborescence
        5 -> order by arborescence
        6 -> order by number of edges
        7 -> reverse order by number of edges
        8 -> random order
    """

    def __init__(self, rules: Iterable[ReducedRule], optim: int=7):
        self.rules = []
        self.consumptionRules = dict()
        self.optim = optim
        for rule in rules:
            # We separate consumption rule from other
            if rule.is_consumption():
                temp = self.consumptionRules.setdefault(rule.get_f(), [])
                if rule not in temp:
                    temp.append(rule)
                self.consumptionRules[rule.get_f()] = temp
            else:
                if rule not in self.rules:
                    self.rules.append(rule)
        ro = RuleOrdering(self.rules, self.consumptionRules)
        if optim == 1:
            self.rules = ro.reverse()
        elif optim == 2:
            self.rules = ro.order_by_core()
        elif optim == 3:
            self.rules = ro.order_by_core(reverse=True)
        elif optim == 4:
            self.rules = ro.order_by_arborescence(reverse=True)
        elif optim == 5:
            self.rules = ro.order_by_arborescence(reverse=False)
        elif optim == 6:
            self.rules = ro.order_by_edges()
        elif optim == 7:
            self.rules = ro.order_by_edges(reverse=True)
        elif optim == 8:
            self.rules = ro.order_random()

    def get_rules(self) -> Iterable[ReducedRule]:
        """Gets the non consumption rules

        Returns
        ----------
        non_consumption_rules :  iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
            The non consumption rules
        """
        return self.rules

    def get_length(self) -> (int, int):
        """Get the total number of rules

        Returns
        ---------
        number_rules : couple of int
            A couple with first the number of non consumption rules and then\
                the number of consumption rules
        """
        return (len(self.rules), len(self.consumptionRules.values()))

    def get_consumption_rules(self) -> Dict[Any, Iterable[ConsumptionRule]]:
        """Gets the consumption rules

        Returns
        ----------
        consumption_rules : dict of any to iterable of \
            :class:`~pyformlang.indexed_grammar.ConsumptionRule`
            A dictionary contains the consumption rules gathered by consumed symbols
        """
        return self.consumptionRules

    def get_terminals(self) -> Iterable[Any]:
        """Gets all the terminals used by all the rules

        Returns
        ----------
        terminals : iterable of any
            The terminals used in the rules
        """
        terminals = set()
        for temp_rule in self.consumptionRules.values():
            for rule in temp_rule:
                terminals = terminals.union(rule.get_terminals())
        for rule in self.rules:
            terminals = terminals.union(rule.get_terminals())
        return terminals

    def get_non_terminals(self) -> Iterable[Any]:
        """Gets all the non-terminals used by all the rules

        Returns
        ----------
        non_terminals : iterable of any
            The non terminals used in the rule
        """
        terminals = set()
        for temp_rule in self.consumptionRules.values():
            for rule in temp_rule:
                terminals = terminals.union(set(rule.get_non_terminals()))
        for rule in self.rules:
            terminals = terminals.union(set(rule.get_non_terminals()))
        return list(terminals)

    def remove_production(self, left: Any, right: Any, prod: Any):
        """Remove the production rule:
            left[sigma] -> right[prod sigma]

        Parameters
        -----------
        left : any
            The left non-terminal in the rule
        right : any
            The right non-terminal in the rule
        prod : any
            The production used in the rule
        """
        self.rules = list(filter(lambda x: not(x.is_production() and
                                 x.get_left_term() == left and
                                 x.get_right_term() == right and
                                 x.get_production() == prod), self.rules))

    def add_production(self, left: Any, right: Any, prod: Any):
        """Add the production rule:
            left[sigma] -> right[prod sigma]

        Parameters
        -----------
        left : any
            The left non-terminal in the rule
        right : any
            The right non-terminal in the rule
        prod : any
            The production used in the rule
        """
        self.rules.append(ProductionRule(left, right, prod))

