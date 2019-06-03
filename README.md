# Mergency - Hospital Sync

<p align="center">
  <img width="460" height="300" src="https://raw.githubusercontent.com/serban-mihai/Mergency/mihai-dev/assets/logo_final.png">
</p>

Mergency este o aplicatie desktop care permite gestionarea ambulantelor al mai multora
spitale in situatii de emergenta precum accidentele sau emergentele de orice fel.

## Baza de date va retine urmatoarele entitati:
- Accident
- Hospital
- Ambulance
- Doctor
- Patient

Baza de date respectiva va permite prin interfata utilizator sa se asigneze personalul
si respectiv ambulanta cu caracteristicele cele mai potrivite pentru emergentele care
se verifica intr-un oras dintr-un judet specific.

<p align="center">
  <img width="460" height="130" src="https://raw.githubusercontent.com/serban-mihai/Mergency/mihai-dev/assets/oracle.png">
</p>

Anumite tabele precum Doctor sau Ambulance contin si campuri care vor stabili daca
sunt disponibili pentru a primii pacientii accidentului sau daca sunt deja ocupati cu
un alt accident si trebuie sa fie pusi in asteptare.

Relatiile tabelelor sunt stabilite printr-un sistem de chei primare si externe catre
campurile *_id al tuturor entitatilor pentru o gestiune clara si eficienta.

Pe back-end vor fi implementate diferite sisteme de control de input al datelor si de
tratare al exceptiilor returnate de posibile date eronate sau de alte mesaje furnizate
de catre server-ul Oracle pentru a nu intrerupe buna functionalitate al aplicatiei

Back-end-ul este gestionat de libajul de programare Python 3 (min. v3.6)  si de clientul
Oracle prin modulul cx_Oracle care permite legatura la baza de date host-ata pe serverul
universitatii la adresa 80.96.123.131. Se va folosi programarea orientata pe obiecte
si metode dedicate pentru a interoga sau a popula baza de date.

Front-end-ul este gestionat de catre libreria Kivy care permite dezvoltarea unei
interfete utilizator eleganta si functionala.

Sistemul operativ gazda folosit pentru development este Linux Mint 19.1 iar se va
implementa si un fisier Bash pentru a automatiza instalarea si configurarea tuturor
dependentelor necesare pentru aplicatie pe orice sistem Unix Like cu gestor de pachete
APT deci bazat pe Debian.
Build-urile ar trebui sa fie posibile si pentru Mac OS la fel cum si pentru Windows dar
vor necesita de instalarea si configurarea manuala a dependentelor si modulelor necesare
pentru Python si pentru clientul Oracle

## Schema Bazei de Date

<p align="center">
  <img width="460" height="800" src="https://raw.githubusercontent.com/serban-mihai/Mergency/master/SCHEMA.png">
</p>

## Functionalitate
Aplicatia se prezinta in prima instanta ca o aplicatie mobila care seamana cu orice alta
aplicatie mobile dar este gandita pentru folosirea sa in ambient Desktop.

**(Insert here splash screen)**

Prin intermediul butonului de navigare situat in coltul stangh superior al chenarului
este posibila chemarea aparitiei unui navigator bar care prezinta urmatoarele optiuni:

Menu | Descriere | Note
--- | --- | ---
`Manager` | Permite gestionarea tuturor entitatilor prezente in baza de date precum Ambulante, Pacient, Accident... | Necesita de o conexiune valida la baza de date
`Database` | Permite conectarea la o baza de date Oracle locala sau host-ata pe un server specific | DEBUG in Terminal
`About` | Contine informatii despre aplicatie si despre autor | -
`Dummy PUSH` | Permite creerea tabelelor si popularea lor cu date de test care vor putea fi folosite in viitor | Necesita de o conexiune valida la baza de date
`Dummy POP` | Permite eliminarea tuturor tabelelor create prin PUSH pentru a face curatenie in structura bazei de date | Necesita de o conexiune valida la baza de date

**(Insert here navigator screen)**

