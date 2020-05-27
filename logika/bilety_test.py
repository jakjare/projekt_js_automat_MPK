"""Testy modułu bilety."""

import unittest
from bilety import Bilety, DrukowaneBilety

class TestBilety(unittest.TestCase):
    def test_wariant(self):
        """Sprawdzam czy mogę utworzyć bilet o nieobsługiwanym wariancie."""
        self.assertRaises(Exception, Bilety, "", 1)
        self.assertRaises(Exception, Bilety, "", [])
        self.assertRaises(Exception, Bilety, "", "coś innego")

if __name__ == '__main__':
    unittest.main()