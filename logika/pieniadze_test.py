"""Testy modułu pieniadze."""

import unittest
from pieniadze import Pieniadz, Przechowywacz

class TestPieniadz(unittest.TestCase):
    def test_wartość(self):
        """Sprawdzam czy mogę utworzyć Pieniądz o wartości niedozwolonej."""
        self.assertRaises(Exception, Pieniadz, "123")
        self.assertRaises(Exception, Pieniadz, [])
        self.assertRaises(Exception, Pieniadz, {})

class TestPrzechowywacz(unittest.TestCase):
    def test_dodawanie(self):
        """Test na dodawanie do przechowywacza czegoś innego niż Pieniadz."""
        self.p = Przechowywacz()
        self.assertRaises(Exception, self.p.dodaj, {})
        self.assertRaises(Exception, self.p.dodaj, [])
        self.assertRaises(Exception, self.p.dodaj, 1)
        self.assertRaises(Exception, self.p.dodaj, "")

    def test_dodanie_waluta(self):
        """Test na dodawanie do przechowywacza pieniądza o innej walucie."""
        self.p = Przechowywacz("PLN")
        self.assertRaises(Exception, self.p.dodaj, Pieniadz(2, "USD"))

    def test_usuwanie(self):
        """Test na usuwanie czegość czego nie ma."""
        self.p = Przechowywacz()
        self.assertRaises(Exception, self.p.usun, "2")

if __name__ == '__main__':
    unittest.main()