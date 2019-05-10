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
        self._head_body = [x for x in body if not isinstance(x, Epsilon)]
        self._head_body.append(head)
        self._hash = None

    def get_head(self) -> CFGObject:
        return self._head_body[-1]

    def get_body(self) -> Iterable[CFGObject]:
        return self._head_body[:-1]

    def __repr__(self):
        return str(self.get_head()) +  " -> " + " ".join([str(x) for x in self.get_body()])

    def __hash__(self):
        if self._hash is None:
            self._hash = sum(map(hash, self._head_body))
        return self._hash

    def __eq__(self, other):
        return self.get_head() == other.get_head() and self.get_body() == other.get_body()
