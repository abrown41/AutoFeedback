"""This file is for testing purposes. It allows the test suite to operate on
main.py in the root directory, exactly as AutoFeedback is intended to operate
on student work by default"""
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


def f1(x):
    return(x**2)


def f2(x, y):
    return


x = 3
y = np.linspace(0, 1, 3)
z = np.eye(3)

plt.plot([0, 1, 2], [0, 1, 4], 'r-', label='quadratic')
plt.plot([0.5, 1.5], [1.5, 2.5], 'bD', label='linear')
plt.legend()
plt.axis([-1, 1, -2, 2])
plt.xlabel('x')
plt.ylabel('y')
plt.title('z')


symx = sp.symbols("x")
symy = sp.Array([1, 2, symx])
symz = sp.Matrix([[1, 2, 3], [1, 3, 2], [3, 1, 2]])
symd = {"a": 1, "b": 2}
