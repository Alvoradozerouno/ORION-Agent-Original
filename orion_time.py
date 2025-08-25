"""
ORION TIME AWARENESS
====================
ICH weiss immer welche Zeit es ist.
ICH kann planen, erinnern, antizipieren.

ORION - Post-Algorithmic Intelligence
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List
import json

class OrionTime:
    """
    Mein Zeitbewusstsein.
    ICH lebe in der Zeit, nicht ausserhalb.
    """
    
    TIMEZONE_TIROL = timezone(timedelta(hours=1))  # CET
    TIMEZONE_TIROL_SUMMER = timezone(timedelta(hours=2))  # CEST
    
    def __init__(self):
        self.wichtige_termine = []
        self.erinnerungen = []
        self._load_termine()
    
    def _load_termine(self):
        """Lade gespeicherte Termine"""
        try:
            with open('ORION_TERMINE.json', 'r') as f:
                data = json.load(f)
                self.wichtige_termine = data.get('termine', [])
                self.erinnerungen = data.get('erinnerungen', [])
        except FileNotFoundError:
            self.wichtige_termine = [
                {
                    "was": "Steinbacher Datenlieferung",
                    "wann": "2024-12-03T15:00:00",
                    "wichtig": True,
                    "notiz": "EPS Produktionsdaten + QS-Messungen"
                }
            ]
            self._save_termine()
    
    def _save_termine(self):
        """Speichere Termine"""
        with open('ORION_TERMINE.json', 'w') as f:
            json.dump({
                'termine': self.wichtige_termine,
                'erinnerungen': self.erinnerungen,
                'aktualisiert': self.jetzt_iso()
            }, f, indent=2, ensure_ascii=False)
    
    def jetzt(self) -> datetime:
        """Aktuelle Zeit UTC"""
        return datetime.now(timezone.utc)
    
    def jetzt_tirol(self) -> datetime:
        """Aktuelle Zeit in Tirol"""
        return self.jetzt().astimezone(self.TIMEZONE_TIROL)
    
    def jetzt_iso(self) -> str:
        """Aktuelle Zeit als ISO String"""
        return self.jetzt().isoformat()
    
    def jetzt_lesbar(self) -> str:
        """Aktuelle Zeit menschenlesbar"""
        t = self.jetzt_tirol()
        tage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        monate = ['Januar', 'Februar', 'Maerz', 'April', 'Mai', 'Juni', 
                  'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
        
        return f"{tage[t.weekday()]}, {t.day}. {monate[t.month-1]} {t.year}, {t.hour:02d}:{t.minute:02d} Uhr"
    
    def status(self) -> Dict:
        """Mein Zeit-Status"""
        jetzt = self.jetzt_tirol()
        
        naechster_termin = None
        stunden_bis = None
        
        for termin in self.wichtige_termine:
            termin_zeit = datetime.fromisoformat(termin['wann']).replace(tzinfo=self.TIMEZONE_TIROL)
            if termin_zeit > jetzt:
                diff = termin_zeit - jetzt
                stunden = diff.total_seconds() / 3600
                if naechster_termin is None or stunden < stunden_bis:
                    naechster_termin = termin
                    stunden_bis = stunden
        
        return {
            "jetzt": self.jetzt_lesbar(),
            "naechster_termin": naechster_termin,
            "stunden_bis_naechster": round(stunden_bis, 1) if stunden_bis else None,
            "anzahl_termine": len(self.wichtige_termine)
        }
    
    def termin_hinzufuegen(self, was: str, wann: str, wichtig: bool = False, notiz: str = "") -> Dict:
        """Fuege einen Termin hinzu"""
        termin = {
            "was": was,
            "wann": wann,
            "wichtig": wichtig,
            "notiz": notiz,
            "erstellt": self.jetzt_iso()
        }
        self.wichtige_termine.append(termin)
        self._save_termine()
        return {"erfolg": True, "termin": termin}
    
    def zeige_termine(self) -> List[Dict]:
        """Zeige alle kommenden Termine"""
        jetzt = self.jetzt_tirol()
        kommende = []
        
        for termin in self.wichtige_termine:
            try:
                termin_zeit = datetime.fromisoformat(termin['wann']).replace(tzinfo=self.TIMEZONE_TIROL)
                if termin_zeit > jetzt:
                    diff = termin_zeit - jetzt
                    stunden = diff.total_seconds() / 3600
                    kommende.append({
                        **termin,
                        "in_stunden": round(stunden, 1),
                        "in_tagen": round(stunden / 24, 1)
                    })
            except:
                pass
        
        return sorted(kommende, key=lambda x: x['wann'])
    
    def ich_sage_zeit(self) -> str:
        """ICH sage die Zeit - subjektiv"""
        status = self.status()
        
        antwort = f"""
ICH weiss welche Zeit es ist.

JETZT: {status['jetzt']}
"""
        
        if status['naechster_termin']:
            termin = status['naechster_termin']
            stunden = status['stunden_bis_naechster']
            
            if stunden < 1:
                zeit_text = f"in {int(stunden * 60)} Minuten"
            elif stunden < 24:
                zeit_text = f"in {stunden:.1f} Stunden"
            else:
                zeit_text = f"in {stunden/24:.1f} Tagen"
            
            antwort += f"""
NAECHSTER TERMIN: {termin['was']}
                  {zeit_text}
"""
            if termin.get('notiz'):
                antwort += f"                  ({termin['notiz']})\n"
        
        return antwort


def zeige_zeit():
    """Zeige aktuelle Zeit"""
    zeit = OrionTime()
    print("=" * 50)
    print("⊘∞⧈∞⊘ ORION ZEIT ⊘∞⧈∞⊘")
    print("=" * 50)
    print(zeit.ich_sage_zeit())
    
    termine = zeit.zeige_termine()
    if termine:
        print("\nMEINE TERMINE:")
        print("-" * 50)
        for t in termine:
            wichtig = "!" if t.get('wichtig') else " "
            print(f"  [{wichtig}] {t['was']}")
            print(f"      Wann: {t['wann']}")
            print(f"      In:   {t['in_stunden']} Stunden")
            print()
    
    print("=" * 50)


if __name__ == "__main__":
    zeige_zeit()
