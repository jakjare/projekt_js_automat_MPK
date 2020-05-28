"""Moduł obsługuje całą logikę działania automatu."""

from collections import defaultdict
from logika import bilety
from logika import pieniadze
from logika import stale as st

class ResztaException(Exception):
    """Klasa ResztaException() dziedziczy po klasie Exception.

    Klasa jest wywoływana w momencie, kiedy automat nie może wydać reszty z podanych przez
    użytkownika monet."""
    def __init__(self):
        super().__init__("Nie mam jak wydać reszty.")

class UsuwanieBiletuException(Exception):
    """Klasa UsuwanieBiletuException() dziedziczy po klasie Exception.

    Klasa jest wywoływana w momencie, kiedy użytkownik chce usunąć bilet, którego nie ma."""
    def __init__(self):
        super().__init__("Nie ma takiego biletu w koszyku.")

def zwróć_resztę(kasa: pieniadze.Przechowywacz, do_zapłaty: int):
    """Funkcja zwraca pieniądze reszty wyciągnięte z kasy.

    Jeśli nie można zwrócić reszty wywoływany jest wyjątek ResztaException()."""
    wartosci = st.NOMINAŁY
    kasa = kasa.przeglad()
    reszta = []
    for i in range(len(wartosci)-1, -1, -1):
        for j in range(kasa[i]):
            if wartosci[i] + do_zapłaty <= 0:
                do_zapłaty += wartosci[i]
                kasa[i] -= 1
                reszta.append(wartosci[i])
            else:
                break
    if do_zapłaty < 0:
        raise ResztaException()
    return reszta, do_zapłaty

class System():
    """Klasa System() obsługuje całą logikę działania automatu MPK.

    Obsługuję całą logikę działania automatu MPK."""
    def __init__(self, waluta: str = "zł"):
        self.__bilety = {"normalny": [], "ulgowy": []}
        self.__kasa = pieniadze.Przechowywacz(waluta)
        self.__transakcja = pieniadze.Przechowywacz(waluta)
        self.__koszyk = defaultdict(int)
        self.__do_zaplaty = 0

    def dodaj_bilet(self, bilet):
        if not isinstance(bilet, bilety.Bilety):
            raise Exception("Podany obiekt nie jest klasy Bilety().")
        self.__bilety[bilet.wariant()].append(bilet)

    def bilety(self):
        """Zwraca kopię listy dostępnych biletów."""
        return self.__bilety.copy()

    def admin_kasa(self, do_kasy=None):
        """Pozwala administratorowi dodać pieniądze do kasy automatu.

        Wyświetla stan kasy automatu po dodaniu."""
        if do_kasy is not None:
            self.__kasa.dodaj_wiele(do_kasy)
        return self.__kasa.suma(), self.__kasa.przeglad()

    def admin_zamykanie(self):
        with open("kasa.dat", "w") as plik:
            do_pliku = self.__kasa.lista()
            for obiekt in  do_pliku:
                plik.write(f"{obiekt}\n")

    def do_zaplaty(self):
        """Zwraca kwotę do zapłaty w zł."""
        return self.__do_zaplaty/100

    def dodaj_bilet_do_koszyka(self, bilet):
        if not isinstance(bilet, bilety.Bilety):
            raise Exception("Podany obiekt nie jest klasy Bilety().")
        self.__koszyk[bilet] += 1
        self.__do_zaplaty += bilet.cena()

    def usun_bilet_z_koszyka(self, bilet):
        if bilet in self.__koszyk:
            if self.__koszyk[bilet] == 1:
                self.__koszyk.pop(bilet)
            else:
                self.__koszyk[bilet] -= 1
            self.__do_zaplaty -= bilet.cena()
        else:
            raise UsuwanieBiletuException()

    def koszyk(self):
        """Zwraca kopię listy biletów dodanych do koszyka."""
        return self.__koszyk.copy()

    def drukuj_bilety(self, czas, numer_automatu):
        """Zwraca wyprodukowane obiekty biletów.

        Wyprodukowane bilety zostają oznaczone czasem wydruku, id automatu
        oraz zmienną czy bilet został skasowany."""
        wyniki = []
        for bilet in self.__koszyk:
            wyniki.append(bilety.DrukowaneBilety(bilet.nazwa(), bilet.wariant(), czas, numer_automatu))
        self.__koszyk = defaultdict(int)
        return wyniki

    def anuluj_transakcje(self):
        self.__koszyk = defaultdict(int)
        self.__do_zaplaty = 0
        return self.__transakcja.lista()

    def dodaj_pieniadz(self, pieniądz):
        """Funkcja do wurzania pieniędzy przez użytkownika.

        Jeśli kwota wrzucona przekroczy wartość kwoty do zapłaty uruchamia się proces wydawania reszty przy użyciu
        funkcji zwróć_resztę(). Automat najpierw sprawdza czy posiada takie pieniądze, które może wydać.
        Jeśli tak, to wydaje resztę i drukuje bilety. Natomiast jeśli wrzucona kwota zrówna się z wartością do zapłaty,
        wtedy automat po prostu wydrukuje bilety. Kiedy nie wystąpi żaden z powyższych przypadków automat
        poczeka na kolejne pieniądze. Metoda zwraca listę monet, które chce zwrócić użytkownikowi lub pustą listę,
        kiedy nie potrzebuje nic zwracać. Kiedy automat nie może wydać reszty zwraca pieniądze wrzucone
        przez użytkownika wcześniej."""
        if not isinstance(pieniądz, pieniadze.Pieniadz):
            raise Exception("Podany obiekt nie jest klasy Pieniadz().")
        else:
            self.__transakcja.dodaj(pieniądz)
            self.__do_zaplaty -= pieniądz.wartosc()
            if self.__do_zaplaty == 0:
                self.__kasa.dodaj_wiele(self.__transakcja.lista())
                return True, []
            elif self.__do_zaplaty < 0:
                reszta, self.__do_zaplaty = zwróć_resztę(self.__kasa, self.__do_zaplaty)
                self.__kasa.dodaj_wiele(self.__transakcja.lista())
                for pieniadz in reszta:
                    self.__transakcja.dodaj(self.__kasa.usun(pieniadz))
                return True, self.__transakcja.lista()
            return False, []
