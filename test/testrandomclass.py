import unittest
from AutoFeedback.randomclass import randomvar as rv


class VarErrorTests(unittest.TestCase):
    def test_integer(self):
        r = rv(expectation=0)
        r.diagnosis = "integer"
        error_message = """The googlyboo should only take integer values
             You should be generating integer valued discrete random variables
             Your random variables should thus only ever take integer values
             """
        assert(error_message == r.get_error("googlyboo"))

    def test_range(self):
        r = rv(expectation=0, vmin=-1, vmax=1)
        r.diagnosis = "range"
        error_message = """The googlyboo fall outside the allowed range of values for this
 type of random variable"""
        error_message += """\n The random variable should be between
 -1 and 1"""
        assert(error_message[-1] == r.get_error("googlyboo")[-1])

