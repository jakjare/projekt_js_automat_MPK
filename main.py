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

def on_enter(event):
    event.widget.configure(bg="#9e9e9e")

def on_leave(event):
    event.widget.configure(bg="#646464")


automat = system.System()                                   #Tworzę obiek automatu MPK
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
okno_glowne.resizable(False, True)

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
        b = Label(ramka_bilety, bg="#646464", text="+", width=8, height=4, font="Arial 15", fg="white")
        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)

        b.grid(row=i, column=j+1, padx=2, pady=2)
        b = Label(ramka_bilety, bg="#646464", text="-", width=8, height=4, font="Arial 15", fg="white")
        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)
        b.grid(row=i, column=j+2, padx=2, pady=2)
        i += 1
    j += 3
    i = 0
del i, j, lista_biletow

#Wyświetla koszyk, czyli listę aktualnie dodanych biletów oraz sumę do zapłaty



okno_glowne.mainloop()
