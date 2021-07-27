import unittest
import numpy as np
import sympy as sp

import AutoFeedback.varchecks as vc

class tmod:
    x = sp.symbols("x")
    y = sp.Array([1,2,x])
    z = sp.Matrix([[1,2,x],[1,x,2],[x,1,2]])

class UnitTests(unittest.TestCase) :
    def test_matrixshape(self):
        myz=np.array([[1,2,3],[4,5,6],[7,8,9]])
        assert(vc.check_size(tmod.z,myz))

    def test_notmatrixshape(self):
        myz=np.array([[1,2,3,4,5,6,7,8,9]])
        assert(not vc.check_size(tmod.z,myz))

    def test_arraysize(self):
        assert(vc.check_size(tmod.y,[1,2,3]))
