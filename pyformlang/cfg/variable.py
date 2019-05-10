""" A variable in a CFG """

from .cfg_object import CFGObject


class Variable(CFGObject): # pylint: disable=too-few-public-methods
    """ An variable in a CFG

    Parameters
    -----------
    value : any
        The value of the variable
    """

    def __init__(self, value):
        super().__init__(value)
        self._hash = None

    def __eq__(self, other):
        return self._value == other.get_value()

    def __str__(self):
        return str(self.get_value())

    def __repr__(self):
        return "Variable(" + str(self.get_value()) + ")"

    def __hash__(self):
        if self._hash is None:
            self._hash = self.compute_new_hash()
        return self._hash

    def compute_new_hash(self):
        return hash(self._value)

