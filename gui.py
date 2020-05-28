"""Moduł obsługuje GUI dla automatu."""

import time

from tkinter import messagebox
import tkinter as tk
from logika import pieniadze
from logika import system

KOLOR_FONT_JASNY = "white"              #Kolor fontu w nagłówku.
KOLOR_FONT_CIEMNY = "black"             #Kolor fontu zawartości.
FONT_N = "Arial 20"                     #Atrybuty fontu nagłówkowego.
FONT_ZAWARTOŚĆ = "Arial 15"             #Atrybuty fontu zawartości.
FONT_N_WIDOK2 = "Arial 35 bold"         #Atrybuty fontu nagłówkowego dla widoku do zapłaty.
FONT_WIDOK2 = "Arial 25"                #Atrybuty fontu dla widoku do zapłaty.
KOLOR_NAGŁÓWEK = "#00a2ff"              #Kolor tła w nagłówku.
KOLOR_BILET = "#061981"                 #Kolor tła przycisków biletowych.
KOLOR_BILET_F = "#646464"               #Kolor tła przycisków biletowych +/-.
KOLOR_BILET_F_HOVER = "#9e9e9e"         #Kolor tła przycisków biletowych +/- po najechaniu myszką.
KOLOR_ALERT = "black"                   #Kolor tła Alert().
KOLOR_ALERT_F = "grey"                  #Kolor tła przycisku funkcyjnego w Alert().
KOLOR_ALERT_HOVER = "#465cfa"           #Kolor tła przycisku funkcyjnego po najechaniu myszką.
KOLOR_BUTTON1 = "#139017"               #Kolor przycisku ZAPŁAĆ.
KOLOR_BUTTON1_HOVER = "#92d050"         #Kolor przycisku ZAPŁAĆ po najechaniu myszką.
KOLOR_BUTTON2 = "#061981"               #Kolor przycisku SPRAWDŹ KOSZYK.
KOLOR_BUTTON2_HOVER = "#465cfa"         #Kolor przycisku SPRAWDŹ KOSZYK po najechaniu myszką.
KOLOR_BUTTON3 = "red"                   #Kolor przycisku ANULUJ.
KOLOR_BUTTON3_HOVER = "#850000"         #Kolor przycisku ANULUJ po najechaniu myszką.

class Nagłówek(tk.Frame):
    """Tworzy nagłówek dla GUI."""
    def __init__(self, okno_glowne: tk.Tk):
        super().__init__(okno_glowne, bg=KOLOR_NAGŁÓWEK)
        self.__o_logo = tk.PhotoImage(file="logo.png", width=80)
        tk.Label(self, bg=KOLOR_NAGŁÓWEK, fg=KOLOR_FONT_JASNY, image=self.__o_logo
                 ).pack(side=tk.LEFT, pady=10, padx=10)
        tk.Label(self, width=46, text="Automat biletowy MPK", bg=KOLOR_NAGŁÓWEK,
                 fg=KOLOR_FONT_JASNY, font=f"{FONT_N} bold underline").pack(side=tk.LEFT)
        self.__czas_naglowek = tk.Label(self, width=17, bg=KOLOR_NAGŁÓWEK, fg=KOLOR_FONT_JASNY,
                                        font=f"{FONT_ZAWARTOŚĆ} bold")
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

class RamkaBilety(tk.Frame):
    """Tworzy ramkę biletów dla GUI.

    Klasę trzeba zainicjalizować metodą inicjalizuj() podając zewnętrzne funkcje/metody, które
    będą wywoływane przy klikaniu przycisków funkcyjnych. Klasa tworzy dwie kolumny, segreguje
    bilety z automatu i umieszcza je w osobnych kolumnach. Do każdego biletu generuje przyciski
    funkcujne."""
    def __init__(self, okno_glowne: tk.Tk):
        super().__init__(okno_glowne)

    def inicjalizuj(self, dodaj_bilet, usun_bilet, automat):
        """Inicjalizuje elementy w ramce dodaje """
        lista_biletow = automat.bilety()
        i = 0
        j = 0
        for rodzaj in lista_biletow:
            for bilet in lista_biletow[rodzaj]:
                nazwa = "{} - {}\n\n{:.2f} zł".format(bilet.nazwa(), rodzaj, bilet.cena() / 100)
                tk.Label(self, bg=KOLOR_BILET, text=nazwa, width=29, height=4,
                         font=FONT_ZAWARTOŚĆ, fg=KOLOR_FONT_JASNY
                         ).grid(row=i, column=j, padx=(18, 3), pady=2)
                for znak in range(1, 3):
                    tmp = tk.Label(self, bg=KOLOR_BILET_F, width=8, height=4,
                                   font=FONT_ZAWARTOŚĆ, fg=KOLOR_FONT_JASNY)
                    if znak == 1:
                        tmp.configure(text="+")
                        tmp.bind("<Button-1>", dodaj_bilet)
                    else:
                        tmp.configure(text="-")
                        tmp.bind("<Button-1>", usun_bilet)
                    tmp.bilet = bilet
                    tmp.bind("<Enter>", lambda event: event.widget.configure(bg=KOLOR_BILET_F_HOVER))
                    tmp.bind("<Leave>", lambda event: event.widget.configure(bg=KOLOR_BILET_F))
                    tmp.grid(row=i, column=j + znak, padx=2, pady=2)
                i += 1
            j += 3
            i = 0

