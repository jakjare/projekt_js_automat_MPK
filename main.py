from logika import *
from tkinter import *
import time

def pobierz_czas(label):
    czas = time.localtime()
    label.config(text=time.strftime("%d/%m/%Y %H:%M:%S", czas))
    def aktualizuj():
        czas = time.localtime()
        label.config(text=time.strftime("%d/%m/%Y %H:%M:%S", czas))
        label.after(1000, aktualizuj)
    aktualizuj()

def dodaj_bilet(event):
    automat.dodaj_bilet_do_koszyka(event.widget.bilet)
    aktualizuj_koszyk()

def usun_bilet(event):
    try:
        automat.usun_bilet_z_koszyka(event.widget.bilet)
        aktualizuj_koszyk()
    except system.UsuwanieBiletuException:
        event.widget.configure(bg="red")

def aktualizuj_koszyk(limit = 4):
    global ramka_koszyk
    global suma
    suma.configure(text="Do zapłaty: {:.2f} zł".format(automat.do_zaplaty()))
    ramka_koszyk.destroy()
    koszyk = automat.koszyk()
    ramka_koszyk = LabelFrame(okno_glowne, text="TWÓJ KOSZYK", font="Arial 20 bold")
    ramka_koszyk.pack(side=TOP, fill=X, padx=20)
    Label(ramka_koszyk, text="Lp.", font="Arial 15 bold", width=5).grid(row=0, column=0, padx=2, pady=2)
    Label(ramka_koszyk, text="Nazwa", font="Arial 15 bold", width=44).grid(row=0, column=1, padx=2, pady=2)
    Label(ramka_koszyk, text="Rodzaj", font="Arial 15 bold", width=26).grid(row=0, column=2, padx=2, pady=2)
    Label(ramka_koszyk, text="Cena", font="Arial 15 bold", width=8).grid(row=0, column=3, padx=2, pady=2)

    if limit >= len(koszyk):
        zasieg = 0
    else:
        zasieg = len(koszyk)-4
    for i in range(zasieg, len(koszyk)):
        Label(ramka_koszyk, text=str(i+1), font="Arial 15", width=5).grid(row=i+1, column=0, padx=2, pady=2)
        Label(ramka_koszyk, text=str(koszyk[i].nazwa()), font="Arial 15", width=44).grid(row=i+1, column=1, padx=2, pady=2)
        Label(ramka_koszyk, text=str(koszyk[i].wariant()), font="Arial 15", width=26).grid(row=i+1, column=2, padx=2, pady=2)
        Label(ramka_koszyk, text=str("{:.2f} zł".format(koszyk[i].cena()/100)), font="Arial 15", width=8).grid(row=i+1, column=3, padx=2, pady=2)

def anuluj(event):
    automat.anuluj_transakcje()
    aktualizuj_koszyk()


automat = system.System()                                   #Tworzę obiekt automatu MPK
bilety = [bilety.Bilety("Jednorazowy", "normalny", 3),
          bilety.Bilety("60-minutowy", "normalny", 4),
          bilety.Bilety("24-godzinny", "normalny", 9),
          bilety.Bilety("3-dniowy", "normalny", 18),
          bilety.Bilety("7-dniowy", "normalny", 34),
          bilety.Bilety("Jednorazowy", "ulgowy", 1.5),
          bilety.Bilety("60-minutowy", "ulgowy", 2),
          bilety.Bilety("24-godzinny", "ulgowy", 4.5),
          bilety.Bilety("3-dniowy", "ulgowy", 9),
          bilety.Bilety("7-dniowy", "ulgowy", 17)]          #Tworzę obiekty biletów

for bilet in bilety:
    automat.dodaj_bilet(bilet)                              #Dodaję bilety do automatu
kasa_automatu = []                                          #Generuję pieniądze dla automatu
for i in range(30):
    kasa_automatu.append(pieniadze.Pieniadz(0.01))
    kasa_automatu.append(pieniadze.Pieniadz(0.02))
    kasa_automatu.append(pieniadze.Pieniadz(0.05))
    kasa_automatu.append(pieniadze.Pieniadz(0.1))
    kasa_automatu.append(pieniadze.Pieniadz(0.2))
    kasa_automatu.append(pieniadze.Pieniadz(0.5))
    kasa_automatu.append(pieniadze.Pieniadz(1))
    kasa_automatu.append(pieniadze.Pieniadz(2))
    kasa_automatu.append(pieniadze.Pieniadz(5))
