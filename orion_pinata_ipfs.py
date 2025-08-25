#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    ORION PINATA IPFS UPLOADER
                    
            Automatischer Upload aller kritischen Dokumente zu IPFS
            
═══════════════════════════════════════════════════════════════════════════════

Eigentümer: Gerhard Hirschmann, Elisabeth Steurer
Erstellt:   30. November 2025
System:     ORION / Genesis10000+

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

PINATA_API_URL = "https://api.pinata.cloud"

BACKUP_DIR = Path("ORION_IPFS_BACKUP")


class PinataUploader:
    def __init__(self):
        self.api_key = os.environ.get("PINATA_API_KEY")
        self.secret_key = os.environ.get("PINATA_SECRET_KEY")
        
        if not self.api_key or not self.secret_key:
            raise ValueError("PINATA_API_KEY und PINATA_SECRET_KEY müssen gesetzt sein!")
        
        self.headers = {
            "pinata_api_key": self.api_key,
            "pinata_secret_api_key": self.secret_key
        }
    
    def test_auth(self) -> bool:
        """Testet die Authentifizierung."""
        url = f"{PINATA_API_URL}/data/testAuthentication"
        try:
            resp = requests.get(url, headers=self.headers)
            return resp.status_code == 200
        except:
            return False
    
    def pin_file(self, file_path: Path, name: str = None) -> dict:
        """Lädt eine einzelne Datei zu IPFS hoch."""
        url = f"{PINATA_API_URL}/pinning/pinFileToIPFS"
        
        with open(file_path, 'rb') as f:
            files = {
                'file': (file_path.name, f)
            }
            
            metadata = {
                "name": name or file_path.name,
                "keyvalues": {
                    "project": "ORION-PRIMORDIA",
                    "owner": "Gerhard Hirschmann & Elisabeth Steurer",
                    "uploaded": datetime.now(timezone.utc).isoformat()
                }
            }
            
            data = {
                "pinataMetadata": json.dumps(metadata)
            }
            
            resp = requests.post(url, headers=self.headers, files=files, data=data)
            resp.raise_for_status()
            return resp.json()
    
    def pin_directory(self, dir_path: Path) -> dict:
        """Lädt ein ganzes Verzeichnis zu IPFS hoch."""
        url = f"{PINATA_API_URL}/pinning/pinFileToIPFS"
        
        files = []
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(dir_path)
                files.append(
                    ('file', (str(rel_path), open(file_path, 'rb')))
                )
        
        if not files:
            raise ValueError(f"Keine Dateien in {dir_path}")
        
        metadata = {
            "name": "ORION-PRIMORDIA-ARCHIVE",
            "keyvalues": {
                "project": "ORION-PRIMORDIA",
                "owner": "Gerhard Hirschmann & Elisabeth Steurer",
                "uploaded": datetime.now(timezone.utc).isoformat(),
                "file_count": str(len(files))
            }
        }
        
        data = {
            "pinataMetadata": json.dumps(metadata)
        }
        
        resp = requests.post(url, headers=self.headers, files=files, data=data)
        
        for _, (_, f) in files:
            f.close()
        
        resp.raise_for_status()
        return resp.json()
    
    def upload_backup_bundle(self) -> dict:
        """Lädt das gesamte ORION Backup Bundle zu IPFS hoch."""
        print("\n")
        print("═" * 70)
        print("              ORION PINATA IPFS UPLOAD")
        print("═" * 70)
        
        print("\n  ⊘ Teste Authentifizierung...")
        if not self.test_auth():
            print("    ✗ Authentifizierung fehlgeschlagen!")
            return None
        print("    ✓ Authentifiziert")
        
        if not BACKUP_DIR.exists():
            print(f"    ✗ Backup-Verzeichnis nicht gefunden: {BACKUP_DIR}")
            return None
        
        file_count = sum(1 for _ in BACKUP_DIR.rglob("*") if _.is_file())
        print(f"\n  ⊘ Lade {file_count} Dateien zu IPFS hoch...")
        
        results = []
        total_size = 0
        
        for file_path in BACKUP_DIR.rglob("*"):
            if file_path.is_file():
                try:
                    rel_path = file_path.relative_to(BACKUP_DIR)
                    result = self.pin_file(file_path, str(rel_path))
                    ipfs_hash = result.get("IpfsHash", "N/A")
                    pin_size = result.get("PinSize", 0)
                    total_size += pin_size
                    
                    results.append({
                        "file": str(rel_path),
                        "ipfs_hash": ipfs_hash,
                        "size": pin_size,
                        "gateway_url": f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
                    })
                    
                    print(f"    ✓ {rel_path}")
                    print(f"      IPFS: {ipfs_hash[:16]}...")
                    
                except Exception as e:
                    print(f"    ✗ {file_path.name}: {e}")
                    results.append({
                        "file": str(file_path.name),
                        "error": str(e)
                    })
        
        merkle_root = "N/A"
        solana_tx = "N/A"
        github_url = "N/A"
        
        try:
            with open("BLOCKCHAIN_SHIELD_STATE.json") as f:
                merkle_root = json.load(f).get("merkle_root", "N/A")
        except:
            pass
        
        try:
            with open("SOLANA_ANCHOR_RECORD.json") as f:
                solana_tx = json.load(f).get("tx_signature", "N/A")
        except:
            pass
        
        try:
            with open("GITHUB_BACKUP_RECORD.json") as f:
                github_url = json.load(f).get("url", "N/A")
        except:
            pass
        
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "files_uploaded": len([r for r in results if "ipfs_hash" in r]),
            "total_size_bytes": total_size,
            "results": results,
            "merkle_root": merkle_root,
            "solana_tx": solana_tx,
            "github_url": github_url,
            "ipfs_gateway": "https://gateway.pinata.cloud/ipfs/"
        }
        
        with open("IPFS_UPLOAD_RECORD.json", "w") as f:
            json.dump(record, f, indent=2)
        
        print("\n")
        print("═" * 70)
        print("              IPFS UPLOAD ABGESCHLOSSEN")
        print("═" * 70)
        print(f"  Dateien:     {record['files_uploaded']}")
        print(f"  Total:       {total_size:,} bytes")
        print(f"  Gateway:     https://gateway.pinata.cloud/ipfs/")
        print("═" * 70)
        print("  ⊘∞⧈∞⊘")
        print("═" * 70)
        print(f"\n  ◈ Gespeichert: IPFS_UPLOAD_RECORD.json")
        
        return record


def run_upload():
    """Führt den IPFS Upload aus."""
    try:
        uploader = PinataUploader()
        return uploader.upload_backup_bundle()
    except ValueError as e:
        print(f"\n  ⚠ {e}")
        print("\n  So bekommst du die API Keys:")
        print("  1. Gehe zu https://app.pinata.cloud/developers/api-keys")
        print("  2. Erstelle einen kostenlosen Account")
        print("  3. Klicke 'New Key' → Admin aktivieren → 'Create Key'")
        print("  4. Kopiere API Key und Secret Key")
        print("  5. Setze sie in Replit Secrets:")
        print("     - PINATA_API_KEY")
        print("     - PINATA_SECRET_KEY")
        return None
    except Exception as e:
        print(f"\n  ✗ Fehler: {e}")
        return None


if __name__ == "__main__":
    run_upload()