class Koszyk(tk.LabelFrame):
    """Tworzy ramkę koszyka dla GUI, która wyświetla listę biletów wybranych przez użytkownika."""
    def __init__(self, okno_glowne: tk.Tk):
        super().__init__(okno_glowne, text="TWÓJ KOSZYK", font=f"{FONT_N} bold")
        self.__okno = okno_glowne

    def aktualizuj_koszyk(self, automat, suma, limit=4):
        """Metoda aktualizuje listę biletów wyświetlaną przez obiekt klasy."""
        suma.configure(text="Do zapłaty: {:.2f} zł".format(automat.do_zaplaty()))
        self.destroy()
        koszyk = automat.koszyk()
        super().__init__(self.__okno, text="TWÓJ KOSZYK", font=f"{FONT_N} bold")
        tk.Label(self, text="Lp.", font=f"{FONT_ZAWARTOŚĆ} bold", width=5
                 ).grid(row=0, column=0, padx=2, pady=2)
        tk.Label(self, text="Nazwa", font=f"{FONT_ZAWARTOŚĆ} bold", width=32
                 ).grid(row=0, column=1, padx=2, pady=2)
        tk.Label(self, text="Rodzaj", font=f"{FONT_ZAWARTOŚĆ} bold", width=20
                 ).grid(row=0, column=2, padx=2, pady=2)
        tk.Label(self, text="Ilość", font=f"{FONT_ZAWARTOŚĆ} bold", width=13
                 ).grid(row=0, column=3, padx=2, pady=2)
        tk.Label(self, text="Cena", font=f"{FONT_ZAWARTOŚĆ} bold", width=13
                 ).grid(row=0, column=4, padx=2, pady=2)

        if limit >= len(koszyk.keys()):
            zasieg = 0
        else:
            zasieg = len(koszyk.keys()) - limit
        for i, bilet in zip(range(zasieg, len(koszyk.keys())), koszyk.keys()):
            tk.Label(self, text=str(i + 1), font=FONT_ZAWARTOŚĆ, width=5
                     ).grid(row=i + 1, column=0, padx=2, pady=2)
            tk.Label(self, text=bilet.nazwa(), font=FONT_ZAWARTOŚĆ, width=32
                     ).grid(row=i + 1, column=1, padx=2, pady=2)
            tk.Label(self, text=bilet.wariant(), font=FONT_ZAWARTOŚĆ, width=20
                     ).grid(row=i + 1, column=2, padx=2, pady=2)
            tk.Label(self, text=str(koszyk[bilet]), font=FONT_ZAWARTOŚĆ, width=13
                     ).grid(row=i + 1, column=3, padx=2, pady=2)
            tk.Label(self, text="{:.2f} zł".format(bilet.cena() / 100), font=FONT_ZAWARTOŚĆ,
                     width=13).grid(row=i + 1, column=4, padx=2, pady=2)
        self.pack(side=tk.TOP, fill=tk.X, padx=20)

