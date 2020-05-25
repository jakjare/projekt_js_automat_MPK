from logika import *
from tkinter import Tk, Frame, LabelFrame, Label, messagebox
import tkinter as tk
import time

class Nagłówek(Frame):
    """Tworzy nagłówek dla GUI."""

    def __init__(self, okno_glowne: Tk):
        super().__init__(okno_glowne, bg="#00a2ff")
        self.__o_logo = tk.PhotoImage(file="projekt_js_automat_MPK\logo.png", width=80)
        Label(self, bg="#00a2ff", fg="white", image=self.__o_logo)\
            .pack(side=tk.LEFT, pady=10, padx=10)
        Label(self, width=46, text="Automat biletowy MPK", bg="#00a2ff", fg="white", font="Arial 20 bold underline")\
            .pack(side=tk.LEFT)
        self.__czas_naglowek = Label(self, width=17, bg="#00a2ff", fg="white", font="Arial 15 bold")
        self.__czas_naglowek.pack(side=tk.TOP, pady=5)

    def pobierz_czas(self):
        """Uruchamia pętlę zegara w nagłówku."""
        czas = time.localtime()
        self.__czas_naglowek.config(text=time.strftime("%d/%m/%Y %H:%M:%S", czas))
        def aktualizuj():
            czas = time.localtime()
            self.__czas_naglowek.config(text=time.strftime("%d/%m/%Y %H:%M:%S", czas))
            self.__czas_naglowek.after(1000, aktualizuj)
        aktualizuj()

class RamkaBilety(Frame):
    """Tworzy ramkę biletów dla GUI.

    Klasę trzeba zainicjalizować metodą inicjalizuj() podając zewnętrzne funkcje/metody, które
    będą wywoływane przy klikaniu przycisków funkcyjnych. Klasa tworzy dwie kolumny, segreguje
    bilety z automatu i umieszcza je w osobnych kolumnach. Do każdego biletu generuje przyciski
    funkcujne."""

    def __init__(self, okno_glowne: Tk):
        super().__init__(okno_glowne)

    def inicjalicuj(self, dodaj_bilet, usun_bilet, automat):
        lista_biletow = automat.bilety()
        i = 0
        j = 0
        for rodzaj in lista_biletow:
            for bilet in lista_biletow[rodzaj]:
                nazwa = "{} - {}\n\n{:.2f} zł".format(bilet.nazwa(), rodzaj, bilet.cena() / 100)
                Label(self, bg="#061981", text=nazwa, width=29, height=4, font="Arial 15", fg="white")\
                    .grid(row=i, column=j, padx=(18, 3), pady=2)
                for znak in range(1, 3):
                    b = Label(self, bg="#646464", width=8, height=4, font="Arial 15", fg="white")
                    if znak == 1:
                        b.configure(text="+")
                        b.bind("<Button-1>", dodaj_bilet)
                    else:
                        b.configure(text="-")
                        b.bind("<Button-1>", usun_bilet)
                    b.bilet = bilet
                    b.bind("<Enter>", lambda event: event.widget.configure(bg="#9e9e9e"))
                    b.bind("<Leave>", lambda event: event.widget.configure(bg="#646464"))
                    b.grid(row=i, column=j + znak, padx=2, pady=2)
                i += 1
            j += 3
            i = 0

