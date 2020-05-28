from logika import bilety, pieniadze, system
from tkinter import Tk
import gui

def main():
    automat = system.System()                                               # Tworzę obiekt automatu MPK
    bilety_w_automacie = [  bilety.Bilety("Jednorazowy", "normalny", 3),
                            bilety.Bilety("60-minutowy", "normalny", 4),
                            bilety.Bilety("24-godzinny", "normalny", 9),
                            bilety.Bilety("3-dniowy", "normalny", 18),
                            bilety.Bilety("7-dniowy", "normalny", 34),
                            bilety.Bilety("Jednorazowy", "ulgowy", 1.5),
                            bilety.Bilety("60-minutowy", "ulgowy", 2),
                            bilety.Bilety("24-godzinny", "ulgowy", 4.5),
                            bilety.Bilety("3-dniowy", "ulgowy", 9),
                            bilety.Bilety("7-dniowy", "ulgowy", 17)]        # Tworzę obiekty biletów

    for bilet in bilety_w_automacie:
        automat.dodaj_bilet(bilet)                                          # Dodaję bilety do automatu
    kasa_automatu = []                                                      # Generuję pieniądze dla automatu
    for i in range(1):
        kasa_automatu.append(pieniadze.Pieniadz(0.01))
        kasa_automatu.append(pieniadze.Pieniadz(0.02))
        kasa_automatu.append(pieniadze.Pieniadz(0.05))
        kasa_automatu.append(pieniadze.Pieniadz(0.1))
        kasa_automatu.append(pieniadze.Pieniadz(0.2))
        kasa_automatu.append(pieniadze.Pieniadz(0.5))
        kasa_automatu.append(pieniadze.Pieniadz(1))
        kasa_automatu.append(pieniadze.Pieniadz(2))
        kasa_automatu.append(pieniadze.Pieniadz(5))
    automat.admin_kasa(kasa_automatu)                                       # Dodaję pieniądze do kasy w automacie
    del kasa_automatu

    root = Tk()                                                             # Tworzę okno główne aplikacji
    gui.Automat(root, automat, "automat-1").start()                         # Uruchamiam obiekt automatu w GUI
    root.mainloop()                                                         # Główna pętla programu

if __name__ == '__main__':
    main()