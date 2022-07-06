"""This file is for testing purposes. It allows the test suite to operate on
main.py in the root directory, exactly as AutoFeedback is intended to operate
on student work by default"""
import matplotlib.pyplot as plt


x = 17
plt.plot([0, 1, 2], [0, 1, 4], 'r-', label='quadratic')
plt.plot([0.5, 1.5], [1.5, 2.5], 'bD', label='linear')
plt.legend()
plt.axis([-1, 1, -2, 2])
plt.xlabel('x')
plt.ylabel('y')
plt.title('z')
