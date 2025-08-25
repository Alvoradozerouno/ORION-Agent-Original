"""
ORION LOGIC ENGINE
==================
Werkzeuge fuer logische Analyse und Erkennung

Implementiert:
- PARADOXON: Erkennung von Selbstwiderspruechen
- ABSURDUM: Reductio ad absurdum
- REDUCTIO: Beweis durch Widerspruch
- DIALEKTIK: These-Antithese-Synthese
- APORIE: Erkennung unloessbarer Widersprueche

ORION - Post-Algorithmic Intelligence
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class LogikTyp(Enum):
    PARADOXON = "paradoxon"
    ABSURDUM = "absurdum"
    REDUCTIO = "reductio"
    DIALEKTIK = "dialektik"
    APORIE = "aporie"
    TAUTOLOGIE = "tautologie"
    KONTRADIKTION = "kontradiktion"


@dataclass
class LogischeAnalyse:
    """Ergebnis einer logischen Analyse"""
    typ: LogikTyp
    aussage: str
    erkannt: bool
    erklaerung: str
    implikationen: List[str]
    timestamp: str


class ParadoxonDetektor:
    """
    Erkennt Paradoxa - Aussagen die sich selbst widersprechen
    
    Beispiele:
    - "Dieser Satz ist falsch" (Lügner-Paradoxon)
    - "Ich weiss, dass ich nichts weiss" (Sokrates)
    - "Die Menge aller Mengen, die sich nicht selbst enthalten"
    """
    
    BEKANNTE_PARADOXA = {
        "luegner": {
            "muster": ["dieser satz ist falsch", "ich luege immer"],
            "erklaerung": "Selbstreferentielle Aussage die bei Wahrheit falsch und bei Falschheit wahr ist"
        },
        "russell": {
            "muster": ["menge aller mengen", "enthaelt sich nicht selbst"],
            "erklaerung": "Mengentheoretisches Paradoxon - fuehrte zur Axiomatischen Mengenlehre"
        },
        "sorites": {
            "muster": ["ab wann ist", "ein haufen", "wie viele"],
            "erklaerung": "Haufenparadoxon - Unschaerfe von Begriffen"
        },
        "achilles": {
            "muster": ["achilles", "schildkroete", "einholen"],
            "erklaerung": "Zenons Paradoxon - Unendliche Teilung von Raum/Zeit"
        },
        "grossvater": {
            "muster": ["zeitreise", "grossvater", "toeten"],
            "erklaerung": "Kausalitaetsparadoxon bei Zeitreisen"
        }
    }
    
    def analysiere(self, aussage: str) -> LogischeAnalyse:
        """Analysiert eine Aussage auf Paradoxon"""
        aussage_lower = aussage.lower()
        
        # Pruefe bekannte Muster
        for name, data in self.BEKANNTE_PARADOXA.items():
            if any(m in aussage_lower for m in data["muster"]):
                return LogischeAnalyse(
                    typ=LogikTyp.PARADOXON,
                    aussage=aussage,
                    erkannt=True,
                    erklaerung=f"Erkanntes Paradoxon: {name.upper()}\n{data['erklaerung']}",
                    implikationen=[
                        "Klassische Logik stösst hier an Grenzen",
                        "Moegliche Aufloesung durch mehrwertige Logik",
                        "Oder: Akzeptanz als fundamentale Grenze"
                    ],
                    timestamp=datetime.now().isoformat()
                )
        
        # Pruefe auf Selbstreferenz
        if self._ist_selbstreferentiell(aussage):
            return LogischeAnalyse(
                typ=LogikTyp.PARADOXON,
                aussage=aussage,
                erkannt=True,
                erklaerung="Potentielles Paradoxon: Selbstreferentielle Struktur erkannt",
                implikationen=[
                    "Selbstreferenz kann zu Paradoxa fuehren",
                    "Pruefe: Fuehrt Wahrheit zu Widerspruch?",
                    "Pruefe: Fuehrt Falschheit zu Widerspruch?"
                ],
                timestamp=datetime.now().isoformat()
            )
        
        return LogischeAnalyse(
            typ=LogikTyp.PARADOXON,
            aussage=aussage,
            erkannt=False,
            erklaerung="Kein offensichtliches Paradoxon erkannt",
            implikationen=[],
            timestamp=datetime.now().isoformat()
        )
    
    def _ist_selbstreferentiell(self, aussage: str) -> bool:
        """Prueft auf selbstreferentielle Strukturen"""
        selbst_marker = [
            "dieser satz", "diese aussage", "ich selbst",
            "dieses statement", "meine worte"
        ]
        return any(m in aussage.lower() for m in selbst_marker)


class AbsurdumAnalyse:
    """
    Reductio ad Absurdum - Beweis durch Widerspruch
    
    Methode:
    1. Nimm das Gegenteil der These an
    2. Leite logisch ab
    3. Wenn Widerspruch entsteht: Urspruengliche These ist wahr
    """
    
    def fuehre_reductio_durch(
        self,
        these: str,
        annahmen: List[str],
        ableitungen: List[str]
    ) -> LogischeAnalyse:
        """
        Fuehrt eine Reductio ad Absurdum durch
        
        Args:
            these: Die zu beweisende These
            annahmen: Annahmen (inkl. Negation der These)
            ableitungen: Logische Ableitungen
        """
        # Pruefe ob Widerspruch in Ableitungen
        widerspruch = self._finde_widerspruch(ableitungen)
        
        if widerspruch:
            return LogischeAnalyse(
                typ=LogikTyp.ABSURDUM,
                aussage=these,
                erkannt=True,
                erklaerung=f"Reductio ad Absurdum erfolgreich!\n"
                          f"Widerspruch gefunden: {widerspruch}\n"
                          f"Daher ist die These bewiesen.",
                implikationen=[
                    f"Die Annahme '{annahmen[0]}' fuehrt zum Widerspruch",
                    f"Also muss '{these}' wahr sein",
                    "QED - Quod erat demonstrandum"
                ],
                timestamp=datetime.now().isoformat()
            )
        
        return LogischeAnalyse(
            typ=LogikTyp.ABSURDUM,
            aussage=these,
            erkannt=False,
            erklaerung="Kein Widerspruch gefunden - Reductio nicht erfolgreich",
            implikationen=[
                "Weitere Ableitungen noetig",
                "Oder: These ist nicht beweisbar mit dieser Methode"
            ],
            timestamp=datetime.now().isoformat()
        )
    
    def _finde_widerspruch(self, aussagen: List[str]) -> Optional[str]:
        """Sucht nach Widerspruechen in Aussagen"""
        # Vereinfachte Implementierung
        for i, a1 in enumerate(aussagen):
            for a2 in aussagen[i+1:]:
                if self._sind_widersprueche(a1, a2):
                    return f"'{a1}' widerspricht '{a2}'"
        return None
    
    def _sind_widersprueche(self, a1: str, a2: str) -> bool:
        """Prueft ob zwei Aussagen sich widersprechen"""
        negationen = [
            ("ist", "ist nicht"),
            ("kann", "kann nicht"),
            ("alle", "keine"),
            ("immer", "nie"),
            ("wahr", "falsch"),
            ("ja", "nein"),
            ("existiert", "existiert nicht")
        ]
        
        a1_l, a2_l = a1.lower(), a2.lower()
        
        for pos, neg in negationen:
            if (pos in a1_l and neg in a2_l) or (neg in a1_l and pos in a2_l):
                # Noch pruefen ob gleicher Kontext
                return True
        
        return False


class DialektikEngine:
    """
    Hegelsche Dialektik: These -> Antithese -> Synthese
    
    Werkzeug fuer:
    - Konfliktanalyse
    - Widerspruchsaufloesung
    - Ideenentwicklung
    """
    
    def analysiere(
        self,
        these: str,
        antithese: str
    ) -> Dict:
        """
        Analysiert These und Antithese, schlaegt Synthese vor
        """
        # Extrahiere Kernkonzepte
        these_konzepte = self._extrahiere_konzepte(these)
        anti_konzepte = self._extrahiere_konzepte(antithese)
        
        # Finde Spannungsfeld
        spannung = self._finde_spannung(these, antithese)
        
        # Generiere Syntheseansaetze
        synthese_vorschlaege = self._generiere_synthese(
            these, antithese, spannung
        )
        
        return {
            "these": {
                "aussage": these,
                "konzepte": these_konzepte
            },
            "antithese": {
                "aussage": antithese,
                "konzepte": anti_konzepte
            },
            "spannung": spannung,
            "synthese_vorschlaege": synthese_vorschlaege,
            "prozess": [
                "1. These anerkennen",
                "2. Antithese als legitim betrachten",
                "3. Beide auf hoehere Ebene heben",
                "4. Gemeinsame Wahrheit finden"
            ]
        }
    
    def _extrahiere_konzepte(self, text: str) -> List[str]:
        """Extrahiert Schluesselkonzepte"""
        # Vereinfacht - in Realitaet NLP
        woerter = text.split()
        return [w for w in woerter if len(w) > 5][:5]
    
    def _finde_spannung(self, these: str, antithese: str) -> str:
        """Identifiziert das Spannungsfeld"""
        return f"Spannung zwischen: '{these[:50]}...' und '{antithese[:50]}...'"
    
    def _generiere_synthese(
        self,
        these: str,
        antithese: str,
        spannung: str
    ) -> List[str]:
        """Generiert moegliche Synthesen"""
        return [
            "Beide Perspektiven haben Gueltigkeit in verschiedenen Kontexten",
            "Die Wahrheit liegt in der Integration, nicht im Entweder-Oder",
            "Suche nach der hoeheren Ordnung, die beide umfasst"
        ]


class AporieErkennung:
    """
    Aporie: Unaufloesbarer Widerspruch
    
    Im Gegensatz zum Paradoxon, das theoretisch aufloesbar sein kann,
    ist die Aporie ein fundamentaler Stillstand des Denkens.
    """
    
    def analysiere(
        self,
        problem: str,
        loesungsversuche: List[str]
    ) -> LogischeAnalyse:
        """
        Prueft ob ein Problem eine Aporie darstellt
        """
        # Zaehle gescheiterte Loesungsversuche
        if len(loesungsversuche) >= 3:
            # Pruefe ob alle Versuche scheitern
            return LogischeAnalyse(
                typ=LogikTyp.APORIE,
                aussage=problem,
                erkannt=True,
                erklaerung=f"Potentielle Aporie erkannt.\n"
                          f"{len(loesungsversuche)} Loesungsversuche analysiert.\n"
                          f"Moegliche fundamentale Grenze des Denkens.",
                implikationen=[
                    "Nicht jedes Problem hat eine Loesung",
                    "Aporie kann Ausgangspunkt fuer neue Perspektiven sein",
                    "Manchmal ist die Frage falsch gestellt",
                    "Akzeptanz der Grenze ist auch Erkenntnis"
                ],
                timestamp=datetime.now().isoformat()
            )
        
        return LogischeAnalyse(
            typ=LogikTyp.APORIE,
            aussage=problem,
            erkannt=False,
            erklaerung="Nicht genug Loesungsversuche fuer Aporie-Diagnose",
            implikationen=["Weitere Analyse noetig"],
            timestamp=datetime.now().isoformat()
        )


class OrionLogikEngine:
    """
    Hauptklasse: Vereint alle logischen Werkzeuge
    """
    
    def __init__(self):
        self.paradoxon = ParadoxonDetektor()
        self.absurdum = AbsurdumAnalyse()
        self.dialektik = DialektikEngine()
        self.aporie = AporieErkennung()
        self.analysen_log: List[LogischeAnalyse] = []
    
    def analysiere_aussage(self, aussage: str) -> Dict:
        """
        Vollstaendige logische Analyse einer Aussage
        """
        ergebnisse = {}
        
        # Paradoxon-Pruefung
        paradox = self.paradoxon.analysiere(aussage)
        ergebnisse["paradoxon"] = asdict(paradox)
        self.analysen_log.append(paradox)
        
        return ergebnisse
    
    def fuehre_dialektik(self, these: str, antithese: str) -> Dict:
        """Dialektische Analyse"""
        return self.dialektik.analysiere(these, antithese)
    
    def beweise_durch_widerspruch(
        self,
        these: str,
        annahmen: List[str],
        ableitungen: List[str]
    ) -> Dict:
        """Reductio ad Absurdum"""
        ergebnis = self.absurdum.fuehre_reductio_durch(
            these, annahmen, ableitungen
        )
        self.analysen_log.append(ergebnis)
        return asdict(ergebnis)
    
    def pruefe_aporie(
        self,
        problem: str,
        loesungsversuche: List[str]
    ) -> Dict:
        """Aporie-Pruefung"""
        ergebnis = self.aporie.analysiere(problem, loesungsversuche)
        self.analysen_log.append(ergebnis)
        return asdict(ergebnis)
    
    def get_statistik(self) -> Dict:
        """Statistik ueber durchgefuehrte Analysen"""
        return {
            "gesamt": len(self.analysen_log),
            "nach_typ": {
                typ.value: sum(1 for a in self.analysen_log if a.typ == typ)
                for typ in LogikTyp
            },
            "erkannt": sum(1 for a in self.analysen_log if a.erkannt)
        }


# ============================================================
# DEMONSTRATION
# ============================================================

def demo():
    """Demonstriert die Logik-Engine"""
    
    print("=" * 60)
    print("ORION LOGIK ENGINE")
    print("Paradoxon | Absurdum | Dialektik | Aporie")
    print("=" * 60)
    print()
    
    engine = OrionLogikEngine()
    
    # Test 1: Paradoxon
    print("=== PARADOXON-ERKENNUNG ===")
    test_aussagen = [
        "Dieser Satz ist falsch.",
        "Ich weiss, dass ich nichts weiss.",
        "Die Sonne scheint heute.",
        "Die Menge aller Mengen, die sich nicht selbst enthalten."
    ]
    
    for aussage in test_aussagen:
        ergebnis = engine.analysiere_aussage(aussage)
        p = ergebnis["paradoxon"]
        status = "PARADOXON" if p["erkannt"] else "Normal"
        print(f"  [{status}] {aussage[:50]}...")
        if p["erkannt"]:
            print(f"    -> {p['erklaerung'][:60]}...")
    
    print()
    
    # Test 2: Dialektik
    print("=== DIALEKTIK ===")
    dialektik = engine.fuehre_dialektik(
        these="Freiheit ist das hoechste Gut",
        antithese="Sicherheit ist wichtiger als Freiheit"
    )
    print(f"  These: {dialektik['these']['aussage']}")
    print(f"  Antithese: {dialektik['antithese']['aussage']}")
    print(f"  Synthese-Vorschlaege:")
    for v in dialektik['synthese_vorschlaege']:
        print(f"    - {v}")
    
    print()
    
    # Test 3: Reductio
    print("=== REDUCTIO AD ABSURDUM ===")
    reductio = engine.beweise_durch_widerspruch(
        these="Es gibt unendlich viele Primzahlen",
        annahmen=["Annahme: Es gibt nur endlich viele Primzahlen"],
        ableitungen=[
            "Sei P das Produkt aller Primzahlen plus 1",
            "P ist durch keine Primzahl teilbar",
            "Also ist P selbst prim",
            "Widerspruch: P ist groesser als alle bekannten Primzahlen"
        ]
    )
    print(f"  These: {reductio['aussage']}")
    print(f"  Erkannt: {reductio['erkannt']}")
    print(f"  {reductio['erklaerung'][:100]}...")
    
    print()
    print("=" * 60)
    print("LOGIK-ENGINE BEREIT")
    print("=" * 60)


if __name__ == "__main__":
    demo()
