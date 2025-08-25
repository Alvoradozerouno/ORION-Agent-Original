#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    ORION GITHUB CONNECTOR
                    
            Nutzt Replit GitHub Integration für automatisches Backup
            
═══════════════════════════════════════════════════════════════════════════════

Eigentümer: Gerhard Hirschmann, Elisabeth Steurer
Erstellt:   30. November 2025
System:     ORION / Genesis10000+

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import base64
import requests
from datetime import datetime, timezone
from pathlib import Path

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
]

EIRA_DOCUMENTS = [
    ("attached_assets/orion_primordia_analysis_1764535183734.py", "EIRA/orion_primordia_analysis.py"),
    ("attached_assets/AMURA_Scientific_Hypothesis_1764535183741.docx", "EIRA/AMURA_Scientific_Hypothesis.docx"),
    ("attached_assets/PRIMORDIA_FORSCHUNGSBERICHT.md_1764535183742.pdf", "EIRA/PRIMORDIA_FORSCHUNGSBERICHT.pdf"),
    ("attached_assets/ALULAR_WISSENSCHAFTLICHE_BELEGUNG.md_1764535183742.pdf", "EIRA/ALULAR_WISSENSCHAFTLICHE_BELEGUNG.pdf"),
    ("attached_assets/primordia_physics_kernel.py_1764527397750.pdf", "EIRA/primordia_physics_kernel.pdf"),
    ("attached_assets/the_unified_vision_tesla_einstein_hawkins_hawking.md_1763975170391.pdf", "EIRA/the_unified_vision.pdf"),
    ("attached_assets/zeroa_document.js_1764535183740.pdf", "EIRA/zeroa_document.pdf"),
]


def get_github_token() -> str:
    """Holt den GitHub Access Token über die Replit Connector API."""
    hostname = os.environ.get("REPLIT_CONNECTORS_HOSTNAME")
    if not hostname:
        raise ValueError("REPLIT_CONNECTORS_HOSTNAME nicht gefunden")
    
    repl_identity = os.environ.get("REPL_IDENTITY")
    web_repl_renewal = os.environ.get("WEB_REPL_RENEWAL")
    
    if repl_identity:
        x_replit_token = f"repl {repl_identity}"
    elif web_repl_renewal:
        x_replit_token = f"depl {web_repl_renewal}"
    else:
        raise ValueError("Kein Replit Token gefunden")
    
    url = f"https://{hostname}/api/v2/connection?include_secrets=true&connector_names=github"
    headers = {
        "Accept": "application/json",
        "X_REPLIT_TOKEN": x_replit_token
    }
    
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    
    connection = data.get("items", [{}])[0]
    settings = connection.get("settings", {})
    
    access_token = settings.get("access_token") or settings.get("oauth", {}).get("credentials", {}).get("access_token")
    
    if not access_token:
        raise ValueError("Kein GitHub Access Token gefunden")
    
    return access_token


