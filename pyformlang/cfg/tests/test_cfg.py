""" Tests the CFG """

import unittest

from pyformlang.cfg import Production, Variable, Terminal, CFG

class TestCFG(unittest.TestCase):
    """ Tests the production """

    def test_creation(self):
        v0 = Variable(0)
        t0 = Terminal("a")
        p0 = Production(v0, [t0, Terminal("A"), Variable(1)])
        cfg = CFG({v0}, {t0}, v0, {p0})
        self.assertIsNotNone(cfg)
        cfg = CFG()
        self.assertIsNotNone(cfg)
