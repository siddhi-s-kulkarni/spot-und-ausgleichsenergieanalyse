# Spot- und Ausgleichsenergieanalyse

Dieses Projekt zeigt den Zusammenhang zwischen Day-Ahead-Spotpreisen und den Kosten für Ausgleichsenergie (reBAP).

Die Ausgleichsenergiekosten liegen üblicherweise sehr nah am Börsenspotpreis, da überdeckte Regelzonen durch unterdeckte ausgeglichen werden. An Tagen mit Systemstress (extreme Nachfrage, ungenaue Prognosen, Kraftwerksausfälle) kann der reBAP jedoch stark einbrechen oder in die Höhe schießen.

Eine Korrelationsanalyse zeigt die Zusammenhänge zwischen diesen beiden Preisreihen sowie Möglichkeiten, wie Flexibilität diese Preisschocks beim reBAP abfedern kann.

## Übersicht zu den Dateien

analysis.py: Enthält den selbst erstellten Python-Code für die Datenaufbereitung, Analyse und Visualisierung.
requirements.txt: Enthält die benötigten Python-Bibliotheken zur Ausführung des Codes.

### Datenquellen
REBAP_2025_12.xlsx: enthält die reBAP-Preise für Dezember 2025. Quelle: https://www.transnetbw.de/de/strommarkt/bilanzierung-und-abrechnung/bilanzierungsgebiete

Gro_handelspreise_202512010000_202601010000_Viertelstunde.xlsx: enthält die Day-Ahead-Spotpreise für Dezember 2025. Quelle: https://www.smard.de/home/downloadcenter/download-marktdaten/

## Hinweise

Die reBAP-Preise werden viertelstündlich abgerechnet. Die Day-Ahead-Spotmarktpreise wurden zum 1. Oktober 2025 von stündlicher auf viertelstündliche Abrechnung umgestellt. Aus Gründen der Einfachheit wurde daher für beide Datensätze (reBAP und Day-Ahead-Spotpreise) einheitlich der Zeitraum Dezember 2025 gewählt.

Es wird ein Batteriespeicher mit einer Kapazität von 0,1 MWh angenommen, der während Stress-Ereignissen als Steuerungsmaßnahme eingesetzt wird. Für die Zwecke dieses Projekts wird zudem angenommen, dass die Batterie bei Bedarf jederzeit über ausreichende Kapazität verfügt. Bei dem Batteriespeicher handelt es sich um eine vereinfachte Modellierung, um den wirtschaftlichen Effekt einer gezielten Steuerungsmaßnahme zu quantifizieren. Eine realistischere Modellierung würde unter anderem Ladezustand, Lade- und Entladeleistung, Wirkungsgrad und die zeitliche Verfügbarkeit der Batterie berücksichtigen.

## Wichtige Ergebnisse

### 1. Zusammenhang zwischen Spotpreis und reBAP

<img width="666" height="627" alt="plot1_korrelationsmatrix" src="https://github.com/user-attachments/assets/f4a79843-1d2e-444a-bef7-f0868c7e0767" />

Korrelationskennzahlen:

|              | Spotpreis | reBAP |
|--------------|-----------|-------|
| **Spotpreis** | 1,00      | 0,64  |
| **reBAP**     | 0,64      | 1,00  |

Korrelationskoeffizient zwischen Spotpreis und reBAP: 0,64 zeigt ein moderater bis starker positiver Zusammenhang. reBAP weist überwiegend eine ähnliche Entwicklung wie der Spotpreis auf, weicht jedoch an einzelnen Tagen deutlich ab.

### 2. Korrelation zwischen Spotpreisvolatilität und reBAP

Korrelation zwischen Spotpreisvolatilität und reBAP: 0,40

Die Ergebnisse zeigen eine moderat positive Korrelation (Pearson-r = 0,40) zwischen der Spotpreisvolatilität und dem reBAP. Dies weist darauf hin, dass volatile Marktphasen häufiger mit erhöhten Ausgleichsenergiepreisen verbunden sind. Die Spotpreisvolatilität erklärt den reBAP jedoch nur teilweise, sodass für eine belastbare Prognose weitere Einflussgrößen wie z. B. Prognosefehler bei Wind- und Solarenergie oder Lastabweichungen berücksichtigt werden müssen. Die Analyse zeigt einen positiven Zusammenhang, aber keine Kausalität.

