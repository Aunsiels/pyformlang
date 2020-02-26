""" Tests the productions """

import unittest

from pyformlang.cfg import Production, Variable, Terminal


class TestProduction(unittest.TestCase):
    """ Tests the production """
    # pylint: disable=missing-function-docstring

    def test_creation(self):
        prod0 = Production(Variable("S0"), [Terminal("S1"), Variable("a")])
        prod1 = Production(Variable("S0"), [Terminal("S1"), Variable("a")])
        prod2 = Production(Variable("S0'"), [Terminal("S1"), Variable("a")])
        prod3 = Production(Variable("S0"), [Terminal("S2"), Variable("a")])
        prod4 = Production(Variable("S0"), [Terminal("S2"), Variable("b")])
        self.assertEqual(prod0, prod1)
        self.assertNotEqual(prod0, prod2)
        self.assertNotEqual(prod0, prod3)
        self.assertNotEqual(prod0, prod4)
        self.assertEqual(str(prod0), str(prod1))
        self.assertNotEqual(str(prod0), str(prod2))
        self.assertNotEqual(str(prod0), str(prod3))
        self.assertNotEqual(str(prod0), str(prod4))
        self.assertEqual(hash(prod0), hash(prod1))
        self.assertNotEqual(hash(prod0), hash(prod2))
        self.assertNotEqual(hash(prod0), hash(prod3))
        self.assertNotEqual(hash(prod0), hash(prod4))
        self.assertIn(" -> ", str(prod0))