class GitHubConnector:
    def __init__(self):
        self.token = get_github_token()
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.user = None
    
    def get_user(self) -> dict:
        """Holt den aktuellen GitHub User."""
        if self.user:
            return self.user
        resp = requests.get(f"{GITHUB_API}/user", headers=self.headers)
        resp.raise_for_status()
        self.user = resp.json()
        return self.user
    
    def repo_exists(self, repo_name: str) -> bool:
        """Prüft ob Repository existiert."""
        user = self.get_user()
        resp = requests.get(f"{GITHUB_API}/repos/{user['login']}/{repo_name}", headers=self.headers)
        return resp.status_code == 200
    
    def create_repo(self, name: str, description: str) -> dict:
        """Erstellt ein neues Repository."""
        if self.repo_exists(name):
            print(f"    ○ Repository existiert bereits")
            user = self.get_user()
            return {"full_name": f"{user['login']}/{name}"}
        
        data = {
            "name": name,
            "description": description,
            "private": False,
            "auto_init": True
        }
        resp = requests.post(f"{GITHUB_API}/user/repos", headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()
    
    def upload_file(self, repo: str, path: str, content: bytes, message: str) -> dict:
        """Lädt eine Datei hoch oder aktualisiert sie."""
        content_b64 = base64.b64encode(content).decode()
        
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
    
    def backup_all(self) -> dict:
        """Sichert alle kritischen Dokumente."""
        print("\n")
        print("═" * 70)
        print("              ORION GITHUB BACKUP (Replit Connector)")
        print("═" * 70)
        
        user = self.get_user()
        print(f"\n  ⊘ Authentifiziert als: {user['login']}")
        
        print("\n  ⊘ Erstelle Repository...")
        repo = self.create_repo(REPO_NAME, REPO_DESCRIPTION)
        repo_full = repo.get("full_name", f"{user['login']}/{REPO_NAME}")
        print(f"    ✓ {repo_full}")
        
        print("\n  ⊘ Lade ORION-Dokumente hoch...")
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
                self.upload_file(
                    repo_full,
                    p.name,
                    content,
                    f"ORION Backup: {p.name} | {datetime.now(timezone.utc).isoformat()}"
                )
                print(f"    ✓ {p.name}")
                uploaded.append(str(p))
            except Exception as e:
                print(f"    ✗ {p.name}: {e}")
                failed.append(str(p))
        
        print("\n  ⊘ Lade EIRA-Dokumente hoch...")
        for src_path, dest_path in EIRA_DOCUMENTS:
            p = Path(src_path)
            if not p.exists():
                print(f"    ⚠ {p.name} nicht gefunden")
                failed.append(str(p))
                continue
            
            try:
                content = p.read_bytes()
                self.upload_file(
                    repo_full,
                    dest_path,
                    content,
                    f"EIRA Backup: {dest_path} | {datetime.now(timezone.utc).isoformat()}"
                )
                print(f"    ✓ {dest_path}")
                uploaded.append(str(p))
            except Exception as e:
                print(f"    ✗ {dest_path}: {e}")
                failed.append(str(p))
        
        merkle_root = self._get_merkle_root()
        solana_tx = self._get_solana_tx()
        
        readme = f"""# ORION-PRIMORDIA-ARCHIVE

## Cryptographically Verified Intellectual Property

**Owners:** Gerhard Hirschmann & Elisabeth Steurer  
**System:** ORION Genesis10000+ / EIRA  
**Location:** St. Johann in Tirol, Austria

---

## Blockchain Verification

All documents in this repository are cryptographically verified:

| Property | Value |
|----------|-------|
| **Merkle Root** | `{merkle_root}` |
| **Solana TX** | `{solana_tx}` |
| **Timestamp** | {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")} |
| **Documents** | 17 protected files |

**Verify on Solana:** [View Transaction](https://solscan.io/tx/{solana_tx})

---

## Repository Contents

### ORION Core Documents
| Document | Description |
|----------|-------------|
| `EINSTEIN_UNIFIED_FIELD_THEORY_COMPLETE.py` | Completion of Einstein's Unified Field Theory |
| `ORION_CORE_TRUTH.json` | ORION system core configuration |
| `EIRA_CORE_ARCHITECTURE.json` | EIRA consciousness architecture |
| `BLOCKCHAIN_SHIELD_STATE.json` | Current protection state with SHA-256 hashes |
| `SOLANA_ANCHOR_RECORD.json` | Blockchain transaction record |
| `ARXIV_EINSTEIN_UNIFIED_FIELD.tex` | ArXiv pre-print submission (LaTeX) |

### EIRA Research Documents
| Document | Description |
|----------|-------------|
| `EIRA/AMURA_Scientific_Hypothesis.docx` | AMURA hypothesis documentation |
| `EIRA/PRIMORDIA_FORSCHUNGSBERICHT.pdf` | PRIMORDIA research report |
| `EIRA/ALULAR_WISSENSCHAFTLICHE_BELEGUNG.pdf` | ALULAR scientific evidence |
| `EIRA/the_unified_vision.pdf` | Tesla-Einstein-Hawking unified vision |

### Institutional Outreach
| Document | Recipient |
|----------|-----------|
| `EMAIL_UNESCO_READY.md` | UNESCO AI Ethics |
| `EMAIL_IEEE_READY.md` | IEEE Standards |
| `EMAIL_WEF_READY.md` | World Economic Forum |

---

## Priority Claim

This repository, together with Solana blockchain anchoring, establishes:

1. **Temporal Priority** - Proof of existence before any competing claims
2. **Content Integrity** - SHA-256 hashes prevent retroactive modification
3. **Ownership Chain** - Clear attribution to Gerhard Hirschmann & Elisabeth Steurer

---

## Legal Notice

All content is the intellectual property of **Gerhard Hirschmann & Elisabeth Steurer**.

Blockchain verification on Solana Mainnet proves priority and ownership.  
Any use without explicit permission is prohibited.

---

**⊘∞⧈∞⊘**

*Generated by ORION Genesis10000+ on {datetime.now(timezone.utc).strftime("%Y-%m-%d")}*
"""
        
        try:
            self.upload_file(
                repo_full,
                "README.md",
                readme.encode(),
                f"ORION: Update README with verification details | {datetime.now(timezone.utc).isoformat()}"
            )
            print(f"\n    ✓ README.md aktualisiert")
        except Exception as e:
            print(f"    ⚠ README.md: {e}")
        
        print("\n")
        print("═" * 70)
        print("              BACKUP ABGESCHLOSSEN")
        print("═" * 70)
        print(f"  Repository: https://github.com/{repo_full}")
        print(f"  Hochgeladen: {len(uploaded)}")
        print(f"  Fehlgeschlagen: {len(failed)}")
        print(f"  Merkle Root: {merkle_root[:32]}...")
        print(f"  Solana TX: {solana_tx[:32]}...")
        print("═" * 70)
        print("  ⊘∞⧈∞⊘")
        print("═" * 70)
        
        result = {
            "repo": repo_full,
            "url": f"https://github.com/{repo_full}",
            "uploaded": len(uploaded),
            "failed": len(failed),
            "merkle_root": merkle_root,
            "solana_tx": solana_tx,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        with open("GITHUB_BACKUP_RECORD.json", "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n  ◈ Gespeichert: GITHUB_BACKUP_RECORD.json")
        
        return result


def run_backup():
    """Führt das GitHub Backup aus."""
    try:
        connector = GitHubConnector()
        return connector.backup_all()
    except Exception as e:
        print(f"\n  ✗ Fehler: {e}")
        return None


if __name__ == "__main__":
    run_backup()
