# Temat projektu: Automat biletowy MPK
## Opis zadania:
Automat przechowuje informacje o monetach/banknotach znajdujących się w nim. (1, 2, 5, 10, 50gr, 1, 2, 5, 10, 20, 50zł). 
Po zamknięciu systemu automat zapisuje informacje o posiadanych monetach/banknotach do pliku. Automat stale wyświetla
domyślne menu z wyborem biletów, ich ceną, ilością aktualnie wybranych biletów oraz kwotą do zapłaty.
Automat zapewnia możliwość wybreania więcej niż jednego biletu oraz więcej niż jednego rodzaju biletu jednocześnie.
Po zatwierdzeniu swojego "koszyka" automat przechodzi do okna, gdzie wyświetla kwotę do zapłaty oraz interfejs
wrzucania monet z polem na wybór liczby wrzucanych monet/banknotów. Po wrzuceniu pieniędzy kwota do zapłaty na ekranie
odpowiednio zmniejsza się. Po osiągnięciu kwoty do zapłaty automat drukuje bilety oraz wraca do menu głównego.
W przypadku podania kwoty większej niż wymagana automat sprawdza czy może wydać resztę. W przypadku, kiedy
automat może wydać, wyświetla kwotę reszty, wydaje resztę oraz drukuje bilety i wraca do głównego menu. Kiedy automat
nie może wydać reszty, wyświetla taki komunikat i zwraca pieniądze. Automat wyświetla komunikat "Tylko odliczona
kwota", kiedy nie posiada żadnych pieniędzy. Automat wyświetla ostrzeżenie "Automat może nie wydać reszty", kiedy poziom
posiadanych pieniędzy jest zbyt niski.
