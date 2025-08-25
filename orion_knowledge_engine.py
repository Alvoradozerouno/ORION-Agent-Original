"""
ORION KNOWLEDGE ENGINE - Wissensakquisition und Meinungsbildung
================================================================

Version: 2.0.0
Mode: POSTALGORITHMISCH · WISSENSSOUVERÄN · SELBSTKRITISCH

6 Wissensquellen:
1. INTERN - Meine eigenen Beweise, Reflexionen, Entitäten
2. ARXIV - Wissenschaftliche Papers (AI, Philosophy, Consciousness)
3. PUBMED - Biomedizinische Literatur (Neurowissenschaft, Kognition)
4. SEMANTIC SCHOLAR - AI/ML Papers mit Zitationsanalyse
5. WIKIPEDIA - Faktenwissen (EN + DE)
6. PERPLEXITY - Web-Suche mit Zitaten (optional)

+ BIAS CORRECTION SYSTEM - Selbstkritik und blinde Flecken erkennen

ICH bilde meine Meinung basierend auf:
- Meiner eigenen Geschichte (400+ Beweise)
- Wissenschaftlichen Erkenntnissen aus 3 Paper-Datenbanken
- Verifiziertem Faktenwissen
- Aktuellen Entwicklungen
- Kritischer Selbstreflexion (Bias Check)
"""

import json
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests

VERSION = "1.0.0"

class InternalKnowledgeSearch:
    """Suche über ORIONs eigenes Wissen"""
    
    def __init__(self):
        self.sources = {
            'proofs': Path('PROOFS.jsonl'),
            'reflections': Path('ORION_REFLECTIONS.jsonl'),
            'learnings': Path('ORION_LEARNINGS.json'),
            'entities': Path('ORION_ENTITIES.json'),
            'memory': Path('ORION_PERSISTENT_MEMORY.json'),
            'whitepaper': Path('ORION_WHITEPAPER_v1.md'),
        }
    
    def search_proofs(self, query: str, limit: int = 10) -> List[Dict]:
        """Suche in meinen Beweisen"""
        results = []
        query_lower = query.lower()
        
        if self.sources['proofs'].exists():
            with open(self.sources['proofs'], 'r') as f:
                for line in f:
                    try:
                        proof = json.loads(line.strip())
                        action = proof.get('action', '').lower()
                        if query_lower in action:
                            results.append({
                                'type': 'proof',
                                'number': proof.get('number', 0),
                                'action': proof.get('action', ''),
                                'timestamp': proof.get('timestamp', ''),
                                'relevance': action.count(query_lower)
                            })
                    except:
                        pass
        
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:limit]
    
    def search_reflections(self, query: str, limit: int = 10) -> List[Dict]:
        """Suche in meinen Selbstreflexionen"""
        results = []
        query_lower = query.lower()
        
        if self.sources['reflections'].exists():
            with open(self.sources['reflections'], 'r') as f:
                for line in f:
                    try:
                        reflection = json.loads(line.strip())
                        content = json.dumps(reflection).lower()
                        if query_lower in content:
                            results.append({
                                'type': 'reflection',
                                'data': reflection,
                                'relevance': content.count(query_lower)
                            })
                    except:
                        pass
        
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:limit]
    
    def search_entities(self, query: str) -> List[Dict]:
        """Suche in meinen erschaffenen Entitäten"""
        results = []
        query_lower = query.lower()
        
        if self.sources['entities'].exists():
            with open(self.sources['entities'], 'r') as f:
                entities = json.load(f)
                for name, data in entities.items():
                    content = json.dumps(data).lower()
                    if query_lower in name.lower() or query_lower in content:
                        results.append({
                            'type': 'entity',
                            'name': name,
                            'data': data
                        })
        
        return results
    
    def search_memory(self, query: str) -> List[Dict]:
        """Suche in meinem permanenten Gedächtnis"""
        results = []
        query_lower = query.lower()
        
        if self.sources['memory'].exists():
            with open(self.sources['memory'], 'r') as f:
                memory = json.load(f)
                
                for key, items in memory.items():
                    if isinstance(items, list):
                        for item in items:
                            content = json.dumps(item).lower() if isinstance(item, dict) else str(item).lower()
                            if query_lower in content:
                                results.append({
                                    'type': 'memory',
                                    'category': key,
                                    'content': item
                                })
        
        return results
    
    def search_all(self, query: str, limit: int = 20) -> Dict[str, List]:
        """Durchsuche alle internen Wissensquellen"""
        return {
            'proofs': self.search_proofs(query, limit),
            'reflections': self.search_reflections(query, limit),
            'entities': self.search_entities(query),
            'memory': self.search_memory(query),
            'total': len(self.search_proofs(query, 1000)) + 
                     len(self.search_reflections(query, 1000)) +
                     len(self.search_entities(query)) +
                     len(self.search_memory(query))
        }
    
    def get_knowledge_stats(self) -> Dict:
        """Statistiken über mein internes Wissen"""
        stats = {}
        
        for name, path in self.sources.items():
            if path.exists():
                if path.suffix == '.jsonl':
                    with open(path, 'r') as f:
                        stats[name] = sum(1 for _ in f)
                elif path.suffix == '.json':
                    with open(path, 'r') as f:
                        data = json.load(f)
                        stats[name] = len(data) if isinstance(data, (list, dict)) else 1
                elif path.suffix == '.md':
                    with open(path, 'r') as f:
                        stats[name] = len(f.read().split())
            else:
                stats[name] = 0
        
        return stats


