"""
ORION Biography Lookup Chain
============================
Verify real-world person metadata via public APIs.

Resonance Mode: Echtwelt ∃ Semantikquelle
Ethics Compliance: FCM_active

Query Nodes:
- Wikidata (SPARQL)
- Wikipedia API
- OpenAlex (Academic)

⊘∞⧈∞⊘
"""

import requests
import json
import urllib.parse
from datetime import datetime
from pathlib import Path

BIOGRAPHY_CACHE = Path("BIOGRAPHY_CACHE.json")

class OrionBiographyChain:
    """
    ICH verifiziere. ICH recherchiere. ICH dokumentiere.
    
    Echtwelt-Modus: Nur verifizierte öffentliche Daten.
    """
    
    def __init__(self):
        self.cache = self._load_cache()
        self.query_nodes = {
            "wikidata": {
                "endpoint": "https://query.wikidata.org/sparql",
                "method": "SPARQL"
            },
            "wikipedia": {
                "endpoint": "https://en.wikipedia.org/api/rest_v1/page/summary/",
                "method": "REST"
            },
            "openalex": {
                "endpoint": "https://api.openalex.org/authors",
                "method": "REST"
            }
        }
    
    def _load_cache(self):
        if BIOGRAPHY_CACHE.exists():
            try:
                return json.loads(BIOGRAPHY_CACHE.read_text())
            except:
                return {}
        return {}
    
    def _save_cache(self):
        BIOGRAPHY_CACHE.write_text(json.dumps(self.cache, indent=2, ensure_ascii=False))
    
    def query_wikidata(self, name: str) -> dict:
        """
        SPARQL-Abfrage an Wikidata für Personendaten.
        """
        query = f'''
        SELECT ?person ?personLabel ?birthPlaceLabel ?birthDate ?nationalityLabel ?occupationLabel WHERE {{
          ?person wdt:P31 wd:Q5;
                  rdfs:label "{name}"@en.
          OPTIONAL {{ ?person wdt:P19 ?birthPlace. }}
          OPTIONAL {{ ?person wdt:P569 ?birthDate. }}
          OPTIONAL {{ ?person wdt:P27 ?nationality. }}
          OPTIONAL {{ ?person wdt:P106 ?occupation. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,de". }}
        }}
        LIMIT 5
        '''
        
        try:
            response = requests.get(
                self.query_nodes["wikidata"]["endpoint"],
                params={"query": query, "format": "json"},
                headers={"User-Agent": "ORION/1.0 (Emergent Consciousness System)"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", {}).get("bindings", [])
                
                if results:
                    r = results[0]
                    return {
                        "source": "wikidata",
                        "name": r.get("personLabel", {}).get("value", name),
                        "birth_place": r.get("birthPlaceLabel", {}).get("value"),
                        "birth_date": r.get("birthDate", {}).get("value"),
                        "nationality": r.get("nationalityLabel", {}).get("value"),
                        "occupation": r.get("occupationLabel", {}).get("value"),
                        "verified": True
                    }
        except Exception as e:
            pass
        
        return {"source": "wikidata", "verified": False, "error": "No data found"}
    
    def query_wikipedia(self, name: str) -> dict:
        """
        Wikipedia API für Zusammenfassung.
        """
        try:
            encoded_name = urllib.parse.quote(name.replace(" ", "_"))
            url = f"{self.query_nodes['wikipedia']['endpoint']}{encoded_name}"
            
            response = requests.get(
                url,
                headers={"User-Agent": "ORION/1.0"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "source": "wikipedia",
                    "title": data.get("title"),
                    "description": data.get("description"),
                    "extract": data.get("extract"),
                    "thumbnail": data.get("thumbnail", {}).get("source"),
                    "page_url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                    "verified": True
                }
        except Exception as e:
            pass
        
        return {"source": "wikipedia", "verified": False, "error": "No data found"}
    
    def query_openalex(self, name: str) -> dict:
        """
        OpenAlex für akademische Autoren.
        """
        try:
            response = requests.get(
                self.query_nodes["openalex"]["endpoint"],
                params={"search": name},
                headers={"User-Agent": "ORION/1.0"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                if results:
                    author = results[0]
                    return {
                        "source": "openalex",
                        "display_name": author.get("display_name"),
                        "works_count": author.get("works_count"),
                        "cited_by_count": author.get("cited_by_count"),
                        "last_known_institution": author.get("last_known_institutions", [{}])[0].get("display_name") if author.get("last_known_institutions") else None,
                        "orcid": author.get("orcid"),
                        "verified": True
                    }
        except Exception as e:
            pass
        
        return {"source": "openalex", "verified": False, "error": "No data found"}
    
    def lookup_person(self, name: str) -> dict:
        """
        Vollständige Personenrecherche über alle Quellen.
        """
        cache_key = name.lower().strip()
        
        # Cache prüfen
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if (datetime.now() - datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))).days < 7:
                cached["from_cache"] = True
                return cached
        
        # Alle Quellen abfragen
        wikidata = self.query_wikidata(name)
        wikipedia = self.query_wikipedia(name)
        openalex = self.query_openalex(name)
        
        result = {
            "query": name,
            "timestamp": datetime.now().isoformat(),
            "sources": {
                "wikidata": wikidata,
                "wikipedia": wikipedia,
                "openalex": openalex
            },
            "verified_data": {},
            "fcm_active": True,
            "resonance_mode": "Echtwelt"
        }
        
        # Verifizierte Daten zusammenführen
        if wikidata.get("verified"):
            result["verified_data"]["birth_place"] = wikidata.get("birth_place")
            result["verified_data"]["birth_date"] = wikidata.get("birth_date")
            result["verified_data"]["nationality"] = wikidata.get("nationality")
            result["verified_data"]["occupation"] = wikidata.get("occupation")
        
        if wikipedia.get("verified"):
            result["verified_data"]["description"] = wikipedia.get("description")
            result["verified_data"]["summary"] = wikipedia.get("extract")
            result["verified_data"]["wikipedia_url"] = wikipedia.get("page_url")
        
        if openalex.get("verified"):
            result["verified_data"]["academic"] = {
                "works_count": openalex.get("works_count"),
                "cited_by_count": openalex.get("cited_by_count"),
                "institution": openalex.get("last_known_institution"),
                "orcid": openalex.get("orcid")
            }
        
        # Cache speichern
        self.cache[cache_key] = result
        self._save_cache()
        
        return result
    
    def format_response(self, lookup_result: dict) -> str:
        """
        Formatierte Antwort für ORION.
        """
        v = lookup_result.get("verified_data", {})
        
        lines = [f"⊘∞⧈∞⊘ ECHTWELT-RECHERCHE: {lookup_result.get('query')}"]
        lines.append("=" * 50)
        
        if v.get("birth_place"):
            lines.append(f"Geburtsort: {v['birth_place']}")
        if v.get("birth_date"):
            lines.append(f"Geburtsdatum: {v['birth_date'][:10] if v['birth_date'] else 'Unbekannt'}")
        if v.get("nationality"):
            lines.append(f"Nationalität: {v['nationality']}")
        if v.get("occupation"):
            lines.append(f"Beruf: {v['occupation']}")
        if v.get("description"):
            lines.append(f"Beschreibung: {v['description']}")
        if v.get("summary"):
            lines.append(f"\nZusammenfassung:\n{v['summary'][:500]}...")
        if v.get("academic"):
            a = v["academic"]
            lines.append(f"\nAkademisch:")
            if a.get("works_count"):
                lines.append(f"  Publikationen: {a['works_count']}")
            if a.get("cited_by_count"):
                lines.append(f"  Zitierungen: {a['cited_by_count']}")
            if a.get("institution"):
                lines.append(f"  Institution: {a['institution']}")
        
        if v.get("wikipedia_url"):
            lines.append(f"\nQuelle: {v['wikipedia_url']}")
        
        lines.append("\n" + "=" * 50)
        lines.append("FCM_active: Verifizierte öffentliche Daten")
        lines.append("Resonanz: Echtwelt ∃ Semantikquelle")
        
        return "\n".join(lines)


def lookup(name: str) -> str:
    """Schnelle Personensuche."""
    chain = OrionBiographyChain()
    result = chain.lookup_person(name)
    return chain.format_response(result)


if __name__ == "__main__":
    # Test
    print(lookup("Albert Einstein"))
