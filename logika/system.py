from logika import bilety
from logika import pieniadze

class System():
    """Klasa System() obsługuje całą logikę działania automatu MPK.

    """
    def __init__(self, waluta: str = "zł"):
        self.__bilety = {"normalny": [], "ulgowy": []}
        self.__kasa = pieniadze.Przechowywacz(waluta)
        self.__transakcja = pieniadze.Przechowywacz(waluta)
        self.__koszyk = []
        self.__do_zaplaty = 0

    def dodaj_bilet(self, b):
        if not isinstance(b, bilety.Bilety):
            raise Exception("Podany obiekt nie jest klasy Bilety().")
        else:
            self.__bilety[b.wariant()].append(b)

    def bilety(self):
        """Zwraca kopię listy dostępnych biletów."""
        return self.__bilety.copy()

    def admin_kasa(self, do_kasy = []):
        """Pozwala administratorowi dodać pieniądze do kasy automatu.

        Wyświetla stan kasy automatu po dodaniu."""
        if not len(do_kasy) == 0:
            self.__kasa.dodaj_wiele(do_kasy)
        print("\nADMIN:\tSuma w kasie: {}\tPrzegląd: {}".format(self.__kasa.suma(), self.__kasa.przeglad()))

    def do_zaplaty(self):
        return self.__do_zaplaty/100

    def dodaj_bilet_do_koszyka(self, b):
        if not isinstance(b, bilety.Bilety):
            raise Exception("Podany obiekt nie jest klasy Bilety().")
        else:
            self.__koszyk.append(b)
            self.__do_zaplaty += b.cena()

    def usun_bilet_z_koszyka(self, b):
        if b in self.__koszyk:
            self.__koszyk.remove(b)
            self.__do_zaplaty -= b.cena()
        else:
            raise Exception("Nie ma takiego biletu w koszyku.")

    def koszyk(self):
        """Zwraca kopię listy biletów dodanych do koszyka."""
        return self.__koszyk.copy()

    def drukuj_bilety(self):
        print("Drukuję bilety.")

    def dodaj_pieniadz(self, p):
        if not isinstance(p, pieniadze.Pieniadz):
            raise Exception("Podany obiekt nie jest klasy Pieniadz().")
        else:
            self.__transakcja.dodaj(p)
            self.__do_zaplaty -= p.wartosc()
            if self.do_zaplaty() == 0:
                self.__kasa.dodaj_wiele(self.__transakcja.lista())
                self.drukuj_bilety()
            elif self.do_zaplaty() < 0:
                print("Transakcja z resztą.")
            else:
                pass




# Test działania klasy System() w wariancie bez wydawania reszty

automat = System()                                  #Tworzę obiek automatu MPK
b1 = bilety.Bilety("20-minutowy", "normalny", 3)    #Tworzę obiekty biletów
b2 = bilety.Bilety("20-minutowy", "ulgowy", 1.7)
automat.dodaj_bilet(b1)                             #Dodaję bilety do automatu
automat.dodaj_bilet(b2)
kasa_automatu = []                                  #Generuję pieniądze dla automatu
for i in range(87):
    kasa_automatu.append(pieniadze.Pieniadz(5))
    kasa_automatu.append(pieniadze.Pieniadz(2))
    kasa_automatu.append(pieniadze.Pieniadz(1))
    kasa_automatu.append(pieniadze.Pieniadz(0.1))
    kasa_automatu.append(pieniadze.Pieniadz(.2))
    kasa_automatu.append(pieniadze.Pieniadz(.5))
    kasa_automatu.append(pieniadze.Pieniadz(.01))
automat.admin_kasa(kasa_automatu)                   #Dodaję pieniądze do kasy w automacie
del kasa_automatu

xx = automat.bilety()
print("Do zapłaty: {}".format(automat.do_zaplaty()))
automat.dodaj_bilet_do_koszyka(xx["normalny"][0])   #Wybieram bilety, które chcę kupić
automat.dodaj_bilet_do_koszyka(xx["normalny"][0])

print("Do zapłaty: {}".format(automat.do_zaplaty()))

p1 = pieniadze.Pieniadz(1)                          #Generuję pieniądze do zapłacenia za bilety
p2 = pieniadze.Pieniadz(5)
automat.dodaj_pieniadz(p1)                          #Płacę za bilety tak aby automat nie musiał wydawać reszty
automat.dodaj_pieniadz(p2)

print("Do zapłaty: {}".format(automat.do_zaplaty()))
automat.admin_kasa()                                #Sprawdzam stan kasy