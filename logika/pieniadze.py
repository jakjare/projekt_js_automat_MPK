from logika import stale as st

class Pieniadz:
    """Klasa pozwala tworzyć obiekty pieniędzy.

    Każdy pieniądz posiada określoną wartość oraz walutę."""
    def __init__(self, wartosc, waluta: str = "zł"):
        self.__waluta = waluta
        if wartosc*100 in st.NOMINAŁY:
            self.__wartosc = int(wartosc * 100)
        else:
            raise Exception("Niedozwolona wartosc monety.")

    def wartosc(self):
        return self.__wartosc

    def waluta(self):
        return self.__waluta

    def __str__(self):
        return f"{self.__wartosc/100} {self.__waluta}"

class Przechowywacz:
    """Klasa tworzy obiekt, przechowujący monety konkretnej waluty.

    Umożliwia dodawanie, usuwanie oraz liczenie wartości całkowitej przechowanych monet.
    Każdy rodzaj jest przechowywany w osobnej liście."""
    def __init__(self, waluta: str = "zł"):
        self.__przechowywane = {i: 0 for i in st.NOMINAŁY}
        self.__waluta = waluta

    def lista(self):
        """Konwertuje przechowywane pieniądze na listę, którą zwraca.

        Funkcja konwertuje wszystkie przechowane pieniądze na listę, zeruje przechowywane pieniądze
        aby uniknąć dublowania pieniędzy oraz zwraca wygenerowaną listę."""
        lista = []
        for kolumna in self.__przechowywane:
            if not self.__przechowywane[kolumna] == 0:
                lista.extend([Pieniadz(kolumna/100) for i in range(self.__przechowywane[kolumna])])
        self.__przechowywane = {i: 0 for i in st.NOMINAŁY}
        return lista

    def dodaj(self, p):
        if not isinstance(p, Pieniadz):
            raise Exception("Podany obiekt nie jest klasy Pieniadz().")
        else:
            if p.waluta() == self.__waluta:
                self.__przechowywane[p.wartosc()] += 1
            else:
                raise Exception("Nieznana waluta.")

    def dodaj_wiele(self, p):
        if not isinstance(p, list):
            raise Exception("Podany obiekt nie jest listą.")
        else:
            for i in p:
                self.dodaj(i)

    def usun(self, wartosc):
        if wartosc not in self.__przechowywane:
            raise Exception("Nie przechowuję takich wartości.")
        if self.__przechowywane[wartosc] > 0:
            self.__przechowywane[wartosc] -= 1
            return Pieniadz(wartosc/100)

    def przeglad(self):
        """Funkcja zwraca listę zliczonych rodzajów posiadanych pieniędzy."""
        posiadane = []
        for kolumna in self.__przechowywane:
            posiadane.append(self.__przechowywane[kolumna])
        return posiadane

    def suma(self):
        posiadane = self.przeglad()
        suma = 0
        for wartosc, ilość in zip(self.__przechowywane, posiadane):
            suma += ilość * wartosc
        return suma/100