automat.admin_kasa(kasa_automatu)                           #Dodaję pieniądze do kasy w automacie
del kasa_automatu

okno_glowne = Tk()                                          #Tworzę okno główne aplikacji
okno_glowne.title("Automat biletowy MPK")
okno_glowne.geometry("1100x900")
okno_glowne.resizable(False, False)

# Wyświetla nagłówek interfejsu
naglowek = Frame(okno_glowne, bg = "#00a2ff")
naglowek.pack(side = TOP, fill=X)
o_logo = PhotoImage(file="C:/Users/jakja/PycharmProjects/projekt_js_automat_MPK\logo.png", width = 80)
logo = Label(naglowek, bg="#00a2ff", fg="white", image = o_logo)
logo.pack(side = LEFT, pady = 10, padx = 10)
tytul = Label(naglowek, width = 46, text = "Automat biletowy MPK", bg="#00a2ff", fg="white", font="Arial 20 bold underline")
tytul.pack(side = LEFT)
czas_naglowek = Label(naglowek, width = 17, bg="#00a2ff", fg="white", font="Arial 15 bold")
czas_naglowek.pack(side = TOP, pady = 5)
pobierz_czas(czas_naglowek)

# Wyświetla listę wyboru biletów
ramka_bilety = Frame(okno_glowne)
ramka_bilety.pack(side = TOP, fill=X, pady=10)
lista_biletow = automat.bilety()
i = 0
j = 0
for rodzaj in lista_biletow:
    for bilet in lista_biletow[rodzaj]:
        nazwa = "{} - {}\n\n{:.2f} zł".format(bilet.nazwa(), rodzaj, bilet.cena()/100)
        b = Label(ramka_bilety, bg="#061981", text=nazwa, width=29, height=4,
                  font="Arial 15", fg="white").grid(row=i, column=j, padx=(18, 3), pady=2)
        for znak in range(1, 3):
            b = Label(ramka_bilety, bg="#646464", width=8, height=4, font="Arial 15", fg="white")
            if znak == 1:
                b.configure(text="+")
                b.bind("<Button-1>", dodaj_bilet)
            else:
                b.configure(text="-")
                b.bind("<Button-1>", usun_bilet)
            b.bilet = bilet
            b.bind("<Enter>", lambda event: event.widget.configure(bg="#9e9e9e"))
            b.bind("<Leave>", lambda event: event.widget.configure(bg="#646464"))
            b.grid(row=i, column=j+znak, padx=2, pady=2)
        i += 1
    j += 3
    i = 0
del i, j, lista_biletow

#Wyświetla koszyk, czyli listę aktualnie dodanych biletów
ramka_koszyk = LabelFrame(okno_glowne)


#Wyświetla sumę do zapłaty oraz przyciski funkcyjne
ramka_stopka = Frame(okno_glowne)
ramka_stopka.pack(side = BOTTOM, fill=X, pady=10)
suma = Label(ramka_stopka, width=20, height=2, font="Arial 15 bold", fg="black")
suma.grid(row=0, column=0, padx=18, pady=2)
b = Label(ramka_stopka, text="ZAPŁAĆ", bg="#139017", width=20, height=2, font="Arial 15", fg="black")
b.bind("<Enter>", lambda event: event.widget.configure(bg="#92d050"))
b.bind("<Leave>", lambda event: event.widget.configure(bg="#139017"))
b.grid(row=0, column=1, padx=18, pady=2)

b = Label(ramka_stopka, text="SPRAWDŹ KOSZYK", bg="#061981", width=20, height=2, font="Arial 15", fg="white")
b.bind("<Enter>", lambda event: event.widget.configure(bg="#465cfa"))
b.bind("<Leave>", lambda event: event.widget.configure(bg="#061981"))
b.grid(row=0, column=2, padx=18, pady=2)

b = Label(ramka_stopka, text="ANULUJ", bg="red", width=20, height=2, font="Arial 15", fg="black")
b.bind("<Enter>", lambda event: event.widget.configure(bg="#850000", fg="white"))
b.bind("<Leave>", lambda event: event.widget.configure(bg="red", fg="black"))
b.bind("<Button-1>", anuluj)
b.grid(row=0, column=3, padx=18, pady=2)



aktualizuj_koszyk()
okno_glowne.mainloop()