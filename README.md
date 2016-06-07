#HistoricalSocialNetworkAnalysis

###Zawartość archiwum:

`dumps` - dump bazy danych, na której przeprowadzono analizę

`export` - katalog eksportu grafów do pliku .csv

`plot` - katalog, do którego zapisywane są wygenerowane wykresy

`resources` - zawiera zastosowane zapytania SparQL do pobierania potrzebnych danych

`requirements` - plik konfiguracyjny PIP (wymagane zależnośći)

`start_database.bat/start_database.sh` - skrypt startujący bazę danych w katalogu .db

`src/analysis` - moduł analizy danych
  
`src/common` - pakiet zawierający wspólne zasoby
  
`src/data` - moduł danych
  
`src/visualisation` - modłu wizualizacji wyników

###Instalacja:

1. Zainstaluj http://perso.crans.org/aynaud/communities/
2. Wykonaj w głównym katalagu projektu:
```
pip install -r requirements.txt
```
3. Stwórz plik .db oraz wykonaj polecenie:
```
./start_database.[bat/sh]
```
