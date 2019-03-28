"""
Representation of a way to order rules
"""

from typing import Iterable, Dict, Any

import networkx as nx
from queue import Queue
import random

from .reduced_rule import ReducedRule
from .consumption_rule import ConsumptionRule


class RuleOrdering(object):
    """A class to order rules in an indexed grammar

    Parameters
    ----------
    rules : iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
        The non consumption rules of the indexed grammar
    conso_rules : dict of any to :class:`~pyformlang.indexed_grammar.ConsumptionRule`
        The consumption rules of the indexed grammar
    """

    def __init__(self, rules: Iterable[ReducedRule],
                 conso_rules: Dict[Any, ConsumptionRule]):
        self.rules = rules
        self.conso_rules = conso_rules

    def reverse(self) -> Iterable[ReducedRule]:
        """The reverser ordering, simply reverse the order.

        Returns
        ----------
        new_rules : iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
            The reversed rules
        """
        return self.rules[::1]

    def _get_graph(self):
        """ Get the graph of the non-terminals in the rules. If there
        there is a link between A and B (oriented), it means that modifying A
        may modify B"""
        di_graph = nx.DiGraph()
        for rule in self.rules:
            if rule.is_duplication():
                if rule.get_right_terms()[0] != rule.get_left_term():
                    di_graph.add_edge(rule.get_right_terms()[0], rule.get_left_term())
                if rule.get_right_terms()[1] != rule.get_left_term():
                    di_graph.add_edge(rule.get_right_terms()[1], rule.get_left_term())
            if rule.is_production():
                f_rules = self.conso_rules.setdefault(
                    rule.get_production(), [])
                for f_rule in f_rules:
                    if f_rule.get_right() != rule.get_left_term():
                        di_graph.add_edge(f_rule.get_right(), rule.get_left_term())
        return di_graph

    def order_by_core(self, reverse: bool=False) -> Iterable[ReducedRule]:
        """Order the rules using the core numbers

        Parameters
        ----------
        reverse : bool
            Boolean to know if we should reverse the order

        Returns
        ----------
        new_rules : iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rules ordered using core number
        """
        # Graph construction
        di_graph = self._get_graph()
        # Get core number, careful the degree is in + out
        core_numbers = nx.core_number(di_graph)
        new_order = sorted(self.rules,
                           key=lambda x: core_numbers.setdefault(
                               x.get_left_term(), 0))
        if reverse:
            new_order.reverse()
        return new_order

    def order_by_arborescence(self, reverse: bool=True) -> Iterable[ReducedRule]:
        """Order the rules using the arborescence method.

        Parameters
        ----------
        reverse : bool
            Boolean to know if we should reverse the order

        Returns
        ----------
        new_rules : iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rules ordered using core number
        """
        di_graph = self._get_graph()
        # arborescence = nx.minimum_spanning_arborescence(di_graph)
        arborescence = nx.minimum_spanning_tree(di_graph.to_undirected())
        to_process = Queue()
        processed = set()
        res = dict()
        res["S"] = 0
        for x in arborescence["S"]:
            if x not in processed:
                res[x] = 1
                processed.add(x)
                to_process.put(x)
        while not to_process.empty():
            p = to_process.get()
            for x in arborescence[p]:
                if x not in processed:
                    res[x] = res[p] + 1
                    processed.add(x)
                    to_process.put(x)
        new_order = sorted(self.rules,
                           key=lambda x: res.setdefault(
                               x.get_left_term(), 0))
        if reverse:
            new_order.reverse()
        return new_order

    def _get_len_out(self, di_graph, x):
        """Get the number of out edges of a rule (more exactly, the non terminal at
        its left.

        Parameters
        ----------
        di_graph : DiGraph
            A directed graph
        x : :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rule
        """
        if x.get_left_term() in di_graph:
            return len(di_graph[x.get_left_term()])
        else:
            return 0

    def order_by_edges(self, reverse=False):
        """Order using the number of edges.

        Parameters
        ----------
        reverse : bool
            Boolean to know if we should reverse the order

        Returns
        ----------
        new_rules : iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rules ordered by number of edges
        """
        di_graph = self._get_graph()
        new_order = sorted(self.rules, key=lambda x:
                           self._get_len_out(di_graph, x))
        if reverse:
            new_order.reverse()
        return new_order

    def order_random(self):
        """The random ordering

        Returns
        ----------
        new_rules : iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rules ordered at random
        """
        random.shuffle(self.rules)
        return self.rules
