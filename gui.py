from logika import system
from tkinter import Tk, Frame, LabelFrame, Label
import tkinter as tk
import time

class Nagłówek(Frame):
    def __init__(self, okno_glowne: Tk):
        super().__init__(okno_glowne, bg="#00a2ff")
        self.__o_logo = tk.PhotoImage(file="C:/Users/jakja/PycharmProjects/projekt_js_automat_MPK\logo.png", width=80)
        Label(self, bg="#00a2ff", fg="white", image=self.__o_logo).pack(side=tk.LEFT, pady=10, padx=10)
        Label(self, width=46, text="Automat biletowy MPK", bg="#00a2ff", fg="white", font="Arial 20 bold underline").pack(side=tk.LEFT)
        self.__czas_naglowek = Label(self, width=17, bg="#00a2ff", fg="white", font="Arial 15 bold")
        self.__czas_naglowek.pack(side=tk.TOP, pady=5)

    def pobierz_czas(self):
        czas = time.localtime()
        self.__czas_naglowek.config(text=time.strftime("%d/%m/%Y %H:%M:%S", czas))
        def aktualizuj():
            czas = time.localtime()
            self.__czas_naglowek.config(text=time.strftime("%d/%m/%Y %H:%M:%S", czas))
            self.__czas_naglowek.after(1000, aktualizuj)
        aktualizuj()

class RamkaBilety(Frame):
    def __init__(self, okno_glowne: Tk):
        super().__init__(okno_glowne)

    def inicjalicuj(self, dodaj_bilet, usun_bilet, automat):
        lista_biletow = automat.bilety()
        i = 0
        j = 0
        for rodzaj in lista_biletow:
            for bilet in lista_biletow[rodzaj]:
                nazwa = "{} - {}\n\n{:.2f} zł".format(bilet.nazwa(), rodzaj, bilet.cena() / 100)
                b = Label(self, bg="#061981", text=nazwa, width=29, height=4, font="Arial 15", fg="white").grid(row=i, column=j, padx=(18, 3), pady=2)
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
        del i, j, lista_biletow

class Koszyk(LabelFrame):
    def __init__(self, okno_glowne: Tk):
        super().__init__(okno_glowne, text="TWÓJ KOSZYK", font="Arial 20 bold")
        self.__okno = okno_glowne

    def aktualizuj_koszyk(self, automat, suma, limit=4):
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
            Label(self, text=str(i + 1), font="Arial 15", width=5).grid(row=i + 1, column=0, padx=2, pady=2)
            Label(self, text=str(koszyk[i].nazwa()), font="Arial 15", width=44).grid(row=i + 1, column=1, padx=2, pady=2)
            Label(self, text=str(koszyk[i].wariant()), font="Arial 15", width=26).grid(row=i + 1, column=2, padx=2, pady=2)
            Label(self, text=str("{:.2f} zł".format(koszyk[i].cena() / 100)), font="Arial 15", width=8).grid(row=i + 1, column=3, padx=2, pady=2)
        self.pack(side=tk.TOP, fill=tk.X, padx=20)

class Stopka(Frame):
    def __init__(self, okno_glowne: Tk):
        super().__init__(okno_glowne)

    def inicjalizuj(self, suma, widok_koszyk, anuluj):
        suma.grid(row=0, column=0, padx=18, pady=2)
        b = Label(self, text="ZAPŁAĆ", bg="#139017", width=20, height=2, font="Arial 15", fg="black")
        b.bind("<Enter>", lambda event: event.widget.configure(bg="#92d050"))
        b.bind("<Leave>", lambda event: event.widget.configure(bg="#139017"))
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

class Automat():
    def __init__(self, okno_glowne: Tk, automat: system.System):
        self.__automat = automat
        okno_glowne.title("Automat biletowy MPK")
        okno_glowne.geometry("1100x900")
        okno_glowne.resizable(False, False)
        self.__nagłówek = Nagłówek(okno_glowne)
        self.__ramka = RamkaBilety(okno_glowne)
        self.__koszyk = Koszyk(okno_glowne)
        self.__stopka = Stopka(okno_glowne)
        self.__suma = Label(self.__stopka, width=20, height=2, font="Arial 15 bold", fg="black")

    def dodaj_bilet(self, event):
        self.__automat.dodaj_bilet_do_koszyka(event.widget.bilet)
        self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)

    def usun_bilet(self, event):
        try:
            self.__automat.usun_bilet_z_koszyka(event.widget.bilet)
            self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        except system.UsuwanieBiletuException:
            event.widget.configure(bg="red")

    def anuluj(self, event):
        self.__automat.anuluj_transakcje()
        self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)

    def widok_koszyk(self, event):
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

    def start(self):
        self.__nagłówek.pobierz_czas()
        self.__nagłówek.pack(side=tk.TOP, fill=tk.X)
        self.__ramka.inicjalicuj(self.dodaj_bilet, self.usun_bilet, self.__automat)
        self.__ramka.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.__koszyk.aktualizuj_koszyk(self.__automat, self.__suma)
        self.__stopka.inicjalizuj(self.__suma, self.widok_koszyk, self.anuluj)
        self.__stopka.pack(side=tk.BOTTOM, fill=tk.X, pady=10)