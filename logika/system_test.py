"""Testy modułu system."""

import unittest

from logika import pieniadze
from logika import bilety
from logika import system

class TestZwróćResztę(unittest.TestCase):
    def setUp(self):
        self.kasa = pieniadze.Przechowywacz()                               # Tworzę kasę.

    def test_reszta_1(self):
        """Test poprawne wydanie reszty.

        Automat posiada dokładnie tyle ile trzeba."""
        self.kasa.dodaj(pieniadze.Pieniadz(2))                              # Dodaję 2 zł do kasy.
        self.reszta = system.zwróć_resztę(self.kasa, -200)                  # Sprawdzam funkcję.
        self.assertEqual(self.reszta[0][0], 200)

    def test_reszta_2(self):
        """Test poprawne wydanie reszty.

        Automat posiada dokładnie tyle ile trzeba, ale w mniejszych nominałach"""
        self.kasa.dodaj(pieniadze.Pieniadz(1))                              # Dodaję 1 zł do kasy.
        self.kasa.dodaj(pieniadze.Pieniadz(1))                              # Dodaję 1 zł do kasy.
        self.reszta = system.zwróć_resztę(self.kasa, -200)                  # Sprawdzam funkcję.
        self.wynik = self.reszta[0][0] + self.reszta[0][1]
        self.assertEqual(self.wynik, 200)

    def test_reszta_error_1(self):
        """Test kiedy automat nie może wydać reszty.

        Posiada pieniądze o wyższych nominałach."""
        self.kasa.dodaj(pieniadze.Pieniadz(5))                              # Dodaję 5 zł do kasy.
        self.assertRaises(system.ResztaException, system.zwróć_resztę, self.kasa, -200)

    def test_reszta_error_2(self):
        """Test kiedy automat nie może wydać reszty.

        Nie posiada pieniędzy."""
        self.kasa = pieniadze.Przechowywacz()
        self.assertRaises(system.ResztaException, system.zwróć_resztę, self.kasa, -200)

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.automat = system.System()                                      # Tworzę obiek automatu MPK.
        self.automat.dodaj_bilet(bilety.Bilety("1", "normalny", 3))         # Dodaję bilet, który kosztuje 3 zł.
        self.automat.dodaj_bilet(bilety.Bilety("1", "normalny", 1))         # Dodaję bilet, który kosztuje 1 zł.
        self.automat.dodaj_bilet(bilety.Bilety("1", "ulgowy", 1))           # Dodaję bilet, który kosztuje 2 zł.
        self.bilety = self.automat.bilety()

    def test_opis_1(self):
        """Bilet kupiony za odliczoną kwotę. Brak reszty."""
        self.automat.admin_kasa([pieniadze.Pieniadz(2)])                    # Dodaję 2 zł do kasy.
        self.automat.dodaj_bilet_do_koszyka(self.bilety["normalny"][0])     # Dodaję bilet do koszyka.
        self.automat.dodaj_pieniadz(pieniadze.Pieniadz(2))                  # Płacę 2 zł.
        self.reszta = self.automat.dodaj_pieniadz(pieniadze.Pieniadz(1))    # Płacę 1 zł.
        if self.reszta[0]:                                                  # Jeśli zwróciło True to wydrukuj bilet.
            self.reszta = self.automat.drukuj_bilety("", "")
        self.assertIsInstance(self.reszta[0], bilety.DrukowaneBilety)

    def test_opis_2(self):
        """Bilet kupiony płacąc więcej. Oczekiwany bilet i reszta."""
        self.automat.admin_kasa([pieniadze.Pieniadz(1)])                    # Dodaję 1 zł do kasy.
        self.automat.dodaj_bilet_do_koszyka(self.bilety["normalny"][0])     # Dodaję bilet do koszyka.
        self.automat.dodaj_pieniadz(pieniadze.Pieniadz(2))                  # Płacę 2 zł.
        self.reszta = self.automat.dodaj_pieniadz(pieniadze.Pieniadz(2))    # Płacę 2 zł, oczekuję reszty 1 zł.
        self.assertIsInstance(self.reszta[1][0], pieniadze.Pieniadz)        # Czy reszta jest pieniądzem?
        self.assertEqual(self.reszta[1][0].wartosc(), 100)                  # Czy pieniądz to oczekiwane 1 zł?
        if self.reszta[0]:                                                  # Jeśli zwróciło True to wydrukuj bilet.
            self.reszta = self.automat.drukuj_bilety("", "")
        self.assertIsInstance(self.reszta[0], bilety.DrukowaneBilety)       # Czy blilet jest wydrukowany?

    def test_opis_3(self):
        """Automat nie ma jak wydać reszty, nie drukuje biletów, zwraca wrzucone pieniądze.

        Jeśli automat nie może wydać reszty to wywoływana jest metoda anuluj_transakcje."""
        self.automat.dodaj_bilet_do_koszyka(self.bilety["normalny"][0])     # Dodaję bilet do koszyka.
        self.automat.dodaj_pieniadz(pieniadze.Pieniadz(2))                  # Płacę 2 zł.
        try:
            self.reszta = self.automat.dodaj_pieniadz(pieniadze.Pieniadz(2))# Płacę 2 zł, oczekuję reszty 1 zł.
        except system.ResztaException:                                      # Uruchamia się metoda anuluj_transakcje.
            self.reszta = self.automat.anuluj_transakcje()
        for i in self.reszta:
            self.assertIsInstance(i, pieniadze.Pieniadz)
            self.assertEqual(i.wartosc(), 200)

    def test_opis_4(self):
        """Zakup biletu płacąc po 1gr - suma stu monet 1gr ma być równa 1zł."""
        self.automat.dodaj_bilet_do_koszyka(self.bilety["normalny"][1])     # Dodaję bilet do koszyka.
        for i in range(99):
            self.automat.dodaj_pieniadz(pieniadze.Pieniadz(.01))            # Płacę 1 gr.
        self.reszta = self.automat.dodaj_pieniadz(pieniadze.Pieniadz(.01))  # Płacę 1 gr, oczekuję biletu.
        if self.reszta[0]:
            self.reszta = self.automat.drukuj_bilety("", "")
            self.assertIsInstance(self.reszta[0], bilety.DrukowaneBilety)  # Czy blilet jest wydrukowany?

    def test_opis_5(self):
        """Zakup dwóch różnych biletów naraz, automat sumuje ceny biletów i drukuje oba."""
        self.automat.dodaj_bilet_do_koszyka(self.bilety["normalny"][1])     # Dodaję bilet do koszyka.
        self.automat.dodaj_bilet_do_koszyka(self.bilety["ulgowy"][0])       # Dodaję bilet do koszyka.
        self.automat.dodaj_pieniadz(pieniadze.Pieniadz(2))                  # Płacę 2 zł.
        self.reszta = self.automat.dodaj_pieniadz(pieniadze.Pieniadz(2))    # Płacę 2 zł, oczekuję 2 biletów.
        if self.reszta[0]:
            self.reszta = self.automat.drukuj_bilety("", "")
            self.assertEqual(len(self.reszta), 2)                           # Czy dostałem 2 obiekty
            for i in self.reszta:
                self.assertIsInstance(i, bilety.DrukowaneBilety)            # Czy oba obiekty to wydrukowane bilety?

if __name__ == '__main__':
    unittest.main()

