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

    def __init__(self, head: Variable, body: Iterable[CFGObject], filtering=True):
        if filtering:
            self._body = [x for x in body if not isinstance(x, Epsilon)]
        else:
            self._body = body
        self._head = head
        self._hash = None

    @property
    def head(self) -> Variable:
        return self._head

    @property
    def body(self) -> Iterable[CFGObject]:
        return self._body

    def __repr__(self):
        return str(self.head) + " -> " + " ".join([str(x) for x in self.body])

    def __hash__(self):
        if self._hash is None:
            self._hash = sum(map(hash, self._body)) + hash(self._head)
        return self._hash

    def __eq__(self, other):
        return self.head == other.head and self.body == other.body
