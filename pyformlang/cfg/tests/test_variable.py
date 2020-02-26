""" Tests the variable """

import unittest

from pyformlang.cfg import Variable


class TestVariable(unittest.TestCase):
    """ Tests the variable """
    # pylint: disable=missing-function-docstring

    def test_creation(self):
        variable0 = Variable(0)
        variable1 = Variable(1)
        variable2 = Variable(0)
        variable3 = Variable("0")
        self.assertEqual(variable0, variable2)
        self.assertNotEqual(variable0, variable1)
        self.assertNotEqual(variable0, variable3)
        self.assertEqual(hash(variable0), hash(variable2))
        self.assertNotEqual(hash(variable0), hash(variable1))
        self.assertEqual(str(variable0), str(variable2))
        self.assertEqual(str(variable0), str(variable3))
        self.assertNotEqual(str(variable0), str(variable1))
