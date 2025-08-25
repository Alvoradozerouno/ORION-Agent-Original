#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    ORION IPFS BACKUP SYSTEM
                    
            Dezentrale Speicherung kritischer Dokumente
            
═══════════════════════════════════════════════════════════════════════════════

Eigentümer: Gerhard Hirschmann, Elisabeth Steurer
Erstellt:   30. November 2025
System:     ORION / Genesis10000+

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# KRITISCHE DOKUMENTE
# ═══════════════════════════════════════════════════════════════════════════════

CRITICAL_DOCUMENTS = [
    "EINSTEIN_UNIFIED_FIELD_THEORY_COMPLETE.py",
    "ORION_CORE_TRUTH.json",
    "EIRA_CORE_ARCHITECTURE.json",
    "ORION_WHITEPAPER.md",
    "BLOCKCHAIN_SHIELD_STATE.json",
    "SOLANA_ANCHOR_RECORD.json",
    "EGGER_KONZERN_ANALYSE_UND_INNOVATION.md",
    "STEINBACHER_DAEMMSTOFFE_ANALYSE_UND_INNOVATION.md",
    "ARXIV_EINSTEIN_UNIFIED_FIELD.tex",
    "EXTENDED_CONTACTS_LIST.json",
    "EMAIL_UNESCO_READY.md",
    "EMAIL_IEEE_READY.md",
    "EMAIL_WEF_READY.md"
]

# ═══════════════════════════════════════════════════════════════════════════════
# IPFS BACKUP VORBEREITUNG
# ═══════════════════════════════════════════════════════════════════════════════

def prepare_ipfs_bundle():
    """Bereitet alle Dokumente für IPFS-Upload vor."""
    
    print("\n")
    print("═" * 70)
    print("              ORION IPFS BACKUP - VORBEREITUNG")
    print("═" * 70)
    
    # Erstelle Backup-Verzeichnis
    backup_dir = Path("ORION_IPFS_BACKUP")
    backup_dir.mkdir(exist_ok=True)
    
    manifest = {
        "orion_ipfs_backup": True,
        "version": "1.0",
        "created": datetime.now(timezone.utc).isoformat(),
        "owner": "Gerhard Hirschmann & Elisabeth Steurer",
        "system": "ORION Genesis10000+",
        "merkle_root": "fbae06202804b9c8abf90b8c25385c4b6b4265d4b4e696c7841fe83a08c862ce",
        "solana_tx": "4kpyxVXcsWKqExKNzuQUD1ZakdRk7yE6i2pNz2Y5tERYkZtz8bXBDqmLo3F2aY85uQSYGkAA9YgyFiAWqtYDf9Eg",
        "documents": [],
        "signature": "⊘∞⧈∞⊘"
    }
    
    print(f"\n  ⊘ Backup-Verzeichnis: {backup_dir}")
    print(f"\n  ⊘ Kopiere Dokumente...")
    
    copied = 0
    for doc in CRITICAL_DOCUMENTS:
        src_path = Path(doc)
        if src_path.exists():
            # Kopiere Datei
            content = src_path.read_bytes()
            dest_path = backup_dir / doc
            dest_path.write_bytes(content)
            
            # Hash berechnen
            sha256 = hashlib.sha256(content).hexdigest()
            
            manifest["documents"].append({
                "name": doc,
                "sha256": sha256,
                "size": len(content)
            })
            
            print(f"    ✓ {doc}")
            copied += 1
        else:
            print(f"    ⚠ {doc} nicht gefunden")
    
    # Speichere Manifest
    manifest_path = backup_dir / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\n    ✓ MANIFEST.json erstellt")
    
    # Erstelle README
    readme_content = f"""# ORION IPFS BACKUP

## Eigentümer
Gerhard Hirschmann & Elisabeth Steurer
St. Johann in Tirol, Austria

## System
ORION Genesis10000+
ID: 56b3b326-4bf9-559d-9887-02141f699a43

## Blockchain Verification
- **Merkle Root:** {manifest["merkle_root"]}
- **Solana TX:** {manifest["solana_tx"]}
- **Verify:** https://solscan.io/tx/{manifest["solana_tx"]}

## Enthaltene Dokumente
{chr(10).join([f"- {d['name']} (SHA256: {d['sha256'][:16]}...)" for d in manifest["documents"]])}

## Timestamp
{manifest["created"]}

## Signatur
⊘∞⧈∞⊘
"""
    
    readme_path = backup_dir / "README.md"
    readme_path.write_text(readme_content)
    print(f"    ✓ README.md erstellt")
    
    print("\n")
    print("═" * 70)
    print("                    BACKUP BEREIT")
    print("═" * 70)
    print(f"  Verzeichnis: {backup_dir.absolute()}")
    print(f"  Dokumente:   {copied}")
    print("═" * 70)
    print("\n  IPFS UPLOAD OPTIONEN:")
    print("")
    print("  1. PINATA (empfohlen - kostenlos):")
    print("     → https://app.pinata.cloud")
    print("     → Account erstellen")
    print("     → Ordner 'ORION_IPFS_BACKUP' hochladen")
    print("")
    print("  2. NFT.STORAGE (kostenlos, permanent):")
    print("     → https://nft.storage")
    print("     → Ordner hochladen")
    print("")
    print("  3. WEB3.STORAGE (kostenlos):")
    print("     → https://web3.storage")
    print("     → Account + Upload")
    print("")
    print("═" * 70)
    print(f"  {manifest['signature']}")
    print("═" * 70)
    
    return backup_dir, manifest


def generate_ipfs_instructions():
    """Generiert detaillierte IPFS Upload-Anweisungen."""
    
    instructions = """
═══════════════════════════════════════════════════════════════════════════════
                    IPFS UPLOAD ANLEITUNG
═══════════════════════════════════════════════════════════════════════════════

SCHRITT 1: PINATA ACCOUNT
─────────────────────────
1. Gehe zu: https://app.pinata.cloud
2. Klicke auf "Sign Up"
3. Erstelle kostenlosen Account

SCHRITT 2: UPLOAD
─────────────────
1. Im Pinata Dashboard: "Upload" → "Folder"
2. Wähle den Ordner: ORION_IPFS_BACKUP
3. Klicke "Upload"

SCHRITT 3: CID SICHERN
──────────────────────
Nach dem Upload erhältst du einen CID (Content Identifier):
→ z.B. QmXoYpZuVkJzGZh...

Diese CID ist die PERMANENTE Adresse deiner Dokumente auf IPFS.

Zugriff: https://gateway.pinata.cloud/ipfs/[DEIN_CID]

WICHTIG:
────────
- Der CID ist wie ein Fingerabdruck
- Wenn EINE Datei sich ändert, ändert sich der CID
- Speichere den CID sicher ab

═══════════════════════════════════════════════════════════════════════════════
                              ⊘∞⧈∞⊘
═══════════════════════════════════════════════════════════════════════════════
"""
    
    print(instructions)
    
    # Speichere Anleitung
    with open("IPFS_UPLOAD_ANLEITUNG.md", "w") as f:
        f.write(instructions)
    
    return instructions


# ═══════════════════════════════════════════════════════════════════════════════
# HAUPTPROGRAMM
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    backup_dir, manifest = prepare_ipfs_bundle()
    generate_ipfs_instructions()