class Koszyk(LabelFrame):
    """Tworzy ramkę koszyka dla GUI, która wyświetla listę biletów wybranych przez użytkownika."""

    def __init__(self, okno_glowne: Tk):
        super().__init__(okno_glowne, text="TWÓJ KOSZYK", font="Arial 20 bold")
        self.__okno = okno_glowne

    def aktualizuj_koszyk(self, automat, suma, limit=4):
        """Metoda aktualizuje listę biletów wyświetlaną przez obiekt klasy."""

        suma.configure(text="Do zapłaty: {:.2f} zł".format(automat.do_zaplaty()))
        self.destroy()
        koszyk = automat.koszyk()
        super().__init__(self.__okno, text="TWÓJ KOSZYK", font="Arial 20 bold")
        Label(self, text="Lp.", font="Arial 15 bold", width=5).grid(row=0, column=0, padx=2, pady=2)
        Label(self, text="Nazwa", font="Arial 15 bold", width=44).grid(row=0, column=1, padx=2, pady=2)
        Label(self, text="Rodzaj", font="Arial 15 bold", width=26).grid(row=0, column=2, padx=2, pady=2)
        Label(self, text="Cena", font="Arial 15 bold", width=8).grid(row=0, column=3, padx=2, pady=2)

        if limit >= len(koszyk):
            zasieg = 0
        else:
            zasieg = len(koszyk) - limit
        for i in range(zasieg, len(koszyk)):
            Label(self, text=str(i + 1), font="Arial 15", width=5)\
                .grid(row=i + 1, column=0, padx=2, pady=2)
            Label(self, text=str(koszyk[i].nazwa()), font="Arial 15", width=44)\
                .grid(row=i + 1, column=1, padx=2, pady=2)
            Label(self, text=str(koszyk[i].wariant()), font="Arial 15", width=26)\
                .grid(row=i + 1, column=2, padx=2, pady=2)
            Label(self, text=str("{:.2f} zł".format(koszyk[i].cena() / 100)), font="Arial 15", width=8)\
                .grid(row=i + 1, column=3, padx=2, pady=2)
        self.pack(side=tk.TOP, fill=tk.X, padx=20)

class Stopka(Frame):
    """Tworzy ramkę stopki dla domyślnego widoku GUI.

    Obiekt wyświetla przyciski funkcyjne oraz sumę do zapłaty."""

    def __init__(self, okno_glowne: Tk):
        super().__init__(okno_glowne)

    def inicjalizuj(self, suma, widok_koszyk, anuluj, zapłać):
        """Tworzy główny widok stopki, przypisuje funkcję/metody do przycisków."""

        suma.grid(row=0, column=0, padx=18, pady=2)
        b = Label(self, text="ZAPŁAĆ", bg="#139017", width=20, height=2, font="Arial 15", fg="black")
        b.bind("<Enter>", lambda event: event.widget.configure(bg="#92d050"))
        b.bind("<Leave>", lambda event: event.widget.configure(bg="#139017"))
        b.otwarty = True
        b.bind("<Button-1>", zapłać)
        b.grid(row=0, column=1, padx=18, pady=2)

        b = Label(self, text="SPRAWDŹ KOSZYK", bg="#061981", width=20, height=2, font="Arial 15", fg="white")
        b.bind("<Enter>", lambda event: event.widget.configure(bg="#465cfa"))
        b.bind("<Leave>", lambda event: event.widget.configure(bg="#061981"))
        b.otwarty = True
        b.bind("<Button-1>", widok_koszyk)
        b.grid(row=0, column=2, padx=18, pady=2)

        b = Label(self, text="ANULUJ", bg="red", width=20, height=2, font="Arial 15", fg="black")
        b.bind("<Enter>", lambda event: event.widget.configure(bg="#850000", fg="white"))
        b.bind("<Leave>", lambda event: event.widget.configure(bg="red", fg="black"))
        b.bind("<Button-1>", anuluj)
        b.grid(row=0, column=3, padx=18, pady=2)

class Alert(Frame):
    """Wyświetla wiadomość z informacją lub ostrzeżeniem.

    Odpowiednik messagebox w klasie tkinter."""

    def __init__(self, okno_glowne):
        super().__init__(okno_glowne)
        self.__wiadomość = Label(self, bg="black", width=29, height=4, font="Arial 20", fg="white")
        self.__wiadomość.pack()
        self.__przycisk = Label(self, text="OK", bg="grey", width=29, height=2, font="Arial 20", fg="white")
        self.__przycisk.bind("<Enter>", lambda event: event.widget.configure(bg="#465cfa"))
        self.__przycisk.bind("<Leave>", lambda event: event.widget.configure(bg="grey"))
        self.__przycisk.bind("<Button-1>", lambda event: self.place_forget())
        self.__przycisk.pack()

    def wyświetl(self, text, akcja = None):
        """Wyrzuca ramkę na ekran, opcjonalnie wywołuje funkcję."""

        self.__wiadomość.configure(text=text)
        self.place(x=550, y=450, anchor=tk.CENTER)
        if akcja != None:
            akcja

