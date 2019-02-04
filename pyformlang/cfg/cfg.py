""" A context free grammar """

from typing import AbstractSet

from .variable import Variable
from .terminal import Terminal
from .production import Production


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
                    self._terminals.add(cfg_object)
                else:
                    self._variables.add(cfg_object)
