# Corona Simulation
##Die Simulation

Wir simulieren eine Pandemie in zwei Gebieten. Die Grenze zwischen den Gebieten kann offen oder zu sein.

Es werden verschiedene Szenarien vorgeschlagen, wobei das Szenario jeweils nur in der linken Bevölkerung angewandt wird, damit man mit der rechten den Fall "Keine Maßnahmen" vergleichen kann.

Es wird in verschieden schwere Krankheitsverläufe unterschieden, wobei sowohl Dauer als auch Lethalität der Verläufe verschieden sind.

Es gibt ein Lockdown Szenario, verschieden starke Social Distancing Szenarien, und ein Testszenario, wobei positiv getestete Personen sich entsprechent nicht mehr bewegen (Quarantäne).




##Parametereinstellungen

In der Params.py Dateikönnen folgende Parameter eingestellt werden:  
* Die Größe der beiden Bevölkerungen
* Initialanzahlen an Infizierten und Erkrankten
* Die Warscheinlichkeit der Ansteckung bei Kontakt, und die Distanz, welche noch als Kontakt zählt
* Die Dauer der Krankheit bei normalem (nicht kritischem) Verlauf in Ticks. Wir haben uns für 150 entschieden
    * Schwere Verläufe dauern 50% länger
* Die Testkapazität und Häufigkeit der Tests, Standardwerte sind 10 Tests alle 2 Ticks.
    * Für eine Simulation ohne Tests kann der Wert einfach auf 0 gesetzt werden.
* Die Gebietsgrößen, wobei das eine Gebiet von (0,0) bis (xlowerlim,ylowerlim) geht, das andere von (xlowerlim, ylowerlim) bis (xLim, yLim)


## Klassen/Dateien

####Area/Location
In der Area.py sind wowohl die Klassen Area als auch Location enthalten.

Die Area macht nichts, außer ihre Grenzen zu speichern.

Die Location beinhaltet 2 Funktionen, welche mit entsprechend verschiedenen Daten (self und other, bzw self und Koordinaten) den Abstand berechnen.
Desweiteren gibt es zwei Funktionen, um Locations zu generieren, ein mal random fürs Bevölkerung generieren, dann noch mit einer Lockdownflag


####Person
Die Klasse Person wird dafür genutzt, die Daten der einzelnen Testpersonen zu speichern und zu manipulieren.
Zu den Daten gehören Dinge wie Gesundheitsstatus inklusive verschieden starken Erkrankungen, die Position, das Heimatgebiet uvm

Zu den Methoden gehören unter anderem diverse Gesundheitschecks und Updates, ein death roll und natürlich Methoden zum berechnen und umsetzen der Bewegung
Außerdem haben wir den Gesundheitsstatus als Enum umgesetzt.
####BasicSim
Hier wird der Großteil der Simulation durchgeführt (wer hätte es gedacht).

**Die erste Methode initialize** initialisiert ein Gebiet und in diesem Gebiet eine Bevölkerung.
Bei der Bevölkerung werden entsprechend den Parametern Leute infiziert.

**Die zweite Methode, updatePop** infiziert und testet zuerst Menschen, hierbei wird die Methode checkForInfect aufgerufen.
Es wird zuerst abgefragt, ob Person A ansteckend ist, bevor mit allen anderen Personen verglichen wird. Dies spart viel Zeit, wenn es wenige Infektionen gibt. 


Danach wird die update Methode aus der Person Klasse aufgerufen, welche sämtliche Gesundheitschecks und Bewegung durchführt.
Die Dataframes werden dann auch entsprechend geupdatet.

Zuletzt werden die Infizierten etc für beide Bevölkerungen separat gezählt. Diese Statistiken werden dann auch zurückgegeben

**Die Methode checkForInfect** ist der große Zeitfresser (da sie gegebenenfalls bis zu n^2 mal aufgerufen wird, wobei n = #Bevölkerung)
Sie überprüft, ob einge gegebene Mindestdistanz unterschritten wird, und würfelt dann entsprechend, ob man angesteckt wird.

**Die Methode simulation** ist die Methode, für die wir alle hier sind ;)

In ihr wird das Modul Pygame initialisiert. Es wird eine Fenstergröße an Hand der Gebietsgröße festgelegt. Außerdem wird die (maximale) Tickrate festgelegt.
Es werden danach die Arrays für unsere Statistiken initialisiert. Danach wird dann kontinuierlich die Bevölkerung geupdatet, die Statistiken gesammelt und für eine schönere Darstellung skaliert.
Schließlich wird der Plot des letzten ticks weiß übermalt und danach wird mit Hilfe der draw Funktion geplottet.

Zuguterletzt wird noch die pygame clock geupdatet (also die Ticks werden gezählt)

Falls escape oder das x oben rechts gedrückt werden, wird die Simulation abgebrochen und das Programm beendet.


**Die Draw Methode** zeichnet uns das ganze auf.

Hier wird zuerst die Legende initialisiert, dann wird die Bevölkerung farbcodiert an ihren entsprechenden Positionen aufgezeichnet.

Danach werden Gebietsgrenzen gezeichnet. Die Grenze zwischen den Gebieten ist dick oder dünn, jenachdem ob sie geschlossen ist.

die if else Abfrage sorgt dafür, dass Statistiken nur über der zugehören Bevölkerung geplottet werden, und nicht nach ein wenig Zeit überlappen.

Zuguterletzt wird noch unsere Legende geplottet.
####Buttons
Die Buttons Klasse erstellt eine GUI für die Szenarienauswahl.

Durch anklicken des Buttons "Lockdown" wird die lockdownFlag auf True gesetzt, also die Grenzen geschlossen. Derzeit ist es nicht möglich, sie wieder zu öffnen (außer durch Neustart).
Die Buttons starten das entsprechende Szenario (mit oder ohne Lockdown).

####SocialDistancing

Wenn das SocialDistancing Szenario aufgerufen wird, wird analog zur BasicSim initialisiert, dabei wird dann einem entsprechenden Prozentsatz vorgeschrieben, sich nicht zu bewegen.

####Coronatest

Dies ist eine Klasse zum durchführen von Tests, und entsprechender Reaktion auf positiven Test (Quarantäne).

Es kann eingestellt werden, wie viele Tests durchgeführt werden, und wie häufig das geschieht (jeder nte Tick).