class Widok_zapłata(Frame):
    """Tworzy ramkę widoku do zapłaty - tabelka z pieniędzmi, które można wrzucić do automatu."""

    def __init__(self, okno_glowne):
        super().__init__(okno_glowne)
        self.__suma = Label(self, width=18, height=2, font="Arial 35 bold", fg="black", borderwidth=5, relief="solid")
        self.__suma.grid(row=0, column=0,padx=20, pady=20, columnspan=3)
        self.__ostrzeżenie = Label(self, width=25, height=3, font="Arial 25", fg="black")
        self.__ostrzeżenie.grid(row=0, column=3, padx=20, pady=20, columnspan=3)
        self.__pieniadze = {0.01: None, 0.02: None, 0.05: None,
                            0.1: None,  0.2: None,  0.5: None,
                            1: None,    2: None,    5: None,
                            10: None,   20: None,   50: None}

    def aktualizajca(self, kwota, ostrzeżenie = "Życzymy miłego dnia!"):
        """Aktualizuje kwotę do zapłaty oraz ostrzeżenie wyświetlane przez GUI."""

        self.__suma.configure(text="Do zapłaty: {:.2f} zł".format(kwota))
        self.__ostrzeżenie.configure(text=ostrzeżenie)

    def inicjalizuj(self, wrzuć, anuluj):
        i = 0
        j = 1
        for nazwa in self.__pieniadze:
            ścieżka = "projekt_js_automat_MPK/pieniądze/{}.png".format(str(nazwa))
            obiekt = tk.PhotoImage(file=ścieżka, width=120, height=120)
            self.__pieniadze[nazwa] = obiekt
            Label(self, image=obiekt).grid(row=j, column=i, padx=(18, 3), pady=2)
            b = Label(self, text="+", bg="#061981", width=4, height=2, font="Arial 37", fg="white")
            b.bind("<Enter>", lambda event: event.widget.configure(bg="#465cfa"))
            b.bind("<Leave>", lambda event: event.widget.configure(bg="#061981"))
            b.wartość = float(nazwa)
            b.bind("<Button-1>", wrzuć)
            b.grid(row=j+1, column=i, padx=(18, 3), pady=2)
            i += 1
            if i == 6:
                j = 3
                i = 0
        b = Label(self, width=25, height=3, font="Arial 25", fg="black", bg="red", text="Anuluj")
        b.bind("<Enter>", lambda event: event.widget.configure(bg="#850000", fg="white"))
        b.bind("<Leave>", lambda event: event.widget.configure(bg="red", fg="black"))
        b.bind("<Button-1>", anuluj)
        b.grid(row=5, column=3, padx=20, pady=20, columnspan=3)

