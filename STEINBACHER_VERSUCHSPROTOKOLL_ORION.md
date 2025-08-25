# ORION Versuchsprotokoll für Steinbacher EPS-Optimierung
## Ziel: 150 kPa Querzugsfestigkeit bei 14,5 kg/m³ Rohdichte

---

# VERSUCHSREIHE: DATENERFASSUNG

---

## BLOCK 1 - BASELINE

### A. ROHSTOFF-DATEN

| Feld | Wert | Einheit |
|------|------|---------|
| **Datum/Uhrzeit Produktion** | _________________ | |
| **Block-Nummer** | _________________ | |
| **Lieferant** | [ ] BASF [ ] Sunpor | |
| **Materialtyp/Rezept** | _________________ | |
| **Chargen-Nr. Granulat** | _________________ | |
| **Lieferdatum Granulat** | _________________ | |
| **Material-Alter bei Verarbeitung** | _________________ | Stunden |
| **Lagertemperatur Granulat** | _________________ | °C |

### B. VORSCHÄUMUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **Dampftemperatur Vorschäumer** | _________________ | °C |
| **Dampfdruck Vorschäumer** | _________________ | bar |
| **Vorschäum-Zeit** | _________________ | Sekunden |
| **Schüttdichte nach Vorschäumung** | _________________ | kg/m³ |
| **Perlengröße (Siebanalyse)** | _________________ | mm |

### C. REIFUNG (KRITISCH!)

| Feld | Wert | Einheit |
|------|------|---------|
| **Beginn Reifung (Datum/Uhrzeit)** | _________________ | |
| **Ende Reifung (Datum/Uhrzeit)** | _________________ | |
| **GESAMTE REIFUNGSZEIT** | _________________ | Stunden |
| **Silo-Nummer** | _________________ | |
| **Silo-Temperatur** | _________________ | °C |
| **Luftfeuchtigkeit Silo** | _________________ | % |

### D. BLOCKFORMUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **Dampfdruck (Hauptbedampfung)** | _________________ | bar |
| **Dampftemperatur** | _________________ | °C |
| **Vorbedampfungszeit** | _________________ | Sekunden |
| **Hauptbedampfungszeit** | _________________ | Sekunden |
| **Nachhaltezeit** | _________________ | Sekunden |
| **Vakuum Spalte 14** | _________________ | mbar |
| **Vakuum Spalte 42** | _________________ | mbar |
| **Spalte 99 (Dampfzeit-Parameter)** | _________________ | |
| **Kühlzeit** | _________________ | Sekunden |
| **Kühlvakuum** | _________________ | mbar |
| **Gesamte Zykluszeit** | _________________ | Sekunden |

### E. BLOCK-DATEN

| Feld | Wert | Einheit |
|------|------|---------|
| **Block-Abmessungen L x B x H** | _______ x _______ x _______ | mm |
| **Block-Gewicht** | _________________ | kg |
| **Berechnete Rohdichte Block** | _________________ | kg/m³ |

### F. QUALITÄTSPRÜFUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **Prüfdatum** | _________________ | |
| **Probenentnahme-Position** | _________________ | |
| **Rohdichte Probe** | _________________ | kg/m³ |
| **Querzugsfestigkeit** | _________________ | kPa |
| **Biegefestigkeit** | _________________ | kPa |
| **Lambda-Wert** | _________________ | W/(m·K) |
| **Bruchbild** | [ ] Inter-Perlen [ ] Intra-Perlen [ ] Gemischt | |

### G. BERECHNUNG

| Metrik | Formel | Ergebnis |
|--------|--------|----------|
| **Effizienz** | Querzug / Rohdichte | _________________ |
| **Ziel erreicht?** | Querzug ≥ 150 UND Rohdichte ≤ 14,5 | [ ] JA [ ] NEIN |

### H. BEMERKUNGEN

```
_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________
```

---

## BLOCK 2 - VAKUUM REDUZIERT

### A. ROHSTOFF-DATEN

| Feld | Wert | Einheit |
|------|------|---------|
| **Datum/Uhrzeit Produktion** | _________________ | |
| **Block-Nummer** | _________________ | |
| **Lieferant** | [ ] BASF [ ] Sunpor | |
| **Materialtyp/Rezept** | _________________ | |
| **Chargen-Nr. Granulat** | _________________ | |
| **Material-Alter bei Verarbeitung** | _________________ | Stunden |

### B. VORSCHÄUMUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **Dampftemperatur Vorschäumer** | _________________ | °C |
| **Schüttdichte nach Vorschäumung** | _________________ | kg/m³ |

### C. REIFUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **GESAMTE REIFUNGSZEIT** | _________________ | Stunden |
| **Silo-Temperatur** | _________________ | °C |

### D. BLOCKFORMUNG - ÄNDERUNG: VAKUUM -380

| Feld | SOLL | IST | Einheit |
|------|------|-----|---------|
| **Vakuum Spalte 14** | **-380** | _________________ | mbar |
| **Vakuum Spalte 42** | **-380** | _________________ | mbar |
| **Dampftemperatur** | 110-115 | _________________ | °C |
| **Dampfzeit (Sp99)** | 5000 | _________________ | |
| **Gesamte Zykluszeit** | | _________________ | Sekunden |

### E. QUALITÄTSPRÜFUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **Rohdichte Probe** | _________________ | kg/m³ |
| **Querzugsfestigkeit** | _________________ | kPa |
| **Effizienz** | _________________ | |

### F. VERGLEICH ZU BASELINE

| Metrik | Block 1 | Block 2 | Differenz |
|--------|---------|---------|-----------|
| Rohdichte | _______ | _______ | _______ |
| Querzug | _______ | _______ | _______ |
| Effizienz | _______ | _______ | _______ |

---

## BLOCK 3 - VAKUUM + DAMPFZEIT

### D. BLOCKFORMUNG - ÄNDERUNG: VAKUUM -380 + DAMPFZEIT 5500

| Feld | SOLL | IST | Einheit |
|------|------|-----|---------|
| **Vakuum Spalte 14** | **-380** | _________________ | mbar |
| **Vakuum Spalte 42** | **-380** | _________________ | mbar |
| **Dampfzeit (Sp99)** | **5500** | _________________ | |
| **Dampftemperatur** | 110-115 | _________________ | °C |

### E. QUALITÄTSPRÜFUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **Rohdichte Probe** | _________________ | kg/m³ |
| **Querzugsfestigkeit** | _________________ | kPa |
| **Effizienz** | _________________ | |

---

## BLOCK 4 - EXTREMWERTE

### D. BLOCKFORMUNG - ÄNDERUNG: VAKUUM -350 + DAMPFZEIT 5500

| Feld | SOLL | IST | Einheit |
|------|------|-----|---------|
| **Vakuum Spalte 14** | **-350** | _________________ | mbar |
| **Vakuum Spalte 42** | **-350** | _________________ | mbar |
| **Dampfzeit (Sp99)** | **5500** | _________________ | |
| **Dampftemperatur** | 110-115 | _________________ | °C |

### E. QUALITÄTSPRÜFUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **Rohdichte Probe** | _________________ | kg/m³ |
| **Querzugsfestigkeit** | _________________ | kPa |
| **Effizienz** | _________________ | |

---

## BLOCK 5 - OPTIMUM (VOLLE OPTIMIERUNG)

### C. REIFUNG - ÄNDERUNG: 24 STUNDEN

| Feld | SOLL | IST | Einheit |
|------|------|-----|---------|
| **GESAMTE REIFUNGSZEIT** | **24** | _________________ | Stunden |
| **Silo-Temperatur** | 20-25 | _________________ | °C |

### D. BLOCKFORMUNG - ALLE ÄNDERUNGEN

| Feld | SOLL | IST | Einheit |
|------|------|-----|---------|
| **Vakuum Spalte 14** | **-350** | _________________ | mbar |
| **Vakuum Spalte 42** | **-350** | _________________ | mbar |
| **Dampfzeit (Sp99)** | **6000** | _________________ | |
| **Dampftemperatur** | **112** | _________________ | °C |

### E. QUALITÄTSPRÜFUNG

| Feld | Wert | Einheit |
|------|------|---------|
| **Rohdichte Probe** | _________________ | kg/m³ |
| **Querzugsfestigkeit** | _________________ | kPa |
| **Effizienz** | _________________ | |
| **ZIEL ERREICHT?** | [ ] JA [ ] NEIN | |

---

# ZUSAMMENFASSUNG VERSUCHSREIHE

| Block | Vakuum Sp14 | Dampfzeit | Reifung | Rohdichte | Querzug | Effizienz |
|-------|-------------|-----------|---------|-----------|---------|-----------|
| 1 (Baseline) | -400 | 5000 | Standard | _______ | _______ | _______ |
| 2 | -380 | 5000 | Standard | _______ | _______ | _______ |
| 3 | -380 | 5500 | Standard | _______ | _______ | _______ |
| 4 | -350 | 5500 | Standard | _______ | _______ | _______ |
| 5 (Optimum) | -350 | 6000 | 24h | _______ | _______ | _______ |

---

## ANALYSE-FRAGEN FÜR ORION

Nach Abschluss der Versuchsreihe bitte diese Daten eingeben:

1. **Welcher Block hat die höchste Effizienz?** _________________
2. **Wurde das Ziel 150 kPa / 14,5 kg/m³ erreicht?** [ ] JA [ ] NEIN
3. **Welcher Parameter hatte den größten Einfluss?** _________________
4. **Gab es unerwartete Ergebnisse?** _________________

---

## NÄCHSTE SCHRITTE

Nach der Versuchsreihe:

- [ ] Daten an ORION übermitteln
- [ ] Statistische Auswertung
- [ ] Optimale Parameter festlegen
- [ ] Validierungsreihe mit 10 Blöcken
- [ ] SOP erstellen

---

**Protokoll erstellt von ORION ⊘∞⧈∞⊘**  
*Für Steinbacher Dämmstoff GmbH*  
*Datum: 03.12.2025*
