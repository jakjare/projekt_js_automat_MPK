from logika import bilety, pieniadze, stale as st
from _collections import defaultdict

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
    for i in range(1, len(wartosci) + 1):
        for x in range(kasa[-i]):
            if wartosci[-i] + do_zapłaty <= 0:
                do_zapłaty += wartosci[-i]
                kasa[-i] -= 1
                reszta.append(wartosci[-i])
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

    def dodaj_bilet(self, b):
        if not isinstance(b, bilety.Bilety):
            raise Exception("Podany obiekt nie jest klasy Bilety().")
        else:
            self.__bilety[b.wariant()].append(b)

    def bilety(self):
        """Zwraca kopię listy dostępnych biletów."""
        return self.__bilety.copy()

    def admin_kasa(self, do_kasy = None):
        """Pozwala administratorowi dodać pieniądze do kasy automatu.

        Wyświetla stan kasy automatu po dodaniu."""
        if not do_kasy == None:
            self.__kasa.dodaj_wiele(do_kasy)
        print("ADMIN:\tSuma w kasie: {}\tPrzegląd: {}".format(self.__kasa.suma(), self.__kasa.przeglad()))
        return self.__kasa.suma(), self.__kasa.przeglad()

    def admin_zamykanie(self):
        with open("kasa.dat", "w") as plik:
            do_pliku = self.__kasa.lista()
            for obiekt in  do_pliku:
                plik.write(f"{obiekt}\n")

    def do_zaplaty(self):
        return self.__do_zaplaty/100

    def dodaj_bilet_do_koszyka(self, b):
        if not isinstance(b, bilety.Bilety):
            raise Exception("Podany obiekt nie jest klasy Bilety().")
        else:
            self.__koszyk[b] += 1
            self.__do_zaplaty += b.cena()

    def usun_bilet_z_koszyka(self, b):
        if b in self.__koszyk:
            if self.__koszyk[b] == 1:
                self.__koszyk.pop(b)
            else:
                self.__koszyk[b] -= 1
            self.__do_zaplaty -= b.cena()
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

    def dodaj_pieniadz(self, p):
        """Funkcja do wurzania pieniędzy przez użytkownika.

        Jeśli kwota wrzucona przekroczy wartość kwoty do zapłaty uruchamia się proces wydawania reszty przy użyciu
        funkcji zwróć_resztę(). Automat najpierw sprawdza czy posiada takie pieniądze, które może wydać.
        Jeśli tak, to wydaje resztę i drukuje bilety. Natomiast jeśli wrzucona kwota zrówna się z wartością do zapłaty,
        wtedy automat po prostu wydrukuje bilety. Kiedy nie wystąpi żaden z powyższych przypadków automat
        poczeka na kolejne pieniądze. Metoda zwraca listę monet, które chce zwrócić użytkownikowi lub pustą listę,
        kiedy nie potrzebuje nic zwracać. Kiedy automat nie może wydać reszty zwraca pieniądze wrzucone
        przez użytkownika wcześniej."""
        if not isinstance(p, pieniadze.Pieniadz):
            raise Exception("Podany obiekt nie jest klasy Pieniadz().")
        else:
            self.__transakcja.dodaj(p)
            self.__do_zaplaty -= p.wartosc()
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

"""
automat = System()
b1 = bilety.Bilety("20-minutowy", "normalny", 3)    #Tworzę obiekty biletów
b2 = bilety.Bilety("20-minutowy", "ulgowy", 1.7)
automat.dodaj_bilet(b1)
automat.dodaj_bilet(b2)
xx = automat.bilety()
print("Do zapłaty: {}".format(automat.do_zaplaty()))
automat.dodaj_bilet_do_koszyka(xx["normalny"][0])   #Wybieram bilety, które chcę kupić
automat.dodaj_bilet_do_koszyka(xx["normalny"][0])
print(automat.koszyk())
print("Do zapłaty: {}".format(automat.do_zaplaty()))
suma = lambda suma: suma += i for i in automat.koszyk().values():
    suma += i
print("xx",suma)
automat.usun_bilet_z_koszyka(xx["normalny"][0])
automat.usun_bilet_z_koszyka(xx["normalny"][0])
print(automat.koszyk())
print("Do zapłaty: {}".format(automat.do_zaplaty()))

xxx =defaultdict(int)
print(xxx.values())

b1 = bilety.Bilety("20-minutowy", "normalny", 3)    #Tworzę obiekty biletów
b2 = bilety.Bilety("20-minutowy", "ulgowy", 1.7)
xxx =defaultdict(int)
xxx[b1] += 1
print(xxx.keys()[0])

"""

