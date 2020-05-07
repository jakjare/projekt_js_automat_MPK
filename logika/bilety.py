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
