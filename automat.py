import tkinter as tk
import gui

from logika import bilety
from logika import pieniadze
from logika import system
from logika import stale

def main():
    """Funkcja główna."""
    automat = system.System()                                               # Tworzę obiekt automatu MPK
    bilety_w_automacie = [bilety.Bilety(nazwa="Jednorazowy", wariant="normalny", cena=3),
                          bilety.Bilety(nazwa="60-minutowy", wariant="normalny", cena=4),
                          bilety.Bilety(nazwa="24-godzinny", wariant="normalny", cena=9),
                          bilety.Bilety(nazwa="3-dniowy", wariant="normalny", cena=18),
                          bilety.Bilety(nazwa="7-dniowy", wariant="normalny", cena=34),
                          bilety.Bilety(nazwa="Jednorazowy", wariant="ulgowy", cena=1.5),
                          bilety.Bilety(nazwa="60-minutowy", wariant="ulgowy", cena=2),
                          bilety.Bilety(nazwa="24-godzinny", wariant="ulgowy", cena=4.5),
                          bilety.Bilety(nazwa="3-dniowy", wariant="ulgowy", cena=9),
                          bilety.Bilety(nazwa="7-dniowy", wariant="ulgowy", cena=17)] # Tworzę obiekty biletów

    for bilet in bilety_w_automacie:
        automat.dodaj_bilet(bilet)                                          # Dodaję bilety do automatu
    kasa_automatu = []                                                      # Generuję pieniądze dla automatu
    for nominał in stale.NOMINAŁY_GR:
        kasa_automatu.append(pieniadze.Pieniadz(wartość_zł=nominał/100))    # Po jednym każdego nominału
    automat.admin_kasa(kasa_automatu)                                       # Dodaję pieniądze do kasy w automaciekasa_automatu

    root = tk.Tk()                                                          # Tworzę okno główne aplikacji
    aplikacja = gui.Automat(root, automat, "automat-1")                     # Tworzę obiekt automatu w GUI
    aplikacja.start()                                                       # Uruchamiam aplikację
    root.mainloop()                                                         # Główna pętla programu

if __name__ == '__main__':
    main()
