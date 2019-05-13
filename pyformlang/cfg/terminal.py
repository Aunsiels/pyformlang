""" A terminal in a CFG """

from .cfg_object import CFGObject


class Terminal(CFGObject): # pylint: disable=too-few-public-methods
    """ An terminal in a CFG

    Parameters
    -----------
    value : any
        The value of the terminal
    """

    def __eq__(self, other):
        return isinstance(other, Terminal) and self.get_value() == other.get_value()

    def __repr__(self):
        return "Terminal(" + str(self.get_value()) + ")"

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self.get_value())
        return self._hash
