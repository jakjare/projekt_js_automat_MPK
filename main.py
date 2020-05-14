from logika import *
from tkinter import *
import time

def pobierz_czas(label):
    czas = time.localtime()
    label.config(text=time.strftime("%d/%m/%Y, %H:%M:%S", czas))
    def aktualizuj():
        czas = time.localtime()
        label.config(text=time.strftime("%d/%m/%Y, %H:%M:%S", czas))
        label.after(1000, aktualizuj)
    aktualizuj()

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

okno_glowne = Tk()
okno_glowne.title("Automat biletowy MPK")
okno_glowne.geometry("1100x800")
okno_glowne.resizable(False, False)

# Wyświetla nagłówek interfejsu
naglowek = Frame(okno_glowne, bg = "#00a2ff")
naglowek.pack(side = TOP)
o_logo = PhotoImage(file="C:/Users/jakja/PycharmProjects/projekt_js_automat_MPK\logo.png", width = 80)
logo = Label(naglowek, bg="#00a2ff", fg="white", image = o_logo)
logo.pack(side = LEFT, pady = 10, padx = 10)
tytul = Label(naglowek, width = 46, text = "Automat biletowy MPK", bg="#00a2ff", fg="white", font="Arial 20 bold underline")
tytul.pack(side = LEFT)
czas_naglowek = Label(naglowek, width = 17, bg="#00a2ff", fg="white", font="Arial 15 bold")
czas_naglowek.pack(side = TOP, pady = 5)
pobierz_czas(czas_naglowek)

# Wyświetla bilety




okno_glowne.mainloop()
