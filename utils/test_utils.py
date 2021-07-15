import numpy as np
import numpy.testing as nptest
import unittest
import utils

class TestUtils(unittest.TestCase):
    def test_divide_zeros(self):
        input = np.zeros((64, 64))
        expected = np.zeros((4, 4, 16, 16))
        actual = utils.divide(input, (4, 4))

        self.assertTrue((expected == actual).all()) 

    def test_divide_small(self):
        input = np.array([
            [1, 2, 3, 4],
            [2, 3, 4, 5],
            [3, 4, 5, 6],
            [4, 5, 6, 7],
        ])
        expected = np.zeros((2, 2, 2, 2))
        expected[0, 0] = np.array([[1, 2], [2, 3]])
        expected[1, 0] = np.array([[3, 4], [4, 5]])
        expected[0, 1] = np.array([[3, 4], [4, 5]])
        expected[1, 1] = np.array([[5, 6], [6, 7]])
        
        actual = utils.divide(input, (2, 2))

        nptest.assert_array_equal(expected, actual)

if __name__ == '__main__':
    unittest.main()