## Database
Tab-ul Database contine diferite campuri unde pot sa fie inserate datele necesare pentru 
conexiunea la baza de date dorita. De default datele serverului de test sunt inserate automat
la startup dar pot fi modificate oricand pentru a folosit alt host sau alta baza de date Oracle.
Toate campurile au un nume si o descriere (helper) care apare atunci cand se selecteaza campul.

**(Insert here database screen)**

O data ce datele sunt inserate se poate incerca conexiunea prin apasarea butonului de **CONNECT**. 
Daca coneziunea a avut succes un mesaj de debug in consola din care este rulata aplicatia va 
confirma acest lucru sau in caz contrar va returna o eroare Oracle daca conexiunea nu a avut loc corect.
Deasemenea dupa ce conexiunea la baza de date este stabilita se poate intrerupe oricand apasand butonul 
**DISCONNECT**

## Dummy PUSH
Pentru a permite un test al aplicatiei a fost introdusa aceasta optiune care permite sa creeze si sa populeze
in automat cu o serie de date cazuale toate tabelele luate in calcul pentru aplicatie. A fost folosit o
variabila *PFIX* in cod care se leaga la fiecare Query si contine numele autorului_ pentru a nu interfera
cu eventuale alte tabele deja prezente pe server-ul de test in timpul development-ului.

O data selectionat acest Tab se va putea observa in consola din care s-a lansat aplicatia diferite mesaje de debug
in legatura cu orice Query este trimis catre server si raspunsul sau la fiecare deasemenea.

**(Insert here debug PUSH log)**

Din lipsa de timp nu s-au putut implementa functii asyncrone pentru trimiterea instructiunilor catre host si
asta se rezolva intr-un freeze momentan al aplicatiei in timp ce functiile isi executa continutul pana cand
fiecare se sfarseste. Aceasta problema este mai accentuata daca se ruleaza aplicatia de pe sisteme tehnologic
mai batrane sau daca viteza de conexiune la retea este slaba sau host-ul raspunde greu la squest-uri.

## Dummy POP
Contrar ca si pentru PUSH, acest Tab permite elminarii instantanee a tuturor tabelelor create prin PUSH si-i se
aplica toate precizarile facute pentru Tab-ul precedent, inclusiv lipsa de functii asyncrone si mesajele de 
debug in consola din care s-a rulat aplicatia.

**(Insert here debug POP log)**

La fel cum si pentru PUSH, nici Tab-ul POP va avea vreo-un efect daca mai intai nu s-a stabilit o conexiune 
valida la o baza de date Oracle.

## Manager
Tab-ul Manager permite getionarea tuturor entitatilor (sau tabelelor) din baza de date relative programului.
Tot de aici este posibila adaugarea sau stergerea manuala al entitatilor din oricare tabel.

In caz ca se intra in acest Tab fara o conexiune la baza de date activa el va fi pur si simplu gol
pana cand o conexiune nu este prezenta si pana cand nu se populeaza respectiv tabelurile cu niste date.

**(Insert here manager empty screen)**

# About


# Resurse si Referinte

Nume | Ver. | Descriere | Link
--- | --- | --- | ---
`Python` | 3.6 | Limbajul de programare | https://www.python.org/downloads/
`Visual Studio Code` | 1.34.0 | Editorul de Text | https://code.visualstudio.com/
`Kivy` | 1.11.0 | Librerie Grafica (Baza) | https://kivy.org/#home
`KivyMD` | 0.1.3 | Librerie Grafica (Custom) | https://github.com/HeaTTheatR/KivyMD
`Pip3` | 19.1.1 | Gestorul de Pachete | https://pypi.org/project/pip/
`cx_Oracle` | 7.1 | Modul Oracle | https://oracle.github.io/python-cx_Oracle/
`Instant Client Oracle` | 11.2 | **ATENTIE** Este foarte importanta versiunea respectiva pentru server-ul folosit! | https://www.oracle.com/database/technologies/instant-client.html
`Linux Mint` | 19.1 | Sistemul Operativ (Tessa) - XFCE | https://linuxmint.com/


