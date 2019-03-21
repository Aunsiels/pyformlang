""" A context free grammar """

from typing import AbstractSet, List, Iterable, Tuple

from .variable import Variable
from .terminal import Terminal
from .production import Production
from .cfg_object import CFGObject
from .epsilon import Epsilon


class CFG(object):
    """ A class representing a context free grammar

    Parameters
    ----------
    variables : set of :class:`~pyformlang.cfg.Variable`, optional
        The variables of the CFG
    terminals : set of :class:`~pyformlang.cfg.Terminal`, optional
        The terminals of the CFG
    start_symbol : :class:`~pyformlang.cfg.Variable`, optional
        The start symbol
    productions : set of :class:`~pyformlang.cfg.Production`, optional
        The productions or rules of the CFG
    """

    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: AbstractSet[Production] = None):
        self._variables = variables or set()
        self._terminals = terminals or set()
        self._start_symbol = start_symbol
        if start_symbol is not None:
            self._variables.add(start_symbol)
        self._productions = productions or set()
        for production in self._productions:
            self._variables.add(production.get_head())
            for cfg_object in production.get_body():
                if isinstance(cfg_object, Terminal):
                    if cfg_object != Epsilon():
                        self._terminals.add(cfg_object)
                else:
                    self._variables.add(cfg_object)

    def get_number_variables(self) -> int:
        """ Returns the number of Variables

        Returns
        ----------
        n_variables : int
            The number of variables
        """
        return len(self._variables)

    def get_number_terminals(self) -> int:
        """ Returns the number of Terminals

        Returns
        ----------
        n_terminals : int
            The number of terminals
        """
        return len(self._terminals)

    def get_number_productions(self) -> int:
        """ Returns the number of Productions

        Returns
        ----------
        n_productions : int
            The number of productions
        """
        return len(self._productions)

    def get_generating_symbols(self) -> AbstractSet[CFGObject]:
        """ Gives the objects which are generating in the CFG

        Returns
        ----------
        generating_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The generating symbols of the CFG
        """
        g_symbols = set()
        g_symbols.add(Epsilon())
        productions = self._productions.copy()
        for terminal in self._terminals:
            g_symbols.add(terminal)
        found_modification = True
        while found_modification:
            found_modification = False
            used_productions = []
            for production in productions:
                if all([x in g_symbols for x in production.get_body()]):
                    found_modification = True
                    used_productions.append(production)
                    g_symbols.add(production.get_head())
            for production in used_productions:
                productions.remove(production)
        g_symbols.remove(Epsilon())
        return g_symbols

    def get_reachable_symbols(self) -> AbstractSet[CFGObject]:
        """ Gives the objects which are reachable in the CFG

        Returns
        ----------
        reachable_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The reachable symbols of the CFG
        """
        r_symbols = set()
        r_symbols.add(self._start_symbol)
        productions = self._productions.copy()
        found_modification = True
        while found_modification:
            found_modification = False
            used_productions = []
            for production in productions:
                if production.get_head() in r_symbols:
                    found_modification = True
                    used_productions.append(production)
                    for symbol in production.get_body():
                        if symbol != Epsilon():
                            r_symbols.add(symbol)
            for production in used_productions:
                productions.remove(production)
        return r_symbols

    def remove_useless_symbols(self) -> "CFG":
        """ Removes useless symbols in a CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG without useless symbols
        """
        generating = self.get_generating_symbols()
        productions = [x for x in self._productions
                       if x.get_head() in generating and
                       all([y in generating for y in x.get_body()])]
        new_var = self._variables.intersection(generating)
        new_ter = self._terminals.intersection(generating)
        cfg_temp = CFG(new_var, new_ter, self._start_symbol, productions)
        reachables = cfg_temp.get_reachable_symbols()
        productions = [x for x in productions
                       if x.get_head() in reachables]
        new_var = new_var.intersection(reachables)
        new_ter = new_ter.intersection(reachables)
        return CFG(new_var, new_ter, self._start_symbol, productions)

    def get_nullable_symbols(self) -> AbstractSet[CFGObject]:
        """ Gives the objects which are nullable in the CFG

        Returns
        ----------
        nullable_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The nullable symbols of the CFG
        """
        n_symbols = set()
        n_symbols.add(Epsilon())
        productions = self._productions.copy()
        found_modification = True
        while found_modification:
            found_modification = False
            used_productions = []
            for production in productions:
                if all([x in n_symbols for x in production.get_body()]) or \
                        len(production.get_body()) == 0:
                    found_modification = True
                    used_productions.append(production)
                    n_symbols.add(production.get_head())
            for production in used_productions:
                productions.remove(production)
        n_symbols.remove(Epsilon())
        return n_symbols

    def remove_epsilon(self) -> "CFG":
        """ Removes the epsilon of a cfg

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG without epsilons
        """
        new_productions = []
        nullables = self.get_nullable_symbols()
        for production in self._productions:
            new_productions += remove_nullable_production(production, nullables)
        return CFG(self._variables,
                   self._terminals,
                   self._start_symbol,
                   set(new_productions))

    def get_unit_pairs(self) -> AbstractSet[Tuple[Variable, Variable]]:
        """ Finds all the unit pairs

        Returns
        ----------
        unit_pairs : set of tuple of :class:`~pyformlang.cfg.Variable`
            The unit pairs
        """
        unit_pairs = set()
        for variable in self._variables:
            unit_pairs.add((variable, variable))
        productions = [x for x in self._productions if len(x.get_body()) == 1 and\
                                                       isinstance(x.get_body()[0], Variable)]
        to_process = list(unit_pairs)
        while to_process:
            var_A, var_B = to_process.pop()
            for production in productions:
                if production.get_head() != var_B:
                    continue
                temp = (var_A, production.get_body()[0])
                if temp not in unit_pairs:
                    unit_pairs.add(temp)
                    to_process.append(temp)
        return unit_pairs

    def eliminate_unit_productions(self) -> "CFG":
        """ Eliminate all the unit production in the CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A new CFG equivalent without unit productions
        """
        unit_pairs = self.get_unit_pairs()
        productions = [x for x in self._productions if len(x.get_body()) != 1 or\
                                                       not isinstance(x.get_body()[0], Variable)]
        new_productions = []
        for var_A, var_B in unit_pairs:
            for production in productions:
                if var_B == production.get_head():
                    new_productions.append(Production(var_A,
                                                      production.get_body()))
        return CFG(self._variables,
                   self._terminals,
                   self._start_symbol,
                   set(productions + new_productions))

    def _get_productions_with_only_single_terminals(self):
        """ Remove the terminals involved in a body of length more than 1 """
        term_to_var = dict()
        new_productions = []
        for terminal in self._terminals:
            var = Variable(str(terminal.get_value()) + "#CNF#")
            term_to_var[terminal] = var
        # We want to add only the useful productions
        used = set()
        for production in self._productions:
            if len(production.get_body()) == 1:
                new_productions.append(production)
                continue
            new_body = []
            for symbol in production.get_body():
                if symbol in term_to_var:
                    new_body.append(term_to_var[symbol])
                    used.add(symbol)
                else:
                    new_body.append(symbol)
            new_productions.append(Production(production.get_head(),
                                              new_body))
        for terminal in used:
            new_productions.append(Production(term_to_var[terminal], [terminal]))
        return new_productions

    def _get_next_free_variable(self, idx):
        idx += 1
        temp = Variable("C#CNF#" + str(idx))
        while temp in self._variables:
            idx += 1
            temp = Variable("C#CNF#" + str(idx))
        return idx, temp

    def _decompose_productions(self, productions):
        """ Decompose productions """
        idx = 0
        new_productions = []
        done = dict()
        for production in productions:
            body = production.get_body()
            if len(body) <= 2:
                new_productions.append(production)
                continue
            new_var = []
            for _ in range(len(body) - 2):
                idx, var = self._get_next_free_variable(idx)
                new_var.append(var)
            head = production.get_head()
            stopped = False
            for i in range(len(body) - 2):
                temp = tuple(body[i+1:])
                if temp in done:
                    new_productions.append(Production(head,
                                                      (body[i], done[temp])))
                    stopped = True
                    break
                new_productions.append(Production(head, (body[i], new_var[i])))
                done[temp] = new_var[i]
                head = new_var[i]
            if not stopped:
                new_productions.append(Production(head, [body[-2], body[-1]]))
        return new_productions


    def to_normal_form(self) -> "CFG":
        """ Gets the Chomsky Normal Form of a CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A new CFG equivalent in the CNF form
        """
        nullables = self.get_nullable_symbols()
        unit_pairs = self.get_unit_pairs()
        generating = self.get_generating_symbols()
        reachables = self.get_reachable_symbols()
        if len(nullables) != 0 or len(unit_pairs) != len(self._variables) or\
                len(generating) != len(self._variables) + len(self._terminals) or \
                len(reachables) != len(self._variables) + len(self._terminals):
            new_cfg = self.remove_epsilon()\
                          .eliminate_unit_productions()\
                          .remove_useless_symbols()
            return new_cfg.to_normal_form()
        # Remove terminals from body
        new_productions = self._get_productions_with_only_single_terminals()
        new_productions = self._decompose_productions(new_productions)
        return CFG(self._variables, self._terminals, self._start_symbol,
                   set(new_productions))

def remove_nullable_production_sub(body: Iterable[CFGObject],
                                   nullables: AbstractSet[CFGObject]) -> List[List[CFGObject]]:
    """ Recursive sub function to remove nullable objects """
    if not body:
        return [[]]
    all_next = remove_nullable_production_sub(body[1:], nullables)
    res = []
    for body_temp in all_next:
        if body[0] in nullables:
            res.append(body_temp)
        if body[0] != Epsilon():
            res.append([body[0]] + body_temp.copy())
    return res

def remove_nullable_production(production: Production,
                               nullables: AbstractSet[CFGObject]) -> List[Production]:
    """ Get all combinations of productions rules after removing nullable """
    next_prod_l = remove_nullable_production_sub(production.get_body(),
                                               nullables)
    res = []
    for prod_l in next_prod_l:
        if prod_l:
            res.append(Production(production.get_head(),
                                  prod_l))
    return res
