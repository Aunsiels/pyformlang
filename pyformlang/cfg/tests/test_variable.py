""" Tests the variable """

import unittest

from pyformlang.cfg import Variable

class TestVariable(unittest.TestCase):
    """ Tests the variable """

    def test_creation(self):
        v0 = Variable(0)
        v1 = Variable(1)
        v2 = Variable(0)
        v3 = Variable("0")
        self.assertEqual(v0, v2)
        self.assertNotEqual(v0, v1)
        self.assertNotEqual(v0, v3)
        self.assertEqual(hash(v0), hash(v2))
        self.assertNotEqual(hash(v0), hash(v1))
        self.assertEqual(str(v0), str(v2))
        self.assertEqual(str(v0), str(v3))
        self.assertNotEqual(str(v0), str(v1))