In den 25 % volatilsten Marktphasen betrug der durchschnittliche Betrag des reBAP 118,23 €/MWh, während er in weniger volatilen Marktphasen bei 90,99 €/MWh lag.

### 3. Spotpreis vs. reBAP im Detail
<img width="1184" height="881" alt="plot2_scatterplot" src="https://github.com/user-attachments/assets/c825e0d0-39f7-48b4-824b-62d780c58e78" />

Solange der Spotpreis bei bis zu ~150 €/MWh liegt, bewegt sich der reBAP in einer klar erkennbaren Bandbreite. Steigt der Spotpreis darüber hinaus, kann der reBAP jedoch stark ausschlagen. Dies deutet darauf hin, dass ein hoher Spotpreis mit deutlich größeren reBAP-Schwankungen einhergeht. In den meisten Fällen bewegen sich Spotpreis und reBAP jedoch in einem vergleichbaren Preisbereich.

### 4. Zeitlicher Verlauf über Dezember 2025

<img width="2234" height="731" alt="plot3_timeseries" src="https://github.com/user-attachments/assets/652e52ae-c0c6-4093-808f-b9ad3f051a8b" />

Hier ist der Zusammenhang zwischen Spotpreis und reBAP über den Zeitverlauf erkennbar. Es zeigt sich, dass der reBAP in den meisten Fällen dem Preistrend des Spotpreises folgt, mit einigen Ausnahmen.

### 5. Häufigkeit von Stress-Ereignissen nach Tageszeit

<img width="1484" height="731" alt="plot4_haeufigkeitstressevents" src="https://github.com/user-attachments/assets/dd8912ce-b5d8-4c96-b5e5-488d590bfc73" />

Es ist erkennbar, dass die meisten Stress-Ereignisse im Morgenhochlauf zwischen 6 und 7 Uhr sowie im Abendhochlauf um 17 Uhr auftreten.

### 6. Quantifizierung der Steuerungsmaßnahmen durch Batteriespeichereinsatz
Zur Quantifizierung der wirtschaftlichen Auswirkungen der Batterie als Steuerungsmaßnahme werden zwei Szenarien betrachtet: Szenario A, in dem die Batterie ausschließlich während Stress-Ereignissen als Steuerungsmaßnahme eingesetzt wird, und Szenario B, in dem die Batterie bei jedem Ereignis eingesetzt wird.

Es zeigt sich Folgendes:

Szenario A:
Ersparnisse bei Steuerungsmaßnahme durch Batteriespeicher in Stress-Ereignisse: 1939,34 Euro
Ersparnisse pro MWh bei Steuerungsmaßnahmen durch Batteriespeicher in Stress-Ereignisse: 130,16 €/MWh

Szenario B:
Ersparnisse bei Steuerungsmaßnahmen wenn Batteriespeicher bei jedem Ereignis eingesetzt wird: 9505,45 Euro
Ersparnisse pro MWh bei Steuerungsmaßnahmen wenn Batteriespeicher bei jedem Ereignis eingesetzt wird: 31,94 €/MWh

Der gezielte Einsatz während der Stress-Ereignisse erfasst 20,4 % der theoretisch möglichen Gesamteinsparung bei nur 5,0 % der Einsatzzeit.

## Reproduzierbarkeit / Ausführung

Die Analyse kann mit wenigen Schritten lokal ausgeführt werden.

### Voraussetzungen

* Python 3.x
* Die im Repository enthaltenen Quelldateien
* Installierte Python-Bibliotheken aus der Datei `requirements.txt`

### Installation

Nach dem Klonen bzw. Herunterladen des Repositories können die benötigten Bibliotheken mit folgendem Befehl installiert werden:

```bash
pip install -r requirements.txt
```

### Ausführung

Anschließend kann die Analyse mit folgendem Befehl gestartet werden:

```bash
python analysis.py
```

Das Skript liest die im Repository enthaltenen Excel-Dateien mit den Spotpreis- und reBAP-Daten ein, führt die Datenaufbereitung und Analyse durch und erstellt die Ergebnisse.

Die erzeugten Grafiken werden automatisch im Ordner `results` gespeichert.