class Stopka(tk.Frame):
    """Tworzy ramkę stopki dla domyślnego widoku GUI.

    Obiekt wyświetla przyciski funkcyjne oraz sumę do zapłaty."""
    def __init__(self, okno_glowne: tk.Tk):
        super().__init__(okno_glowne)

    def inicjalizuj(self, suma, widok_koszyk, anuluj, zapłać):
        """Tworzy główny widok stopki, przypisuje funkcję/metody do przycisków."""
        suma.grid(row=0, column=0, padx=18, pady=2)
        tmp = tk.Label(self, text="ZAPŁAĆ", bg=KOLOR_BUTTON1, width=20, height=2,
                       font=FONT_ZAWARTOŚĆ, fg=KOLOR_FONT_JASNY)
        tmp.bind("<Enter>", lambda event: event.widget.configure(bg=KOLOR_BUTTON1_HOVER))
        tmp.bind("<Leave>", lambda event: event.widget.configure(bg=KOLOR_BUTTON1))
        tmp.otwarty = True
        tmp.bind("<Button-1>", zapłać)
        tmp.grid(row=0, column=1, padx=18, pady=2)

        tmp = tk.Label(self, text="SPRAWDŹ KOSZYK", bg=KOLOR_BUTTON2, width=20, height=2,
                       font=FONT_ZAWARTOŚĆ, fg=KOLOR_FONT_JASNY)
        tmp.bind("<Enter>", lambda event: event.widget.configure(bg=KOLOR_BUTTON2_HOVER))
        tmp.bind("<Leave>", lambda event: event.widget.configure(bg=KOLOR_BUTTON2))
        tmp.otwarty = True
        tmp.bind("<Button-1>", widok_koszyk)
        tmp.grid(row=0, column=2, padx=18, pady=2)

        tmp = tk.Label(self, text="ANULUJ", bg=KOLOR_BUTTON3, width=20, height=2,
                       font=FONT_ZAWARTOŚĆ, fg=KOLOR_FONT_CIEMNY)
        tmp.bind("<Enter>", lambda event: event.widget.configure(bg=KOLOR_BUTTON3_HOVER,
                                                                 fg=KOLOR_FONT_JASNY))
        tmp.bind("<Leave>", lambda event: event.widget.configure(bg=KOLOR_BUTTON3,
                                                                 fg=KOLOR_FONT_CIEMNY))
        tmp.bind("<Button-1>", anuluj)
        tmp.grid(row=0, column=3, padx=18, pady=2)

class Alert(tk.Frame):
    """Wyświetla wiadomość z informacją lub ostrzeżeniem.

    Odpowiednik messagebox w klasie tkinter."""
    def __init__(self, okno_glowne):
        super().__init__(okno_glowne)
        self.__wiadomość = tk.Label(self, bg=KOLOR_ALERT, width=29, height=4,
                                    font=FONT_N, fg=KOLOR_FONT_JASNY)
        self.__wiadomość.pack()
        self.__przycisk = tk.Label(self, text="OK", bg=KOLOR_ALERT_F, width=29,
                                   height=2, font=FONT_N, fg=KOLOR_FONT_JASNY)
        self.__przycisk.bind("<Enter>", lambda event: event.widget.configure(bg=KOLOR_ALERT_HOVER))
        self.__przycisk.bind("<Leave>", lambda event: event.widget.configure(bg=KOLOR_ALERT_F))
        self.__przycisk.bind("<Button-1>", lambda event: self.place_forget())
        self.__przycisk.pack()

    def wyświetl(self, text, akcja=None):
        """Wyrzuca ramkę na ekran, opcjonalnie wywołuje funkcję."""
        self.__wiadomość.configure(text=text)
        self.place(x=550, y=450, anchor=tk.CENTER)
        if akcja is not None:
            akcja

class Widokzapłata(tk.Frame):
    """Tworzy ramkę widoku do zapłaty - tabelka z pieniędzmi, które można wrzucić do automatu."""
    def __init__(self, okno_glowne):
        super().__init__(okno_glowne)
        self.__suma = tk.Label(self, width=18, height=2, font=FONT_N_WIDOK2,
                               fg=KOLOR_FONT_CIEMNY, borderwidth=5, relief="solid")
        self.__suma.grid(row=0, column=0, padx=20, pady=20, columnspan=3)
        self.__ostrzeżenie = tk.Label(self, width=25, height=3,
                                      font=FONT_WIDOK2, fg=KOLOR_FONT_CIEMNY)
        self.__ostrzeżenie.grid(row=0, column=3, padx=20, pady=20, columnspan=3)
        self.__pieniadze = {0.01: None, 0.02: None, 0.05: None,
                            0.1: None, 0.2: None, 0.5: None,
                            1: None, 2: None, 5: None,
                            10: None, 20: None, 50: None}

    def aktualizacja(self, kwota, ostrzeżenie="Życzymy miłego dnia!"):
        """Aktualizuje kwotę do zapłaty oraz ostrzeżenie wyświetlane przez GUI."""
        self.__suma.configure(text="Do zapłaty: {:.2f} zł".format(kwota))
        self.__ostrzeżenie.configure(text=ostrzeżenie)

    def inicjalizuj(self, wrzuć, anuluj):
        """Inicjalizuje obiekty wewnątrz ramki."""
        i = 0
        j = 1
        for nazwa in self.__pieniadze:
            ścieżka = f"pieniądze/{nazwa}.png"
            obiekt = tk.PhotoImage(file=ścieżka, width=120, height=120)
            self.__pieniadze[nazwa] = obiekt
            tk.Label(self, image=obiekt).grid(row=j, column=i, padx=(18, 3), pady=2)
            tmp = tk.Label(self, text="+", bg=KOLOR_BUTTON2, width=4, height=2,
                           font="Arial 37", fg=KOLOR_FONT_JASNY)
            tmp.bind("<Enter>", lambda event: event.widget.configure(bg=KOLOR_BUTTON2_HOVER))
            tmp.bind("<Leave>", lambda event: event.widget.configure(bg=KOLOR_BUTTON2))
            tmp.wartość = float(nazwa)
            tmp.bind("<Button-1>", wrzuć)
            tmp.grid(row=j+1, column=i, padx=(18, 3), pady=2)
            i += 1
            if i == 6:
                j = 3
                i = 0
        tmp = tk.Label(self, width=25, height=3, font=FONT_WIDOK2,
                       fg=KOLOR_FONT_CIEMNY, bg=KOLOR_BUTTON3, text="Anuluj")
        tmp.bind("<Enter>", lambda event: event.widget.configure(bg=KOLOR_BUTTON3_HOVER,
                                                                 fg=KOLOR_FONT_JASNY))
        tmp.bind("<Leave>", lambda event: event.widget.configure(bg=KOLOR_BUTTON3,
                                                                 fg=KOLOR_FONT_CIEMNY))
        tmp.bind("<Button-1>", anuluj)
        tmp.grid(row=5, column=3, padx=20, pady=20, columnspan=3)

