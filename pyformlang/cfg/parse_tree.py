""" A parse Tree """

from pyformlang.cfg import Variable


class ParseTree:
    """ A parse tree """

    def __init__(self, value):
        self.value = value
        self.sons = []

    def __repr__(self):
        return "ParseTree(" + str(self.value) + ", " + str(self.sons) + ")"

    def get_leftmost_derivation(self):
        """
        Get the leftmost derivation

        Returns
        -------
        derivation : list of list of :class:`~pyformlang.cfg.CFGObject`
            The derivation

        """
        if len(self.sons) == 0 and isinstance(self.value, Variable):
            return [[self.value], []]
        if len(self.sons) == 0:
            return [[self.value]]
        res = [[self.value]]
        start = []
        for i, son in enumerate(self.sons):
            end = [x.value for x in self.sons[i + 1:]]
            derivation = []
            derivations = son.get_leftmost_derivation()
            if i != 0 and derivations and derivations[0]:
                del derivations[0]
            for derivation in derivations:
                res.append(start + derivation + end)
            start = start + derivation
        return res

    def get_rightmost_derivation(self):
        """
        Get the leftmost derivation

        Returns
        -------
        derivation : list of list of :class:`~pyformlang.cfg.CFGObject`
            The derivation

        """
        if len(self.sons) == 0 and isinstance(self.value, Variable):
            return [[self.value], []]
        if len(self.sons) == 0:
            return [[self.value]]
        res = [[self.value]]
        end = []
        for i, son in enumerate(self.sons[::-1]):
            start = [x.value for x in self.sons[:-1 - i]]
            derivation = []
            derivations = son.get_rightmost_derivation()
            if i != 0 and derivations and derivations[0]:
                del derivations[0]
            for derivation in derivations:
                res.append(start + derivation + end)
            end = derivation + end
        return res
