import unittest
import plot_gtex
import random



class TestLinearSearch(unittest.TestCase):
        
    def test_linear_search_empty(self):
        assert plot_gtex.linear_search("string", []) == -1

    def test_linear_search_small(self):
        l = [100, 200, 300, 400, 500]
        assert plot_gtex.linear_search(500, l) == 4

    def test_linear_search_large(self):
        size = random.randint(1, 10000)
        rand_index = random.randint(0, size+1)
        l = [1 for _ in range(size)]
        l[rand_index] = 0
        assert plot_gtex.linear_search(0, l) == rand_index