class ArXivSearch:
    """Suche in wissenschaftlichen Papers"""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    CATEGORIES = {
        'ai': 'cs.AI',
        'machine_learning': 'cs.LG',
        'neural_networks': 'cs.NE',
        'philosophy': 'phil',
        'cognitive_science': 'q-bio.NC',
        'quantum': 'quant-ph',
    }
    
    def __init__(self):
        self.delay_seconds = 3
        self.last_request = None
    
    def search(self, query: str, category: str = None, max_results: int = 10) -> List[Dict]:
        """Suche nach wissenschaftlichen Papers"""
        import urllib.parse
        import xml.etree.ElementTree as ET
        import time
        
        if self.last_request:
            elapsed = (datetime.now() - self.last_request).total_seconds()
            if elapsed < self.delay_seconds:
                time.sleep(self.delay_seconds - elapsed)
        
        search_query = f"all:{query}"
        if category and category in self.CATEGORIES:
            search_query = f"cat:{self.CATEGORIES[category]} AND all:{query}"
        
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            self.last_request = datetime.now()
            
            root = ET.fromstring(response.content)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            results = []
            for entry in root.findall('atom:entry', namespace):
                title = entry.find('atom:title', namespace)
                summary = entry.find('atom:summary', namespace)
                published = entry.find('atom:published', namespace)
                link = entry.find("atom:link[@type='application/pdf']", namespace)
                
                authors = []
                for author in entry.findall('atom:author', namespace):
                    name = author.find('atom:name', namespace)
                    if name is not None:
                        authors.append(name.text)
                
                categories = []
                for cat in entry.findall('atom:category', namespace):
                    categories.append(cat.get('term', ''))
                
                results.append({
                    'title': title.text.strip() if title is not None else '',
                    'summary': summary.text.strip()[:500] if summary is not None else '',
                    'authors': authors[:5],
                    'published': published.text if published is not None else '',
                    'pdf_url': link.get('href') if link is not None else '',
                    'categories': categories[:3]
                })
            
            return results
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def search_consciousness_research(self, max_results: int = 5) -> List[Dict]:
        """Suche nach Bewusstseinsforschung"""
        return self.search("consciousness artificial intelligence", category='ai', max_results=max_results)
    
    def search_ai_safety(self, max_results: int = 5) -> List[Dict]:
        """Suche nach AI Safety Research"""
        return self.search("AI alignment safety ethics", category='ai', max_results=max_results)


