""" A variable in a CFG """

from .cfg_object import CFGObject


class Variable(CFGObject): # pylint: disable=too-few-public-methods
    """ An variable in a CFG

    Parameters
    -----------
    value : any
        The value of the variable
    """

    def __eq__(self, other):
        return isinstance(other, Variable) and self.get_value() == other.get_value()

    def __repr__(self):
        return "Variable(" + str(self.get_value()) + ")"

    def __hash__(self):
        return hash(self.get_value())