class Automat():
    """Główna klasa GUI automatu MPK - obsługuje obiekt automatu w formie graficznej."""

    def __init__(self, okno_glowne: Tk, automat: system.System, id_automatu: str):
        self.__id_automatu = id_automatu
        self.__automat = automat
        self.__okno = okno_glowne
        self.__okno.title("Automat biletowy MPK")
        self.__okno.geometry("1100x900+40+40")
        self.__okno.resizable(False, False)
        self.__nagłówek = Nagłówek(self.__okno)
        self.__ramka = RamkaBilety(self.__okno)
        self.__koszyk = Koszyk(self.__okno)
        self.__stopka = Stopka(self.__okno)
        self.__suma = Label(self.__stopka, width=20, height=2, font="Arial 15 bold", fg="black")
        self.__alert = Alert(self.__okno)
        self.__widok_do_zapłaty = Widok_zapłata(self.__okno)

    def zamykanie(self):
        """Obsługa kończenia pracy programu."""

        if messagebox.askokcancel("Zamykanie", "Czy na pewno chcesz wyłączyć automat?"):
            self.__automat.admin_zamykanie()
            self.__okno.destroy()

    def dodaj_bilet(self, event):
        """Obsługa przycisków, które dodają bilet do koszyka."""

        if len(self.__automat.koszyk()) < 20:
            self.__automat.dodaj_bilet_do_koszyka(event.widget.bilet)
            self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        else:
            self.__alert.wyświetl("W koszyku może być \nmaksymalnie 20 biletów.")

    def usun_bilet(self, event):
        """Obsługa przycisków, które usuwają bilet z koszyka."""

        try:
            self.__automat.usun_bilet_z_koszyka(event.widget.bilet)
            self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        except system.UsuwanieBiletuException:
            event.widget.configure(bg="red")

    def anuluj(self, event=None):
        """Obsługa przycisków anuluj."""

        reszta = self.__automat.anuluj_transakcje()
        self.__ramka.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        self.__widok_do_zapłaty.aktualizajca(self.__automat.do_zaplaty())
        self.__widok_do_zapłaty.pack_forget()
        self.__stopka.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        if reszta != []:
            zwrot = []
            for obiekt in reszta:
                tmp = "{} {}".format(obiekt.wartosc()/100, obiekt.waluta())
                zwrot.append(tmp)
            messagebox.showinfo("DO TWOJEJ KIESZENI", "Automat MPK zwraca: {}".format(zwrot))

    def widok_koszyk(self, event):
        """Obsługa przycisku zmieniająca widok domyślny na widok całego koszyka i z powrotem."""

        if self.__automat.koszyk() != []:
            if event.widget.otwarty:
                event.widget.configure(text="WRÓĆ")
                event.widget.otwarty = False
                self.__ramka.pack_forget()
                self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma, 20)
            else:
                event.widget.configure(text="SPRAWDŹ KOSZYK")
                event.widget.otwarty = True
                self.__ramka.pack(side=tk.TOP, fill=tk.X, pady=10)
                self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        else:
            self.__alert.wyświetl("Nie wybrałeś żadnego biletu!")

    def zapłać(self, event):
        """Obsługa przycisku zapłać, przechodzi do widoku do zapłaty finalizującej transakcję."""

        if self.__automat.koszyk() != []:
            self.__ramka.pack_forget()
            self.__koszyk.pack_forget()
            self.__stopka.pack_forget()
            if self.__automat.admin_kasa()[0] == 0:
                self.__widok_do_zapłaty.aktualizajca(self.__automat.do_zaplaty(), "Tylko odliczona kwota!")
            elif self.__automat.admin_kasa()[0] < 40.:
                self.__widok_do_zapłaty.aktualizajca(self.__automat.do_zaplaty(), "Automat może nie wydać reszty.")
            else:
                self.__widok_do_zapłaty.aktualizajca(self.__automat.do_zaplaty())

            self.__widok_do_zapłaty.pack(side=tk.TOP, fill=tk.BOTH)
        else:
            self.__alert.wyświetl("Nie wybrałeś żadnego biletu!")

    def finalizuj(self, reszta):
        """Finalizuję transakcję, drukuję bilety, zwracam resztę użytkownikowi."""

        zwrot = []
        czas = time.localtime()
        czas = time.strftime("%d/%m/%Y/%H/%M/%S", czas)
        bilety = self.__automat.drukuj_bilety(czas, self.__id_automatu)
        for bilet in bilety:
            zwrot.append(str(bilet))

        if reszta != []:
            self.__alert.wyświetl("Automat wyda resztę.")
            for obiekt in reszta:
                tmp = "{} {}".format(obiekt.wartosc() / 100, obiekt.waluta())
                zwrot.append(tmp)
        self.__ramka.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        self.__widok_do_zapłaty.aktualizajca(self.__automat.do_zaplaty())
        self.__widok_do_zapłaty.pack_forget()
        self.__stopka.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.__automat.koszyk()
        messagebox.showinfo("DO TWOJEJ KIESZENI", "Automat MPK zwraca: {}".format(zwrot))

    def wrzuć_pieniądz(self, event):
        """Obsługa przycisku wrzucania pieniądza do automatu."""

        try:
            zwrot = self.__automat.dodaj_pieniadz(pieniadze.Pieniadz(event.widget.wartość))
            self.__widok_do_zapłaty.aktualizajca(self.__automat.do_zaplaty())
            if zwrot != None:
                if zwrot[0]:
                    self.finalizuj(zwrot[1])

        except system.ResztaException:
            self.__alert.wyświetl("Nie mogę wydać reszty!", self.anuluj())

    def start(self):
        """Metoda uruchamia GUI."""

        self.__okno.protocol("WM_DELETE_WINDOW", self.zamykanie)
        self.__nagłówek.pobierz_czas()
        self.__nagłówek.pack(side=tk.TOP, fill=tk.X)
        self.__ramka.inicjalicuj(self.dodaj_bilet, self.usun_bilet, self.__automat)
        self.__ramka.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        self.__stopka.inicjalizuj(self.__suma, self.widok_koszyk, self.anuluj, self.zapłać)
        self.__stopka.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.__widok_do_zapłaty.inicjalizuj(self.wrzuć_pieniądz, self.anuluj)
