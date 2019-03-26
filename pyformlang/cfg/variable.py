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
        return isinstance(other, Variable) and self.get_value() == other.get_value()

    def __repr__(self):
        return "Variable(" + str(self.get_value()) + ")"

    def __hash__(self):
        if self._hash is not None:
            return self._hash
        else:
            temp = hash(self.get_value())
            self._hash = temp
            return temp