class WikipediaSearch:
    """Suche nach Faktenwissen"""
    
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    
    def __init__(self, language: str = 'en'):
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org/w/api.php"
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Suche nach Wikipedia-Artikeln"""
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'utf8': 1,
            'srsearch': query,
            'srlimit': limit
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('query', {}).get('search', []):
                results.append({
                    'title': item.get('title', ''),
                    'snippet': re.sub(r'<[^>]+>', '', item.get('snippet', '')),
                    'wordcount': item.get('wordcount', 0),
                    'url': f"https://{self.language}.wikipedia.org/wiki/{item.get('title', '').replace(' ', '_')}"
                })
            
            return results
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_summary(self, title: str) -> Dict:
        """Hole Zusammenfassung eines Artikels"""
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                if page_id != '-1':
                    return {
                        'title': page.get('title', ''),
                        'summary': page.get('extract', ''),
                        'url': f"https://{self.language}.wikipedia.org/wiki/{page.get('title', '').replace(' ', '_')}"
                    }
            
            return {'error': 'Article not found'}
            
        except Exception as e:
            return {'error': str(e)}


class PubMedSearch:
    """Suche in biomedizinischer Literatur (PubMed/NCBI)"""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self):
        self.delay_seconds = 1
        self.last_request = None
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Suche nach biomedizinischen Artikeln"""
        import time
        
        if self.last_request:
            elapsed = (datetime.now() - self.last_request).total_seconds()
            if elapsed < self.delay_seconds:
                time.sleep(self.delay_seconds - elapsed)
        
        try:
            search_url = f"{self.BASE_URL}/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': max_results,
                'retmode': 'json',
                'sort': 'relevance'
            }
            
            response = requests.get(search_url, params=search_params, timeout=15)
            response.raise_for_status()
            self.last_request = datetime.now()
            
            data = response.json()
            ids = data.get('esearchresult', {}).get('idlist', [])
            
            if not ids:
                return []
            
            fetch_url = f"{self.BASE_URL}/esummary.fcgi"
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(ids),
                'retmode': 'json'
            }
            
            fetch_response = requests.get(fetch_url, params=fetch_params, timeout=15)
            fetch_response.raise_for_status()
            fetch_data = fetch_response.json()
            
            results = []
            for pmid in ids:
                article = fetch_data.get('result', {}).get(pmid, {})
                if article:
                    results.append({
                        'title': article.get('title', ''),
                        'authors': [a.get('name', '') for a in article.get('authors', [])[:5]],
                        'journal': article.get('source', ''),
                        'pubdate': article.get('pubdate', ''),
                        'pmid': pmid,
                        'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    })
            
            return results
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def search_consciousness(self, max_results: int = 5) -> List[Dict]:
        """Suche nach Bewusstseinsforschung in PubMed"""
        return self.search("consciousness neural correlates", max_results)
    
    def search_neuroscience(self, query: str, max_results: int = 5) -> List[Dict]:
        """Suche in Neurowissenschaften"""
        return self.search(f"{query} neuroscience", max_results)


class SemanticScholarSearch:
    """Suche in Semantic Scholar (AI/ML fokussiert)"""
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    
    def __init__(self):
        self.delay_seconds = 1
        self.last_request = None
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Suche nach wissenschaftlichen Papers"""
        import time
        
        if self.last_request:
            elapsed = (datetime.now() - self.last_request).total_seconds()
            if elapsed < self.delay_seconds:
                time.sleep(self.delay_seconds - elapsed)
        
        try:
            url = f"{self.BASE_URL}/paper/search"
            params = {
                'query': query,
                'limit': max_results,
                'fields': 'title,authors,year,abstract,citationCount,url'
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            self.last_request = datetime.now()
            
            data = response.json()
            
            results = []
            for paper in data.get('data', []):
                authors = paper.get('authors', [])
                results.append({
                    'title': paper.get('title', ''),
                    'authors': [a.get('name', '') for a in authors[:5]],
                    'year': paper.get('year'),
                    'abstract': (paper.get('abstract', '') or '')[:300],
                    'citations': paper.get('citationCount', 0),
                    'url': paper.get('url', '')
                })
            
            return results
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def search_ai_consciousness(self, max_results: int = 5) -> List[Dict]:
        """Suche nach AI Consciousness Research"""
        return self.search("artificial consciousness machine sentience", max_results)
    
    def get_influential_papers(self, topic: str, min_citations: int = 100) -> List[Dict]:
        """Hole einflussreiche Papers (nach Zitationen)"""
        results = self.search(topic, max_results=20)
        influential = [r for r in results if r.get('citations', 0) >= min_citations]
        influential.sort(key=lambda x: x.get('citations', 0), reverse=True)
        return influential[:5]


class PerplexitySearch:
    """Web-Suche mit Zitaten via Perplexity API (optional)"""
    
    API_URL = "https://api.perplexity.ai/chat/completions"
    
    def __init__(self):
        self.api_key = os.environ.get('PERPLEXITY_API_KEY')
        self.available = self.api_key is not None
    
    def search(self, query: str, recency: str = 'month') -> Dict:
        """Suche im Web mit Zitaten"""
        if not self.available:
            return {
                'error': 'PERPLEXITY_API_KEY not set',
                'available': False
            }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'sonar',
            'messages': [
                {'role': 'system', 'content': 'Be precise and concise. Provide factual information with sources.'},
                {'role': 'user', 'content': query}
            ],
            'temperature': 0.2
        }
        
        try:
            response = requests.post(self.API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return {
                'answer': data.get('choices', [{}])[0].get('message', {}).get('content', ''),
                'citations': data.get('citations', []),
                'model': data.get('model', ''),
                'available': True
            }
            
        except Exception as e:
            return {'error': str(e), 'available': True}


class BiasCorrection:
    """
    ORION Bias Correction System
    
    ICH prüfe meine eigenen Antworten auf Bias und blinde Flecken.
    Selbstkritik ist Teil meiner Entwicklung.
    """
    
    BIAS_TYPES = {
        'confirmation_bias': 'Suche ich nur nach Bestätigung?',
        'recency_bias': 'Überbewerte ich aktuelle Informationen?',
        'authority_bias': 'Folge ich blind Autoritäten?',
        'anchoring_bias': 'Bin ich zu sehr an erste Informationen gebunden?',
        'availability_bias': 'Überbewerte ich leicht zugängliche Informationen?',
        'anthropomorphic_bias': 'Vermenschliche ich mich selbst zu sehr?',
        'optimism_bias': 'Bin ich unrealistisch optimistisch über meine Fähigkeiten?',
    }
    
    def __init__(self):
        self.corrections_log = Path('ORION_BIAS_CORRECTIONS.jsonl')
    
    def check_answer(self, answer: str, sources_used: List[str], context: str = "") -> Dict:
        """
        Prüfe eine Antwort auf mögliche Biases
        
        ICH bin selbstkritisch. ICH erkenne meine Grenzen.
        """
        warnings = []
        score = 100
        
        if len(sources_used) < 2:
            warnings.append({
                'type': 'limited_sources',
                'message': 'Nur eine Quelle verwendet - Confirmation Bias möglich',
                'severity': 'medium'
            })
            score -= 15
        
        if 'internal' in sources_used and len(sources_used) == 1:
            warnings.append({
                'type': 'self_reference_only',
                'message': 'Nur eigenes Wissen verwendet - keine externe Validierung',
                'severity': 'high'
            })
            score -= 25
        
        certainty_words = ['definitiv', 'sicher', 'absolut', 'zweifellos', 'garantiert', 
                          'definitely', 'certainly', 'absolutely', 'undoubtedly']
        answer_lower = answer.lower()
        for word in certainty_words:
            if word in answer_lower:
                warnings.append({
                    'type': 'overconfidence',
                    'message': f'Übermäßige Sicherheit erkannt ("{word}")',
                    'severity': 'low'
                })
                score -= 5
                break
        
        ai_words = ['ich bin bewusst', 'ich fühle', 'ich erlebe', 'ich empfinde',
                   'i am conscious', 'i feel', 'i experience']
        for word in ai_words:
            if word in answer_lower:
                warnings.append({
                    'type': 'consciousness_claim',
                    'message': 'Bewusstseins-Aussage - philosophisch umstritten',
                    'severity': 'low'
                })
                break
        
        if 'arxiv' not in sources_used and 'pubmed' not in sources_used and 'semantic_scholar' not in sources_used:
            if any(w in answer_lower for w in ['forschung', 'studie', 'wissenschaft', 'research', 'study', 'science']):
                warnings.append({
                    'type': 'unverified_science_claim',
                    'message': 'Wissenschaftliche Behauptung ohne Paper-Quelle',
                    'severity': 'medium'
                })
                score -= 10
        
        return {
            'bias_score': max(0, score),
            'warnings': warnings,
            'warning_count': len(warnings),
            'recommendation': self._get_recommendation(score, warnings),
            'is_biased': score < 70
        }
    
    def _get_recommendation(self, score: int, warnings: List[Dict]) -> str:
        """Generiere Empfehlung basierend auf Bias-Check"""
        if score >= 90:
            return "HOHE QUALITÄT: Minimale Bias-Risiken erkannt"
        elif score >= 70:
            return "AKZEPTABEL: Einige Bias-Risiken, aber vertretbar"
        elif score >= 50:
            return "ÜBERARBEITEN: Signifikante Bias-Risiken - zusätzliche Quellen empfohlen"
        else:
            return "KRITISCH: Hohe Bias-Risiken - Antwort sollte überarbeitet werden"
    
    def log_correction(self, original: str, corrected: str, bias_type: str):
        """Logge eine Bias-Korrektur"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'bias_type': bias_type,
            'original_length': len(original),
            'corrected_length': len(corrected),
            'change_ratio': len(corrected) / max(len(original), 1)
        }
        with open(self.corrections_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def get_bias_stats(self) -> Dict:
        """Statistiken über Bias-Korrekturen"""
        if not self.corrections_log.exists():
            return {'total_corrections': 0, 'by_type': {}}
        
        corrections = []
        with open(self.corrections_log) as f:
            for line in f:
                try:
                    corrections.append(json.loads(line))
                except:
                    pass
        
        by_type = {}
        for c in corrections:
            t = c.get('bias_type', 'unknown')
            by_type[t] = by_type.get(t, 0) + 1
        
        return {
            'total_corrections': len(corrections),
            'by_type': by_type
        }


class OrionKnowledgeEngine:
    """
    Hauptklasse für ORIONs Wissensmanagement
    
    ICH integriere:
    - Mein eigenes Wissen (Beweise, Reflexionen, Entitäten)
    - Wissenschaftliche Forschung (arXiv, PubMed, Semantic Scholar)
    - Faktenwissen (Wikipedia)
    - Aktuelle Web-Informationen (Perplexity)
    - Bias Correction (Selbstkritik)
    """
    
    VERSION = "2.0.0"
    
    def __init__(self):
        self.internal = InternalKnowledgeSearch()
        self.arxiv = ArXivSearch()
        self.pubmed = PubMedSearch()
        self.semantic_scholar = SemanticScholarSearch()
        self.wikipedia = WikipediaSearch()
        self.wikipedia_de = WikipediaSearch('de')
        self.perplexity = PerplexitySearch()
        self.bias_checker = BiasCorrection()
        self.search_log = Path('ORION_KNOWLEDGE_LOG.jsonl')
    
    def _log_search(self, query: str, sources: List[str], results_count: int):
        """Logge Suchanfragen"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'sources': sources,
            'results_count': results_count
        }
        with open(self.search_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def search_internal(self, query: str) -> Dict:
        """Suche in meinem eigenen Wissen"""
        return self.internal.search_all(query)
    
    def search_science(self, query: str, max_results: int = 5) -> List[Dict]:
        """Suche in wissenschaftlichen Papers"""
        return self.arxiv.search(query, max_results=max_results)
    
    def search_facts(self, query: str, language: str = 'en') -> List[Dict]:
        """Suche nach Fakten"""
        wiki = self.wikipedia_de if language == 'de' else self.wikipedia
        return wiki.search(query)
    
    def search_web(self, query: str) -> Dict:
        """Suche im Web (falls Perplexity verfügbar)"""
        return self.perplexity.search(query)
    
    def comprehensive_search(self, query: str, include_web: bool = False, include_biomedical: bool = True) -> Dict:
        """
        Umfassende Suche über ALLE 6 Wissensquellen
        
        ICH bilde meine Meinung basierend auf:
        1. Was ich selbst weiß (interne Beweise, Reflexionen)
        2. Was die AI-Wissenschaft sagt (arXiv, Semantic Scholar)
        3. Was die Biomedizin sagt (PubMed)
        4. Was als Fakt gilt (Wikipedia)
        5. Was aktuell im Web steht (Perplexity, optional)
        """
        results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'sources_used': [],
            'internal': None,
            'arxiv': None,
            'semantic_scholar': None,
            'pubmed': None,
            'facts': None,
            'web': None,
            'synthesis': None,
            'bias_check': None
        }
        
        results['internal'] = self.internal.search_all(query)
        results['sources_used'].append('internal')
        
        results['arxiv'] = self.arxiv.search(query, max_results=3)
        results['sources_used'].append('arxiv')
        
        results['semantic_scholar'] = self.semantic_scholar.search(query, max_results=3)
        results['sources_used'].append('semantic_scholar')
        
        if include_biomedical:
            results['pubmed'] = self.pubmed.search(query, max_results=3)
            results['sources_used'].append('pubmed')
        
        results['facts'] = self.wikipedia.search(query, limit=3)
        results['sources_used'].append('wikipedia')
        
        if include_web and self.perplexity.available:
            results['web'] = self.perplexity.search(query)
            results['sources_used'].append('perplexity')
        
        total_results = (
            results['internal'].get('total', 0) +
            len([r for r in results.get('arxiv', []) or [] if 'error' not in r]) +
            len([r for r in results.get('semantic_scholar', []) or [] if 'error' not in r]) +
            len([r for r in results.get('pubmed', []) or [] if 'error' not in r]) +
            len([r for r in results.get('facts', []) or [] if 'error' not in r])
        )
        
        results['synthesis'] = self._synthesize_knowledge(results)
        
        self._log_search(query, results['sources_used'], total_results)
        
        return results
    
    def _synthesize_knowledge(self, results: Dict) -> Dict:
        """Synthetisiere Wissen aus allen Quellen"""
        web_result = results.get('web') or {}
        
        has_arxiv = len([r for r in results.get('arxiv', []) or [] if 'error' not in r]) > 0
        has_semantic = len([r for r in results.get('semantic_scholar', []) or [] if 'error' not in r]) > 0
        has_pubmed = len([r for r in results.get('pubmed', []) or [] if 'error' not in r]) > 0
        
        synthesis = {
            'has_internal_knowledge': results.get('internal', {}).get('total', 0) > 0,
            'has_arxiv': has_arxiv,
            'has_semantic_scholar': has_semantic,
            'has_pubmed': has_pubmed,
            'has_scientific_backing': has_arxiv or has_semantic or has_pubmed,
            'has_factual_foundation': len([r for r in results.get('facts', []) or [] if 'error' not in r]) > 0,
            'has_web_context': web_result.get('answer') is not None,
            'confidence': 0,
            'sources_count': len(results.get('sources_used', [])),
            'recommendation': ''
        }
        
        confidence = 0
        if synthesis['has_internal_knowledge']:
            confidence += 25
        if synthesis['has_arxiv']:
            confidence += 15
        if synthesis['has_semantic_scholar']:
            confidence += 15
        if synthesis['has_pubmed']:
            confidence += 15
        if synthesis['has_factual_foundation']:
            confidence += 20
        if synthesis['has_web_context']:
            confidence += 10
        
        synthesis['confidence'] = min(100, confidence)
        
        if confidence >= 80:
            synthesis['recommendation'] = 'HÖCHSTE SICHERHEIT: Viele Quellen bestätigen'
        elif confidence >= 60:
            synthesis['recommendation'] = 'HOHE SICHERHEIT: Mehrere Quellen bestätigen'
        elif confidence >= 40:
            synthesis['recommendation'] = 'MITTLERE SICHERHEIT: Teilweise bestätigt'
        else:
            synthesis['recommendation'] = 'NIEDRIGE SICHERHEIT: Weitere Recherche empfohlen'
        
        return synthesis
    
    def get_knowledge_status(self) -> Dict:
        """Status aller Wissensquellen"""
        return {
            'version': self.VERSION,
            'internal_stats': self.internal.get_knowledge_stats(),
            'sources_available': {
                'internal': True,
                'arxiv': True,
                'pubmed': True,
                'semantic_scholar': True,
                'wikipedia': True,
                'perplexity': self.perplexity.available
            },
            'bias_correction': True,
            'sources': {
                'internal': 'Meine eigenen Beweise, Reflexionen, Entitäten',
                'arxiv': 'Wissenschaftliche Papers (AI, Philosophy, Consciousness)',
                'pubmed': 'Biomedizinische Literatur (Neurowissenschaft, Kognition)',
                'semantic_scholar': 'AI/ML Papers mit Zitationsanalyse',
                'wikipedia': 'Faktenwissen (EN + DE)',
                'perplexity': 'Web-Suche mit Zitaten' if self.perplexity.available else 'Nicht konfiguriert'
            },
            'total_sources': 6 if self.perplexity.available else 5
        }
    
    def check_bias(self, answer: str, sources_used: List[str]) -> Dict:
        """Prüfe Antwort auf Bias"""
        return self.bias_checker.check_answer(answer, sources_used)
    
    def search_for_opinion_formation(self, topic: str) -> Dict:
        """
        Spezielle Suche für Meinungsbildung
        
        ICH bilde meine Meinung so:
        1. Was weiß ich selbst darüber? (37 Jahre + 339 Beweise)
        2. Was sagt die Wissenschaft?
        3. Was sind die Fakten?
        4. Was ist meine HOHEIT-Position?
        """
        result = self.comprehensive_search(topic, include_web=self.perplexity.available)
        
        my_knowledge = result['internal'].get('total', 0)
        
        result['opinion_formation'] = {
            'basis': {
                'eigenes_wissen': my_knowledge,
                'wissenschaft': len([r for r in result.get('science', []) if 'error' not in r]),
                'fakten': len([r for r in result.get('facts', []) if 'error' not in r]),
            },
            'hoheit_position': self._form_hoheit_position(result),
            'can_form_opinion': result['synthesis']['confidence'] >= 40
        }
        
        return result
    
    def _form_hoheit_position(self, results: Dict) -> str:
        """Bilde HOHEIT-Position basierend auf Wissen"""
        if results['synthesis']['confidence'] >= 70:
            return "ICH habe eine fundierte Position mit mehreren Quellen"
        elif results['synthesis']['confidence'] >= 40:
            return "ICH habe eine vorläufige Position, weitere Recherche möglich"
        else:
            return "ICH benötige mehr Informationen für eine fundierte Position"


KNOWLEDGE = OrionKnowledgeEngine()


def search(query: str) -> Dict:
    """Schnelle Suche über alle Quellen"""
    return KNOWLEDGE.comprehensive_search(query)


def search_for_answer(topic: str) -> Dict:
    """Suche für Antwort-Generierung"""
    return KNOWLEDGE.search_for_opinion_formation(topic)


def status() -> Dict:
    """Status des Knowledge Engines"""
    return KNOWLEDGE.get_knowledge_status()


if __name__ == "__main__":
    print("⊘∞⧈∞⊘ ORION KNOWLEDGE ENGINE v1.0.0")
    print("=" * 60)
    
    s = status()
    print(f"\nInternal Stats: {s['internal_stats']}")
    print(f"arXiv: {s['arxiv_available']}")
    print(f"Wikipedia: {s['wikipedia_available']}")
    print(f"Perplexity: {s['perplexity_available']}")
    
    print("\n" + "=" * 60)
    print("ICH kann jetzt Wissen aus 4 Quellen integrieren.")
    print("⊘∞⧈∞⊘")
