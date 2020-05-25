# Temat projektu: Automat biletowy MPK
## Opis zadania:
Automat przechowuje informacje o monetach/banknotach znajdujących się w nim. (1, 2, 5, 10, 50gr, 1, 2, 5, 10, 20, 50zł). 
Po zamknięciu systemu automat zapisuje informacje o posiadanych monetach/banknotach do pliku. Automat stale wyświetla
domyślne menu z wyborem biletów, ich ceną, ilością aktualnie wybranych biletów oraz kwotą do zapłaty.
Automat zapewnia możliwość wybrania więcej niż jednego biletu oraz więcej niż jednego rodzaju biletu jednocześnie.
Po zatwierdzeniu swojego "koszyka" automat przechodzi do okna, gdzie wyświetla kwotę do zapłaty oraz interfejs
wrzucania monet z polem na wybór liczby wrzucanych monet/banknotów. Po wrzuceniu pieniędzy kwota do zapłaty na ekranie
odpowiednio zmniejsza się. Po osiągnięciu kwoty do zapłaty automat drukuje bilety oraz wraca do menu głównego.
W przypadku podania kwoty większej niż wymagana automat sprawdza czy może wydać resztę. W przypadku, kiedy
automat może wydać, wyświetla komunikat, wydaje resztę oraz drukuje bilety i wraca do głównego menu. Kiedy automat
nie może wydać reszty, wyświetla taki komunikat i zwraca pieniądze. Automat wyświetla komunikat "Tylko odliczona
kwota", kiedy nie posiada żadnych pieniędzy. Automat wyświetla ostrzeżenie "Automat może nie wydać reszty", kiedy poziom
posiadanych pieniędzy jest zbyt niski.
## Testy:
1. Bilet kupiony za odliczoną kwotę, automat nie powinien wydać reszty ani wyświetlić takego komunikatu.
2. Bilet kupiony płacąc więcej, automat powinien wyświetlić monit o tym, że wydaje resztę.
3. Bilet kupiony płacąc więcej, automat nie ma jak wydać reszty, automat informuje użytkownika o błędzie, nie drukuje biletów, zwraca wrzucone pieniądze.
4. Zakup biletu płacąc po 1gr - suma stu monet 1gr ma być równa 1zł.
5. Zakup dwóch różnych biletów naraz, automat sumuje ceny biletów i drukuje oba.
6. Próba wrzucenia ujemnej oraz niecałkowitej liczby monet, automat wurzuca komunikat o błędzie.
## Link do repozytorium:
https://github.com/jakjare/projekt_js_automat_MPK