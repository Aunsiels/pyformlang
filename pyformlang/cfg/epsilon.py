""" An epsilon terminal """

from .terminal import Terminal

class Epsilon(Terminal):
    """ An epsilon terminal """

    def __init__(self):
        super().__init__("epsilon")
