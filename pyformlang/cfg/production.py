""" A production or rule of a CFG """

from typing import Iterable

from .variable import Variable
from .cfg_object import CFGObject
from .epsilon import Epsilon


class Production(object):
    """ A production or rule of a CFG

    Parameters
    ----------
    head : :class:`~pyformlang.cfg.Variable`
        The head of the production
    body : iterable of :class:`~pyformlang.cfg.CFGObject`
        The body of the production
    """

    def __init__(self, head: Variable, body: Iterable[CFGObject]):
        self._head = head
        self._body = tuple([x for x in body if x != Epsilon()])

    def get_head(self) -> Variable:
        return self._head

    def get_body(self) -> Iterable[CFGObject]:
        return self._body

    def __repr__(self):
        return str(self._head) +  " -> " + " ".join([str(x) for x in self._body])

    def __hash__(self):
        return hash(self._head) + hash(self._body)

    def __eq__(self, other):
        return self._head == other.get_head() and self._body == other.get_body()
