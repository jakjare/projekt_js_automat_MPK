"""Testy modułu bilety."""

import unittest

from logika import bilety as b

class TestBilety(unittest.TestCase):
    def test_wariant(self):
        """Sprawdzam czy mogę utworzyć bilet o nieobsługiwanym wariancie."""
        self.assertRaises(Exception, b.Bilety, "", 1)
        self.assertRaises(Exception, b.Bilety, "", [])
        self.assertRaises(Exception, b.Bilety, "", "coś innego")

if __name__ == '__main__':
    unittest.main()