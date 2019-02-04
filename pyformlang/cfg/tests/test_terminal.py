""" Tests the terminal """

import unittest

from pyformlang.cfg import Terminal

class TestTerminal(unittest.TestCase):
    """ Tests the terminal """

    def test_creation(self):
        t0 = Terminal(0)
        t1 = Terminal(1)
        t2 = Terminal(0)
        t3 = Terminal("0")
        self.assertEqual(t0, t2)
        self.assertNotEqual(t0, t1)
        self.assertNotEqual(t0, t3)
        self.assertEqual(hash(t0), hash(t2))
        self.assertNotEqual(hash(t0), hash(t1))
        self.assertEqual(str(t0), str(t2))
        self.assertEqual(str(t0), str(t3))
        self.assertNotEqual(str(t0), str(t1))
