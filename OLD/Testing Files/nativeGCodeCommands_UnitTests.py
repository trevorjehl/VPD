"""
Verify functionality of all basic 
GCode commands.

Created Jul 2023
"""
import unittest
import sys
import math

sys.path.append("../VPD")
from nativeGCodeCommands import *


class testAddDecimalPoint(unittest.TestCase):
    def testNone(self):
        self.assertEqual(addDecimalPoint(None), None)

    def testFloat(self):
        self.assertEqual(addDecimalPoint(1.0), "1.0")

    def testInt(self):
        self.assertEqual(addDecimalPoint(1), "1.0")

    def testTuple(self):
        self.assertEqual(addDecimalPoint((1.4, 2)), (1.4, 2.0))

    def testNoneList(self):
        self.assertEqual(addDecimalPoint([None, None]), [None, None])

    def testNoneAndInt(self):
        self.assertEqual(addDecimalPoint([None, 1]), [None, 1.0])

    def testNoneAndFloat(self):
        self.assertEqual(addDecimalPoint([None, 1.2]), [None, 1.2])

    def testNoneAndString(self):
        self.assertEqual(addDecimalPoint([None, "helloword"]), [None, "helloword"])


class TestNonExtrudeMove(unittest.TestCase):
    def test_xyz_move(self):
        self.assertEqual(nonExtrudeMove([], 1, 2, 3), ["G0 X1.0 Y2.0 Z3.0"])

    def test_xy_move(self):
        self.assertEqual(nonExtrudeMove([], X=1, Y=2), ["G0 X1.0 Y2.0"])

    def test_xz_move(self):
        self.assertEqual(nonExtrudeMove([], X=1, Z=3), ["G0 X1.0 Z3.0"])

    def test_yz_move(self):
        self.assertEqual(nonExtrudeMove([], Y=2, Z=3), ["G0 Y2.0 Z3.0"])

    def test_x_move(self):
        self.assertEqual(nonExtrudeMove([], X=1), ["G0 X1.0"])

    def test_y_move(self):
        self.assertEqual(nonExtrudeMove([], Y=2), ["G0 Y2.0"])

    def test_z_move(self):
        self.assertEqual(nonExtrudeMove([], Z=3), ["G0 Z3.0"])


if __name__ == "__main__":
    unittest.main()
