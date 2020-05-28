from logika import stale as st

class Pieniadz:
    """Klasa pozwala tworzyć obiekty pieniędzy.

    Każdy pieniądz posiada określoną wartość oraz walutę."""
    def __init__(self, wartość_zł, waluta: str = "zł"):
        self.__waluta = waluta
        if wartość_zł*100 in st.NOMINAŁY_GR:
            self.__wartość_gr = int(wartość_zł * 100)
        else:
            raise Exception("Niedozwolona wartosc monety.")

    def wartość_gr(self):
        return self.__wartość_gr

    def waluta(self):
        return self.__waluta

    def __str__(self):
        return f"{self.__wartość_gr/100} {self.__waluta}"

class Przechowywacz:
    """Klasa tworzy obiekt, przechowujący monety konkretnej waluty.

    Umożliwia dodawanie, usuwanie oraz liczenie wartości całkowitej przechowanych monet.
    Każdy rodzaj jest przechowywany w osobnej liście."""
    def __init__(self, waluta: str = "zł"):
        self.__przechowywane = {i: 0 for i in st.NOMINAŁY_GR}
        self.__waluta = waluta

    def lista(self):
        """Konwertuje przechowywane pieniądze na listę, którą zwraca.

        Funkcja konwertuje wszystkie przechowane pieniądze na listę, zeruje przechowywane pieniądze
        aby uniknąć dublowania pieniędzy oraz zwraca wygenerowaną listę."""
        lista = []
        for kolumna in self.__przechowywane:
            if not self.__przechowywane[kolumna] == 0:
                lista.extend([Pieniadz(wartość_zł=kolumna/100) for i in range(self.__przechowywane[kolumna])])
        self.__przechowywane = {i: 0 for i in st.NOMINAŁY_GR}
        return lista

    def dodaj(self, pieniądz):
        if not isinstance(pieniądz, Pieniadz):
            raise Exception("Podany obiekt nie jest klasy Pieniadz().")
        else:
            if pieniądz.waluta() == self.__waluta:
                self.__przechowywane[pieniądz.wartość_gr()] += 1
            else:
                raise Exception("Nieznana waluta.")

    def dodaj_wiele(self, lista_pieniędzy):
        if not isinstance(lista_pieniędzy, list):
            raise Exception("Podany obiekt nie jest listą.")
        else:
            for i in lista_pieniędzy:
                self.dodaj(i)

    def usun(self, wartość):
        if wartość not in self.__przechowywane:
            raise Exception("Nie przechowuję takich wartości.")
        if self.__przechowywane[wartość] > 0:
            self.__przechowywane[wartość] -= 1
            return Pieniadz(wartość_zł=(wartość/100))

    def przeglad(self):
        """Funkcja zwraca listę zliczonych rodzajów posiadanych pieniędzy."""
        posiadane = []
        for kolumna in self.__przechowywane:
            posiadane.append(self.__przechowywane[kolumna])
        return posiadane

    def suma_zł(self):
        """Zwraca sumę w zł."""
        posiadane = self.przeglad()
        suma = 0
        for wartość_gr, ilość in zip(self.__przechowywane, posiadane):
            suma += ilość * wartość_gr
        return suma/100
