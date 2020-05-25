class Pieniadz():
    """Klasa pozwala tworzyć obiekty pieniędzy.

    Każdy pieniądz posiada określoną wartość oraz walutę."""
    def __init__(self, wartosc, waluta: str = "zł"):
        self.__waluta = waluta
        if wartosc in [.01, .02, .05, .1, .2, .5, 1, 2, 5, 10, 20, 50]:
            self.__wartosc = int(wartosc * 100)
        else:
            raise Exception("Niedozwolona wartosc monety.")

    def wartosc(self):
        return self.__wartosc

    def waluta(self):
        return self.__waluta

    def __str__(self):
        return "{} {}".format(self.__wartosc/100, self.__waluta)

class Przechowywacz():
    """Klasa tworzy obiekt, przechowujący monety konkretnej waluty.

    Umożliwia dodawanie, usuwanie oraz liczenie wartości całkowitej przechowanych monet.
    Każdy rodzaj jest przechowywany w osobnej liście."""
    def __init__(self, waluta: str = "zł"):
        self.__przechowywane = {1: [], 2: [], 5: [], 10: [], 20: [], 50: [], 100: [], 200: [], 500: [], 1000: [], 2000: [], 5000: []}
        self.__waluta = waluta

    def lista(self):
        """Konwertuje przechowywane pieniądze na listę.

        Funkcja konwertuje wszystkie przechowane pieniądze na listę, zeruje przechowywane pieniądze
        aby uniknąć dublowania pieniędzy oraz zwraca wygenerowaną listę."""
        lista = []
        for kolumna in self.__przechowywane:
            if not len(self.__przechowywane[kolumna]) == 0:
                lista.extend(self.__przechowywane[kolumna])
        self.__przechowywane = {1: [], 2: [], 5: [], 10: [], 20: [], 50: [], 100: [], 200: [], 500: [], 1000: [], 2000: [], 5000: []}
        return lista

    def dodaj(self, p):
        if not isinstance(p, Pieniadz):
            raise Exception("Podany obiekt nie jest klasy Pieniadz().")
        else:
            if p.waluta() == self.__waluta:
                self.__przechowywane[p.wartosc()].append(p)
            else:
                raise Exception("Nieznana waluta.")

    def dodaj_wiele(self, p):
        if not isinstance(p, list):
            raise Exception("Podany obiekt nie jest listą.")
        else:
            for i in p:
                self.dodaj(i)

    def usun(self, wartosc):
        if len(self.__przechowywane[wartosc]) > 0:
            p = self.__przechowywane[wartosc].pop()
            return p

    def przeglad(self):
        """Funkcja zwraca listę zliczonych rodzajów posiadanych pieniędzy."""
        posiadane = []
        for kolumna in self.__przechowywane:
            posiadane.append(len(self.__przechowywane[kolumna]))
        return posiadane

    def suma(self):
        posiadane = self.przeglad()
        suma = 0
        i = 0
        for wartosc in self.__przechowywane:
            suma += posiadane[i] * wartosc
            i += 1
        return suma/100
