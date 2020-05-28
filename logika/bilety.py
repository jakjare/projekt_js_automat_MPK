"""Obiekty biletów oraz biletów przetworzonych przez automat."""

class Bilety:
    """Klasa tworzy obiekty biletów do sprzedaży.

    Bilety będą używane w automacie oraz drukowane."""
    def __init__(self, nazwa: str, wariant: str, cena_zł):
        self.__nazwa = nazwa
        if not wariant in ["normalny", "ulgowy"]:
            raise Exception("Nieobsługiwany wariant biletu.")
        self.__wariant = wariant
        self.__cena_gr = int(cena_zł*100)

    def cena_gr(self):
        return self.__cena_gr

    def wariant(self):
        return self.__wariant

    def nazwa(self):
        return self.__nazwa

class DrukowaneBilety(Bilety):
    """Klasa tworzy obiekty biletów, które zostaną wyprodukowane przez automat.

    Teraz bilet zawiera więcej informacji: czas wydrukowania biletu, id automatu, który
    drukował ten bilet oraz zmienna sygnalizująca czy bilet został użyty."""

    def __init__(self, nazwa: str, wariant: str, czas: str, automat: str):
        super().__init__(nazwa, wariant, cena_zł=0)
        self.__czas = czas
        self.__id_automatu = automat
        self.__skasowany = False

    def __str__(self):
        return "Bilet {} - {}, z dnia {}, {}, skasowany: {}".format(self.nazwa(), self.wariant(),
                                                                    self.__czas, self.__id_automatu,
                                                                    ["Nie", "Tak"][self.__skasowany])

    def skasuj(self):
        self.__skasowany = True

    def skasowany(self):
        return self.__skasowany
