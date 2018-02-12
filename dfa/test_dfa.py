"""
    dfa.test_dfa
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
import unittest
from dfa import DFAInterp
from machines import *


class TestDFAInterp(unittest.TestCase):
    def setUp(self):
        self.interp = DFAInterp(DFA1)

    def test_delta(self):
        self.assertEqual(self.interp._current, "q0")

        self.interp.delta(1)

        self.assertEqual(self.interp._current, "q0")

        self.interp.delta(0)

        self.assertEqual(self.interp._current, "q1")

        with self.assertRaises(RuntimeError):
            self.interp.delta(4)

    def test_run(self):
        self.interp("01011")

        self.assertEqual(self.interp.accept_status, True)

        self.interp = DFAInterp(DFA1)

        self.interp("010010")

        self.assertEqual(self.interp.accept_status, False)

    def test_counter(self):
        self.interp("0101111111111111111")
        self.assertEqual(self.interp.counter, 19)


if __name__ == '__main__':
    unittest.main()