class Automat:
    """Główna klasa GUI automatu MPK - obsługuje obiekt automatu w formie graficznej."""
    def __init__(self, okno_glowne: tk.Tk, automat: system.System, id_automatu: str):
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
        self.__suma = tk.Label(self.__stopka, width=20, height=2,
                               font=FONT_ZAWARTOŚĆ, fg=KOLOR_FONT_CIEMNY)
        self.__alert = Alert(self.__okno)
        self.__widok_do_zapłaty = Widokzapłata(self.__okno)

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
        self.__widok_do_zapłaty.aktualizacja(self.__automat.do_zaplaty())
        self.__widok_do_zapłaty.pack_forget()
        self.__stopka.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        if reszta != []:
            zwrot = []
            for obiekt in reszta:
                tmp = f"{obiekt.wartość_gr()/100} {obiekt.waluta()}"
                zwrot.append(tmp)
            messagebox.showinfo("DO TWOJEJ KIESZENI", f"Automat MPK zwraca: {zwrot}")

    def widok_koszyk(self, event):
        """Obsługa przycisku zmieniająca widok domyślny na widok całego koszyka i z powrotem."""
        if len(self.__automat.koszyk().values()) != 0:
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
        if len(self.__automat.koszyk().values()) != 0:
            self.__ramka.pack_forget()
            self.__koszyk.pack_forget()
            self.__stopka.pack_forget()
            if self.__automat.admin_kasa()[0] == 0:
                self.__widok_do_zapłaty.aktualizacja(self.__automat.do_zaplaty(),
                                                     "Tylko odliczona kwota!")
            elif self.__automat.admin_kasa()[0] < 40.:
                self.__widok_do_zapłaty.aktualizacja(self.__automat.do_zaplaty(),
                                                     "Automat może nie wydać reszty.")
            else:
                self.__widok_do_zapłaty.aktualizacja(self.__automat.do_zaplaty())

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
                tmp = f"{obiekt.wartość_gr() / 100} {obiekt.waluta()}"
                zwrot.append(tmp)
        self.__ramka.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        self.__widok_do_zapłaty.aktualizacja(self.__automat.do_zaplaty())
        self.__widok_do_zapłaty.pack_forget()
        self.__stopka.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.__automat.koszyk()
        messagebox.showinfo("DO TWOJEJ KIESZENI", f"Automat MPK zwraca: {zwrot}")

    def wrzuć_pieniądz(self, event):
        """Obsługa przycisku wrzucania pieniądza do automatu."""
        try:
            zwrot = self.__automat.dodaj_pieniadz(pieniadze.Pieniadz(event.widget.wartość))
            self.__widok_do_zapłaty.aktualizacja(self.__automat.do_zaplaty())
            if zwrot is not None:
                if zwrot[0]:
                    self.finalizuj(zwrot[1])

        except system.ResztaException:
            self.__alert.wyświetl("Nie mogę wydać reszty!", self.anuluj())

    def start(self):
        """Metoda uruchamia GUI."""
        self.__okno.protocol("WM_DELETE_WINDOW", self.zamykanie)
        self.__nagłówek.pobierz_czas()
        self.__nagłówek.pack(side=tk.TOP, fill=tk.X)
        self.__ramka.inicjalizuj(self.dodaj_bilet, self.usun_bilet, self.__automat)
        self.__ramka.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        self.__stopka.inicjalizuj(self.__suma, self.widok_koszyk, self.anuluj, self.zapłać)
        self.__stopka.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.__widok_do_zapłaty.inicjalizuj(self.wrzuć_pieniądz, self.anuluj)