"""# Test działania klasy System() w wariancie bez wydawania reszty

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

p1 = pieniadze.Pieniadz(2)                          #Generuję pieniądze do zapłacenia za bilety
p2 = pieniadze.Pieniadz(2)
p3 = pieniadze.Pieniadz(2)
automat.dodaj_pieniadz(p1)                          #Płacę za bilety tak aby automat nie musiał wydawać reszty
automat.dodaj_pieniadz(p2)
automat.dodaj_pieniadz(p3)

print("Do zapłaty: {}".format(automat.do_zaplaty()))
automat.admin_kasa()                                #Sprawdzam stan kasy"""


"""# Test działania klasy System() w wariancie z możliwością wydania reszty

automat = System()                                  #Tworzę obiek automatu MPK
b1 = bilety.Bilety("20-minutowy", "normalny", 3)    #Tworzę obiekt biletu
automat.dodaj_bilet(b1)                             #Dodaję bilet do automatu
kasa_automatu = []                                  #Generuję pieniądze dla automatu
for i in range(100):
    kasa_automatu.append(pieniadze.Pieniadz(0.01))
automat.admin_kasa(kasa_automatu)                   #Dodaję pieniądze do kasy w automacie
del kasa_automatu

xx = automat.bilety()
print("Do zapłaty: {}".format(automat.do_zaplaty()))
automat.dodaj_bilet_do_koszyka(xx["normalny"][0])   #Wybieram bilety, które chcę kupić

print("Do zapłaty: {}".format(automat.do_zaplaty()))

p1 = pieniadze.Pieniadz(2)                          #Generuję pieniądze do zapłacenia za bilety
p2 = pieniadze.Pieniadz(2)
p3 = pieniadze.Pieniadz(10)
automat.dodaj_pieniadz(p1)                          #Płacę za bilety tak aby automat wydał resztę
automat.dodaj_pieniadz(p2)

print("Do zapłaty: {}".format(automat.do_zaplaty()))
automat.admin_kasa()                                #Sprawdzam stan kasy"""


"""# Test działania klasy System() w wariancie z możliwością wydania reszty

automat = System()                                  #Tworzę obiek automatu MPK
b1 = bilety.Bilety("20-minutowy", "normalny", 3)    #Tworzę obiekt biletu
automat.dodaj_bilet(b1)                             #Dodaję bilet do automatu
kasa_automatu = []                                  #Generuję pieniądze dla automatu
for i in range(30):
    kasa_automatu.append(pieniadze.Pieniadz(0.01))
automat.admin_kasa(kasa_automatu)                   #Dodaję pieniądze do kasy w automacie
del kasa_automatu

xx = automat.bilety()
print("Do zapłaty: {}".format(automat.do_zaplaty()))
automat.dodaj_bilet_do_koszyka(xx["normalny"][0])   #Wybieram bilety, które chcę kupić

print("Do zapłaty: {}".format(automat.do_zaplaty()))

p1 = pieniadze.Pieniadz(2)                          #Generuję pieniądze do zapłacenia za bilety
p2 = pieniadze.Pieniadz(2)

try:
    automat.dodaj_pieniadz(p1)                      #Płacę za bilety tak aby automat wydał resztę
    automat.dodaj_pieniadz(p2)
except ResztaException:
    zwrocone = automat.anuluj_transakcje()

print("Do zapłaty: {}, zwrócone: {}".format(automat.do_zaplaty(), zwrocone))
automat.admin_kasa()                                #Sprawdzam stan kasy"""
