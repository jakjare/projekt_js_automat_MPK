"""Testy modułu pieniadze."""

import unittest

from logika import pieniadze as p

class TestPieniadz(unittest.TestCase):
    def test_wartość(self):
        """Sprawdzam czy mogę utworzyć Pieniądz o wartości niedozwolonej."""
        self.assertRaises(Exception, p.Pieniadz, "123")
        self.assertRaises(Exception, p.Pieniadz, [])
        self.assertRaises(Exception, p.Pieniadz, {})

class TestPrzechowywacz(unittest.TestCase):
    def setUp(self):
        self.p = p.Przechowywacz("PLN")

    def test_dodawanie(self):
        """Test na dodawanie do przechowywacza czegoś innego niż Pieniadz."""
        self.assertRaises(Exception, self.p.dodaj, {})
        self.assertRaises(Exception, self.p.dodaj, [])
        self.assertRaises(Exception, self.p.dodaj, 1)
        self.assertRaises(Exception, self.p.dodaj, "")

    def test_dodanie_waluta(self):
        """Test na dodawanie do przechowywacza pieniądza o innej walucie."""
        self.assertRaises(Exception, self.p.dodaj, p.Pieniadz(2, "USD"))

    def test_usuwanie(self):
        """Test na usuwanie czegość czego nie ma."""
        self.assertRaises(Exception, self.p.usun, "2")

if __name__ == '__main__':
    unittest.main()