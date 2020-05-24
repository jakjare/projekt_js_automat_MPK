class Bilety():
    """Klasa tworzy obiekty biletów do sprzedaży.

    Bilety będą używane w automacie oraz drukowane."""
    def __init__(self, nazwa: str, wariant: str, cena):
        self.__nazwa = nazwa
        if not wariant in ["normalny", "ulgowy"]:
            raise Exception("Nieobsługiwany wariant biletu.")
        else:
            self.__wartiant = wariant
            self.__cena = int(cena*100)

    def cena(self):
        return self.__cena

    def wariant(self):
        return self.__wartiant

    def nazwa(self):
        return self.__nazwa

class DrukowaneBilety(Bilety):
    """Klasa tworzy obiekty biletów, które zostaną wyprodukowane przez automat.

    Teraz bilet zawiera więcej informacji: czas wydrukowania biletu, id automatu, który
    drukował ten bilet oraz zmienna sygnalizująca czy bilet został użyty."""

    def __init__(self, nazwa: str, wariant: str, cena, czas: str, automat: str):
        super().__init__(nazwa, wariant, cena)
        self.__czas = czas
        self.__id_automatu = automat
        self.__skasowany = False

    def __str__(self):
        if self.__skasowany:
            return "Bilet {} - {}, z dnia {}, {}, skasowany: Tak".format(self.nazwa(), self.wariant(), self.__czas,self.__id_automatu)
        return "Bilet {} - {}, z dnia {}, {}, skasowany: Nie".format(self.nazwa(), self.wariant(), self.__czas, self.__id_automatu)

    def skasuj(self):
        self.__skasowany = True

    def skasowany(self):
        return self.__skasowany