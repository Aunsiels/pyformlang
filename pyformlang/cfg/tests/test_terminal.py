""" Tests the terminal """

import unittest

from pyformlang.cfg import Terminal


class TestTerminal(unittest.TestCase):
    """ Tests the terminal """
    # pylint: disable=missing-function-docstring

    def test_creation(self):
        terminal0 = Terminal(0)
        terminal1 = Terminal(1)
        terminal2 = Terminal(0)
        terminal3 = Terminal("0")
        self.assertEqual(terminal0, terminal2)
        self.assertNotEqual(terminal0, terminal1)
        self.assertNotEqual(terminal0, terminal3)
        self.assertEqual(hash(terminal0), hash(terminal2))
        self.assertNotEqual(hash(terminal0), hash(terminal1))
        self.assertEqual(str(terminal0), str(terminal2))
        self.assertEqual(str(terminal0), str(terminal3))
        self.assertNotEqual(str(terminal0), str(terminal1))
