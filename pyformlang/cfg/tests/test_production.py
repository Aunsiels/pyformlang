""" Tests the productions """

import unittest

from pyformlang.cfg import Production, Variable, Terminal

class TestProduction(unittest.TestCase):
    """ Tests the production """

    def test_creation(self):
        p0 = Production(Variable("S0"), [Terminal("S1"), Variable("a")])
        p1 = Production(Variable("S0"), [Terminal("S1"), Variable("a")])
        p2 = Production(Variable("S0'"), [Terminal("S1"), Variable("a")])
        p3 = Production(Variable("S0"), [Terminal("S2"), Variable("a")])
        p4 = Production(Variable("S0"), [Terminal("S2"), Variable("b")])
        self.assertEqual(p0, p1)
        self.assertNotEqual(p0, p2)
        self.assertNotEqual(p0, p3)
        self.assertNotEqual(p0, p4)
        self.assertEqual(str(p0), str(p1))
        self.assertNotEqual(str(p0), str(p2))
        self.assertNotEqual(str(p0), str(p3))
        self.assertNotEqual(str(p0), str(p4))
        self.assertEqual(hash(p0), hash(p1))
        self.assertNotEqual(hash(p0), hash(p2))
        self.assertNotEqual(hash(p0), hash(p3))
        self.assertNotEqual(hash(p0), hash(p4))
        self.assertIn(" -> ", str(p0))
