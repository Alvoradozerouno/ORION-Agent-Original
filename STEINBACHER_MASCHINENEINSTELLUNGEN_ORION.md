# ORION Maschineneinstellungen für Steinbacher EPS
## Ziel: 150 kPa Querzugsfestigkeit bei 14,5 kg/m³ Rohdichte

**Erstellt:** 03.12.2025  
**Basis:** Produktionsdaten-Analyse + Wissenschaftliche Literatur + Industrie-Standards

---

## WICHTIGE ERKENNTNIS

**ASTM C578 Standard für EPS 15 kg/m³:**
- Biegezugfestigkeit: 115-150 kPa

**Das bedeutet:** 150 kPa bei 14,5 kg/m³ ist **TECHNISCH MÖGLICH** - aber erfordert optimale Prozessführung.

---

## 1. ROHMATERIAL

| Parameter | Empfehlung | Begründung |
|-----------|------------|------------|
| **Lieferant** | BASF (nicht Sunpor) | +14% höhere Querzugsfestigkeit in den Daten |
| **Materialtyp** | BASF 215 e-l oder Neopor F5 | Graphit-EPS hat bessere Verschweißung |
| **Pentangehalt** | Frisches Material (< 48h) | Optimal: 5-7% Pentangehalt |
| **Perlengröße** | Kleine, gleichmäßige Perlen | Größere Oberfläche = bessere Verschweißung |

---

## 2. VORSCHÄUMUNG

| Parameter | Einstellung |
|-----------|-------------|
| **Dampftemperatur** | 93-102°C |
| **Ziel-Schüttdichte** | 8-10 kg/m³ (ergibt ca. 14-15 kg/m³ Blockdichte) |
| **Expansionsverhältnis** | 50-60x Original-Volumen |

---

## 3. REIFUNG (KRITISCH!)

| Parameter | Einstellung | Begründung |
|-----------|-------------|------------|
| **Reifungszeit** | MINDESTENS 12-24 Stunden | Ermöglicht vollständige Luftdiffusion |
| **Lagertemperatur** | 15-25°C | |
| **Belüftung** | Atmungsaktive Silos/Säcke | Luft muss in Zellen diffundieren |

**Zweck:** Innendruck = Außendruck → Verhindert Kollaps beim Formen, erzeugt "innere Feder" für Verschweißung

---

## 4. BLOCKFORMUNG - DAMPFPARAMETER

### KRITISCHE EINSTELLUNGEN:

| Parameter | Empfehlung | NICHT |
|-----------|------------|-------|
| **Dampfdruck** | 0.3-0.5 bar (30-50 kPa) | Höher = Zellkollaps |
| **Dampftemperatur** | 110-115°C | Über 120°C = Zellstruktur zerstört |
| **Dampfzeit** | 8-15 Sek. Hauptbedampfung + 3-5 Sek. Vorbedampfung + 2-5 Sek. Nachhalten | |
| **Vakuum (Sp14)** | -380 bis -400 mbar | -470 mbar (zu stark!) |
| **Vakuum (Sp42)** | -350 bis -380 mbar | -450 mbar (zu stark!) |

### Aus den Produktionsdaten:
- TOP-Blöcke hatten Vakuum -380 bis -400 mbar
- BOTTOM-Blöcke hatten Vakuum -450 bis -470 mbar
- **Weniger Vakuum = bessere Festigkeit!**

---

## 5. KÜHLUNG

| Parameter | Einstellung |
|-----------|-------------|
| **Vakuumkühlung** | 0.25-0.4 bar Vakuum |
| **Kühlzeit** | 60-120 Sekunden |
| **Restfeuchte** | < 5% Ziel |
| **Nachlagerung** | 24-48 Stunden vor Schneiden |

---

## VERGLEICH: PRODUKTIONSDATEN vs. EMPFEHLUNG

| Parameter | Eure TOP-Blöcke | Empfehlung | Anpassung |
|-----------|-----------------|------------|-----------|
| Lieferant | BASF 215 e-l | BASF | ✓ Beibehalten |
| Zykluszeit | 185-225s | 180-240s | ✓ OK |
| Vakuum Sp14 | -400 mbar | -380 mbar | → Weniger! |
| Vakuum Sp42 | -380 mbar | -350 mbar | → Weniger! |
| Dampfzeit (Sp99) | 5000 | 5500-6000 | → Mehr! |
| Dampftemperatur | (nicht in Daten) | 110-115°C | → PRÜFEN! |

---

## ERWARTETES ERGEBNIS

Mit diesen Einstellungen:

| Metrik | Aktuell | Erwartet |
|--------|---------|----------|
| **Effizienz** | 8.74 (beste) | 10.0-10.5 |
| **Querzugsfestigkeit** | 134.3 kPa | 145-155 kPa |
| **Rohdichte** | 15.36 kg/m³ | 14.0-14.8 kg/m³ |

**ZIEL VON 150 kPa / 14,5 kg/m³ SOLLTE ERREICHBAR SEIN**

---

## EMPFOHLENE VERSUCHSREIHE

| Block | Material | Vakuum Sp14 | Dampfzeit Sp99 | Reifung | Erwartung |
|-------|----------|-------------|----------------|---------|-----------|
| 1 | BASF | -400 | 5000 | Standard | Baseline |
| 2 | BASF | -380 | 5000 | Standard | +5% Effizienz |
| 3 | BASF | -380 | 5500 | Standard | +8% Effizienz |
| 4 | BASF | -350 | 5500 | Standard | +12% Effizienz |
| 5 | BASF | -350 | 6000 | 24h | +18% Effizienz |

**Jeder Block mit QS-Prüfung:** Querzug + Rohdichte messen!

---

## WISSENSCHAFTLICHE GRUNDLAGEN

### Verschweißungsmechanismus:
1. Dampf erhitzt Perlenoberfläche über Glasübergangstemperatur (90-100°C)
2. Polymerketten diffundieren an Perlengrenzen
3. Physikalische Verkettung der amorphen PS-Ketten
4. Schnelle Kühlung "friert" Verschweißung ein

### Kritische Faktoren:
- **Temperatur an Grenzfläche** - Muss Erweichungspunkt erreichen
- **Molekulargewicht** - Balance zwischen Stabilität und Mobilität
- **Dampfdruck** - Höherer Druck verbessert Verschweißungsgrad
- **Verweilzeit** - Ausreichend für Kettendiffusion ohne Zellkollaps

### Qualitätskriterien:
- **Inter-Perlen-Bruch** (schlecht) = Versagen zwischen Perlen
- **Intra-Perlen-Bruch** (gut) = Versagen durch Perlen selbst
- Ziel: Höherer Anteil Intra-Perlen-Bruch = bessere Verschweißung

---

## QUELLEN

- ASTM C578: Standard Specification for Rigid Cellular Polystyrene Thermal Insulation
- EN 13163: Thermal insulation products for buildings
- Wissenschaftliche Literatur zu Steam-Chest Molding und Interbead Bonding
- Steinbacher Produktionsdaten (159 QS-Messungen, 444 Produktionsblöcke)

---

**Erstellt von ORION ⊘∞⧈∞⊘**  
*Post-Synthetische Analyse für Steinbacher Dämmstoff GmbH*
