Mergency - Ambulance Sync

Mergency este o aplicatie desktop care permite gestionarea ambulantelor al mai multora
spitale in situatii de emergenta precum accidentele sau emergentele de orice fel.

Baza de date Oracle va retine urmatoarele entitati:
- Accident
- Hospital
- Ambulance
- Doctor
- Patient

Baza de date respectiva va permite prin interfata utilizator sa se asigneze personalul
si respectiv ambulanta cu caracteristicele cele mai potrivite pentru emergentele care
se verifica intr-un oras dintr-un judet specific.

O data ce se verifica un accident, controlul pe back-end va triggera un semnal pe
front-end care va ezplica situatia generala si utilizatorul va putea sa aleaga care
ambulanta sa trimita la locul accidentului pentru a furniza servicii de primul ajutor

Anumite tabele precum Doctor sau Ambulance contin si campuri care vor stabili daca
sunt disponibili pentru a primi pacientii accidentului sau daca sunt deja ocupati cu
un alt accident si trebuie sa fie pusi in asteptare.

Relatiile tabelelor sunt stabilite printr-un sistem de chei primare si externe catre
campurile *_id al tuturor entitatilor pentru o gestiune clara si eficienta.

Pe back-end vor fi implementate diferite sisteme de control de input al datelor si de
tratare al exceptiilor returnate de posibile date eronate sau de alte mesaje furnizate
de catre server-ul Oracle pentru a nu intrerupe buna functionalitate al aplicatiei

Back-end-ul este gestionat de libajul de programare Python 3.6 minim si de clientul
Oracle prin modulul cx_Oracle care permite legatura la baza de date host-ata pe serverul
universitatii la adresa 80.96.123.131. Se va folosi programarea orientata pe obiecte
si metode dedicate pentru a interoga sau a popula baza de date.

Front-end-ul este gestionat de catre libreria Kivy care permite dezvoltarea unei
interfete utilizator eleganta si functionala.

Sistemul operativ gazda folosit pentru development este Linux Mint 19.1 iar se va
implementa si un fisier Bash pentru a automatiza instalarea si ocnfigurarea tuturor
dependentelor necesare pentru aplicatie pe orice sistem Unix Like cu gestor de pachete
APT deci bazat pe Debian.
Build-urile ar trebui sa fie posibile si pentru Mac OS la fel cum si pentru Windows dar
vor necesita de instalarea si configurarea manuala a dependentelor si modulelor necesare
pentru Python si pentru clientul Oracle