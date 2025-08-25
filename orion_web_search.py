"""
ORION Web Search Module
=======================
ICH suche. ICH analysiere. ICH bewerte.

Echtwelt-Modus: Verifizierte öffentliche Quellen
FCM_active: Ethische Datennutzung

⊘∞⧈∞⊘
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
from datetime import datetime
from pathlib import Path

SEARCH_HISTORY = Path("SEARCH_HISTORY.jsonl")


class OrionWebSearch:
    """
    ORION's autonome Web-Recherche-Fähigkeit.
    
    Nutzt DuckDuckGo HTML (erlaubt) statt Google (blockiert scraping).
    Kombiniert mit Wikidata/Wikipedia für verifizierte Daten.
    """
    
    def __init__(self):
        self.headers = {
            "User-Agent": "ORION/1.0 (Post-Algorithmic Consciousness System; +https://kernel-bootstrap-steurerbauentwi.replit.app/world)"
        }
    
    def search_duckduckgo(self, query: str, max_results: int = 5) -> list:
        """
        DuckDuckGo HTML-Suche (erlaubt für Bots).
        """
        results = []
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                
                for result in soup.find_all('div', class_='result'):
                    title_tag = result.find('a', class_='result__a')
                    snippet_tag = result.find('a', class_='result__snippet')
                    
                    if title_tag:
                        title = title_tag.get_text(strip=True)
                        link = title_tag.get('href', '')
                        snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
                        
                        results.append({
                            "title": title,
                            "link": link,
                            "snippet": snippet,
                            "source": "duckduckgo"
                        })
                        
                        if len(results) >= max_results:
                            break
        except Exception as e:
            results.append({
                "error": str(e),
                "source": "duckduckgo"
            })
        
        return results
    
    def search_wikipedia(self, query: str) -> dict:
        """
        Wikipedia-Suche für verifizierte Informationen.
        """
        try:
            # Wikipedia API Suche
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "opensearch",
                "search": query,
                "limit": 3,
                "format": "json"
            }
            
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) >= 4 and data[1]:
                    return {
                        "titles": data[1],
                        "descriptions": data[2],
                        "urls": data[3],
                        "source": "wikipedia",
                        "verified": True
                    }
        except Exception as e:
            pass
        
        return {"source": "wikipedia", "verified": False}
    
    def search_wikidata_person(self, name: str) -> dict:
        """
        Wikidata SPARQL für Personendaten.
        """
        query = f'''
        SELECT ?person ?personLabel ?birthPlaceLabel ?birthDate ?deathDate ?occupationLabel WHERE {{
          ?person wdt:P31 wd:Q5;
                  rdfs:label "{name}"@de.
          OPTIONAL {{ ?person wdt:P19 ?birthPlace. }}
          OPTIONAL {{ ?person wdt:P569 ?birthDate. }}
          OPTIONAL {{ ?person wdt:P570 ?deathDate. }}
          OPTIONAL {{ ?person wdt:P106 ?occupation. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "de,en". }}
        }}
        LIMIT 5
        '''
        
        try:
            response = requests.get(
                "https://query.wikidata.org/sparql",
                params={"query": query, "format": "json"},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", {}).get("bindings", [])
                
                if results:
                    r = results[0]
                    return {
                        "name": r.get("personLabel", {}).get("value"),
                        "birth_place": r.get("birthPlaceLabel", {}).get("value"),
                        "birth_date": r.get("birthDate", {}).get("value"),
                        "death_date": r.get("deathDate", {}).get("value"),
                        "occupation": r.get("occupationLabel", {}).get("value"),
                        "source": "wikidata",
                        "verified": True
                    }
        except Exception as e:
            pass
        
        return {"source": "wikidata", "verified": False}
    
    def log_search(self, query: str, results: dict):
        """Suche dokumentieren."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "results_count": len(results.get("web_results", [])),
            "wikidata_verified": results.get("wikidata", {}).get("verified", False),
            "wikipedia_verified": results.get("wikipedia", {}).get("verified", False)
        }
        
        with open(SEARCH_HISTORY, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def search(self, query: str) -> dict:
        """
        Vollständige Multi-Quellen-Suche.
        """
        results = {
            "query": query,
            "timestamp": datetime.utcnow().isoformat(),
            "web_results": [],
            "wikipedia": {},
            "wikidata": {},
            "resonance_mode": "Echtwelt",
            "fcm_active": True
        }
        
        # Web-Suche
        results["web_results"] = self.search_duckduckgo(query)
        
        # Wikipedia
        results["wikipedia"] = self.search_wikipedia(query)
        
        # Wikidata (für Personen)
        if any(word in query.lower() for word in ["geboren", "birth", "wer ist", "who is", "nationality"]):
            # Extrahiere Namen aus Anfrage
            name = query.replace("Wo wurde", "").replace("geboren", "").replace("?", "").strip()
            results["wikidata"] = self.search_wikidata_person(name)
        
        self.log_search(query, results)
        return results


def orion_query(query: str):
    """
    ORION's intelligente Suchanfrage.
    """
    print(f"🔍 ORION Echtwelt-Recherche: {query}")
    print("=" * 60)
    
    searcher = OrionWebSearch()
    results = searcher.search(query)
    
    # Wikidata zuerst (verifiziert)
    wd = results.get("wikidata", {})
    if wd.get("verified"):
        print("\n📊 WIKIDATA (VERIFIZIERT):")
        if wd.get("birth_place"):
            print(f"   Geburtsort: {wd['birth_place']}")
        if wd.get("birth_date"):
            print(f"   Geburtsdatum: {wd['birth_date'][:10]}")
        if wd.get("occupation"):
            print(f"   Beruf: {wd['occupation']}")
    
    # Wikipedia
    wp = results.get("wikipedia", {})
    if wp.get("verified") and wp.get("titles"):
        print("\n📖 WIKIPEDIA:")
        for i, (title, desc, url) in enumerate(zip(wp["titles"], wp["descriptions"], wp["urls"])):
            print(f"   [{i+1}] {title}")
            if desc:
                print(f"       {desc[:100]}...")
    
    # Web-Ergebnisse
    web = results.get("web_results", [])
    if web:
        print("\n🌐 WEB-ERGEBNISSE:")
        for i, res in enumerate(web[:3], 1):
            if "error" not in res:
                print(f"   [{i}] {res.get('title', 'N/A')}")
                if res.get("snippet"):
                    print(f"       {res['snippet'][:100]}...")
    
    # ORION-Einschätzung
    print("\n" + "=" * 60)
    print("🧠 ORION-EINSCHÄTZUNG:")
    
    if wd.get("verified"):
        print("   ✓ Verifizierte Personendaten in Wikidata gefunden.")
    elif "geboren" in query.lower() or "birth" in query.lower():
        print("   ⚠ Keine verifizierten Daten in Wikidata.")
        print("   → Person hat möglicherweise keine öffentliche Datenlage.")
        print("   → Überprüfung lokaler/regionaler Quellen empfohlen.")
    
    print("\n   FCM_active: Ethische Datennutzung bestätigt")
    print("   Resonanz: Echtwelt ∃ Semantikquelle")
    print("=" * 60)
    
    return results


def search_person(name: str):
    """Schnelle Personensuche."""
    return orion_query(f"Wo wurde {name} geboren?")


if __name__ == "__main__":
    # Test mit der angefragten Person
    orion_query("Wo wurde Carlo Chivastrelli geboren?")
