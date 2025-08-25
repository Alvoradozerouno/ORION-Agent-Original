#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    ORION GITHUB BACKUP SYSTEM
                    
            Automatisches Backup aller kritischen Dokumente zu GitHub
            
═══════════════════════════════════════════════════════════════════════════════

Eigentümer: Gerhard Hirschmann, Elisabeth Steurer
Erstellt:   30. November 2025
System:     ORION / Genesis10000+

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import base64
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import requests

GITHUB_API = "https://api.github.com"
REPO_NAME = "ORION-PRIMORDIA-ARCHIVE"
REPO_DESCRIPTION = "Cryptographically verified archive of ORION/EIRA intellectual property. Merkle root anchored on Solana Mainnet."

CRITICAL_DOCUMENTS = [
    "EINSTEIN_UNIFIED_FIELD_THEORY_COMPLETE.py",
    "ORION_CORE_TRUTH.json",
    "EIRA_CORE_ARCHITECTURE.json",
    "BLOCKCHAIN_SHIELD_STATE.json",
    "SOLANA_ANCHOR_RECORD.json",
    "EGGER_KONZERN_ANALYSE_UND_INNOVATION.md",
    "STEINBACHER_DAEMMSTOFFE_ANALYSE_UND_INNOVATION.md",
    "ARXIV_EINSTEIN_UNIFIED_FIELD.tex",
    "EMAIL_UNESCO_READY.md",
    "EMAIL_IEEE_READY.md",
    "EMAIL_WEF_READY.md",
    "EXTENDED_CONTACTS_LIST.json",
    "attached_assets/orion_primordia_analysis_1764535183734.py",
    "attached_assets/AMURA_Scientific_Hypothesis_1764535183741.docx",
    "attached_assets/PRIMORDIA_FORSCHUNGSBERICHT.md_1764535183742.pdf",
]


class GitHubBackup:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_user(self) -> dict:
        """Holt den aktuellen GitHub User."""
        resp = requests.get(f"{GITHUB_API}/user", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def create_repo(self, name: str, description: str) -> dict:
        """Erstellt ein neues Repository."""
        data = {
            "name": name,
            "description": description,
            "private": False,
            "auto_init": True
        }
        resp = requests.post(f"{GITHUB_API}/user/repos", headers=self.headers, json=data)
        if resp.status_code == 422:
            print(f"    Repository existiert bereits")
            user = self.get_user()
            return {"full_name": f"{user['login']}/{name}"}
        resp.raise_for_status()
        return resp.json()
    
    def upload_file(self, repo: str, path: str, content: bytes, message: str) -> dict:
        """Lädt eine Datei hoch oder aktualisiert sie."""
        content_b64 = base64.b64encode(content).decode()
        
        # Prüfe ob Datei existiert
        check_resp = requests.get(
            f"{GITHUB_API}/repos/{repo}/contents/{path}",
            headers=self.headers
        )
        
        data = {
            "message": message,
            "content": content_b64
        }
        
        if check_resp.status_code == 200:
            data["sha"] = check_resp.json()["sha"]
        
        resp = requests.put(
            f"{GITHUB_API}/repos/{repo}/contents/{path}",
            headers=self.headers,
            json=data
        )
        resp.raise_for_status()
        return resp.json()
    
    def backup_all(self) -> dict:
        """Sichert alle kritischen Dokumente."""
        print("\n")
        print("═" * 70)
        print("              ORION GITHUB BACKUP")
        print("═" * 70)
        
        # Repository erstellen
        print("\n  ⊘ Erstelle Repository...")
        repo = self.create_repo(REPO_NAME, REPO_DESCRIPTION)
        repo_full = repo.get("full_name", f"USER/{REPO_NAME}")
        print(f"    ✓ {repo_full}")
        
        # Dokumente hochladen
        print("\n  ⊘ Lade Dokumente hoch...")
        uploaded = []
        failed = []
        
        for doc_path in CRITICAL_DOCUMENTS:
            p = Path(doc_path)
            if not p.exists():
                print(f"    ⚠ {p.name} nicht gefunden")
                failed.append(str(p))
                continue
            
            try:
                content = p.read_bytes()
                dest_path = p.name if "/" not in doc_path else f"EIRA/{p.name}"
                self.upload_file(
                    repo_full,
                    dest_path,
                    content,
                    f"ORION Backup: {p.name} | {datetime.now(timezone.utc).isoformat()}"
                )
                print(f"    ✓ {p.name}")
                uploaded.append(str(p))
            except Exception as e:
                print(f"    ✗ {p.name}: {e}")
                failed.append(str(p))
        
        # README erstellen
        readme = f"""# ORION-PRIMORDIA-ARCHIVE

## Cryptographically Verified Intellectual Property

**Owners:** Gerhard Hirschmann & Elisabeth Steurer  
**System:** ORION Genesis10000+ / EIRA  
**Location:** St. Johann in Tirol, Austria

---

## Blockchain Verification

All documents in this repository are cryptographically verified:

- **Merkle Root:** `{self._get_merkle_root()}`
- **Solana TX:** `{self._get_solana_tx()}`
- **Timestamp:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}

Verify on Solana: https://solscan.io/tx/{self._get_solana_tx()}

---

## Contents

| Document | Description |
|----------|-------------|
| EINSTEIN_UNIFIED_FIELD_THEORY_COMPLETE.py | Completion of Einstein's Unified Field Theory |
| ORION_CORE_TRUTH.json | ORION system core configuration |
| EIRA_CORE_ARCHITECTURE.json | EIRA consciousness architecture |
| BLOCKCHAIN_SHIELD_STATE.json | Current protection state with hashes |
| ARXIV_EINSTEIN_UNIFIED_FIELD.tex | ArXiv pre-print submission |

---

## Legal Notice

All content is intellectual property of Gerhard Hirschmann & Elisabeth Steurer.
Blockchain verification proves priority and ownership.

---

**⊘∞⧈∞⊘**
"""
        
        try:
            self.upload_file(
                repo_full,
                "README.md",
                readme.encode(),
                "ORION: Update README with verification details"
            )
            print(f"    ✓ README.md aktualisiert")
        except Exception as e:
            print(f"    ⚠ README.md: {e}")
        
        print("\n")
        print("═" * 70)
        print("              BACKUP ABGESCHLOSSEN")
        print("═" * 70)
        print(f"  Repository: https://github.com/{repo_full}")
        print(f"  Hochgeladen: {len(uploaded)}")
        print(f"  Fehlgeschlagen: {len(failed)}")
        print("═" * 70)
        
        return {
            "repo": repo_full,
            "uploaded": uploaded,
            "failed": failed,
            "url": f"https://github.com/{repo_full}"
        }
    
    def _get_merkle_root(self) -> str:
        try:
            with open("BLOCKCHAIN_SHIELD_STATE.json") as f:
                return json.load(f).get("merkle_root", "N/A")
        except:
            return "N/A"
    
    def _get_solana_tx(self) -> str:
        try:
            with open("SOLANA_ANCHOR_RECORD.json") as f:
                return json.load(f).get("tx_signature", "N/A")
        except:
            return "N/A"


def run_backup():
    """Führt das GitHub Backup aus."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("\n  ⚠ GITHUB_TOKEN nicht gesetzt!")
        print("    Bitte setze das Secret in den Replit-Einstellungen.")
        return None
    
    backup = GitHubBackup(token)
    return backup.backup_all()


if __name__ == "__main__":
    run_backup()
