# Spot- und Ausgleichsenergieanalyse

Dieses Projekt zeigt den Zusammenhang zwischen Day-Ahead-Spotpreisen und den Kosten für Ausgleichsenergie (reBAP).

Die Ausgleichsenergiekosten liegen üblicherweise sehr nah am Börsenspotpreis, da überdeckte Regelzonen durch unterdeckte ausgeglichen werden. An Tagen mit Systemstress (extreme Nachfrage, ungenaue Prognosen, Kraftwerksausfälle) kann der reBAP jedoch stark einbrechen oder in die Höhe schießen.

Eine Korrelationsanalyse zeigt die Abhängigkeiten zwischen diesen beiden Preisreihen sowie Möglichkeiten, wie Flexibilität diese Preisschocks beim reBAP abfedern kann.

## Quelldaten

Die reBAP-Preise stammen von: 
https://www.transnetbw.de/de/strommarkt/bilanzierung-und-abrechnung/bilanzierungsgebiete

Die Day-Ahead-Spotpreise stammen von: 
https://www.smard.de/home/downloadcenter/download-marktdaten/

## Hinweise

Die reBAP-Preise werden viertelstündlich abgerechnet. Die Day-Ahead-Spotmarktpreise wurden zum 1. Oktober 2025 von stündlicher auf viertelstündliche Abrechnung umgestellt. Aus Gründen der Einfachheit wurde daher für beide Datensätze (reBAP und Day-Ahead-Spotpreise) einheitlich der Zeitraum Dezember 2025 gewählt.

Es wird ein Batteriespeicher mit einer Kapazität von 0,1 MWh angenommen, der während Stress-Ereignissen als Steuerungsmaßnahme eingesetzt wird. Für die Zwecke dieses Projekts wird zudem angenommen, dass die Batterie bei Bedarf jederzeit über ausreichende Kapazität verfügt.


## Wichtige Ergebnisse

### 1. Zusammenhang zwischen Spotpreis und reBAP

<img width="666" height="627" alt="plot1_korrelationsmatrix" src="https://github.com/user-attachments/assets/f4a79843-1d2e-444a-bef7-f0868c7e0767" />

Korrelationskennzahlen:

|              | Spotpreis | reBAP |
|--------------|-----------|-------|
| **Spotpreis** | 1,00      | 0,64  |
| **reBAP**     | 0,64      | 1,00  |

Korrelationskoeffizient zwischen Spotpreis und reBAP: 0,64 zeigt ein moderater bis starker positiver Zusammenhang. reBAP folgt überwiegend dem Spotpreis, weicht jedoch an einzelnen Tagen deutlich ab.

### 2. Korrelation zwischen Spotpreis Volatilität und reBAP

Korrelation zwischen Spotpreis Volatilität and reBAP: 0,4

Die Ergebnisse zeigen eine moderat positive Korrelation (Pearson-r = 0,4) zwischen der Spotpreisvolatilität und dem reBAP. Dies weist darauf hin, dass volatile Marktphasen häufiger mit erhöhten Ausgleichsenergiepreisen verbunden sind. Die Spotpreisvolatilität erklärt den reBAP jedoch nur teilweise, sodass für eine belastbare Prognose weitere Einflussgrößen wie z.B. Prognosefehler bei Wind- und Solarenergie oder Lastabweichungen berücksichtigt werden müssen.

In den 25 % volatilsten Marktphasen betrug der durchschnittliche Betrag des reBAP 118,23 €/MWh, während er in weniger volatilen Marktphasen bei 91 €/MWh lag.

### 3. Spotpreis vs. reBAP im Detail
<img width="1184" height="881" alt="plot2_scatterplot" src="https://github.com/user-attachments/assets/c825e0d0-39f7-48b4-824b-62d780c58e78" />

Solange der Spotpreis bei bis zu ~150 €/MWh liegt, bewegt sich der reBAP in einer klar erkennbaren Bandbreite. Steigt der Spotpreis darüber hinaus, kann der reBAP jedoch stark ausschlagen. Dies deutet darauf hin, dass ein hoher Spotpreis mit deutlich größeren reBAP-Schwankungen einhergeht. In den meisten Fällen bewegen sich Spotpreis und reBAP jedoch in einem vergleichbaren Preisbereich.

### 4. Zeitlicher Verlauf über Dezember 2025

<img width="2234" height="731" alt="plot3_timeseries" src="https://github.com/user-attachments/assets/652e52ae-c0c6-4093-808f-b9ad3f051a8b" />

Hier ist der Zusammenhang zwischen Spotpreis und reBAP über den Zeitverlauf erkennbar. Es zeigt sich, dass der reBAP in den meisten Fällen dem Preistrend des Spotpreises folgt, mit einigen Ausnahmen.

### 5. Häufigkeit von Stress-Ereignissen nach Tageszeit

<img width="1484" height="731" alt="plot4_haeufigkeitstressevents" src="https://github.com/user-attachments/assets/dd8912ce-b5d8-4c96-b5e5-488d590bfc73" />

Es ist erkennbar, dass die meisten Stress-Ereignisse im Morgenhochlauf zwischen 6–7 Uhr sowie im Abendhochlauf um 17 Uhr auftreten.

### 6. Quantifizierung der Steuerungsmaßnahmen durch Batteriespeicher Einsatz
Zur Quantifizierung der wirtschaftlichen Auswirkung der Batterie als Steuerungsmaßnahme werden zwei Szenarien betrachtet: Szenario A, in dem die Batterie ausschließlich während Stress-Ereignissen als Steuerungsmaßnahme eingesetzt wird, und Szenario B, in dem die Batterie bei jedem Ereignis eingesetzt wird.

Es zeigt sich Folgendes:

Scenario A:
Ersparnisse bei Steuerungsmaßnahme durch Batteriespeicher in Stress events: 1939,340 Euro
Ersparnisse pro MWh bei Steuerungsmaßnahmen durch Batteriespeicher in Stress events: 130,157 €/MWh

Scenario B:
Ersparnisse bei Steuerungsmaßnahmen wenn Batteriespeicher bei jedem Ereignis eingesetzt wird: 9505,453 Euro
Ersparnisse pro MWh bei Steuerungsmaßnahmen wenn Batteriespeicher bei jedem Ereignis eingesetzt wird: 31,940 €/MWh


Der gezielte Einsatz während der Stress-Ereignisse erfasst 20,4 % der theoretisch möglichen Gesamteinsparung bei nur 5,0 % der Einsatzzeit.

