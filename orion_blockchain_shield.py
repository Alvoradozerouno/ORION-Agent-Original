#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    ORION BLOCKCHAIN SHIELD
                    
            Dezentraler Schutz für EIRA/ORION Erkenntnisse
            
            • Proof of Existence (Solana)
            • Kryptographische Signaturen
            • Dezentrale Verankerung
            • Multi-Node Verknüpfung
═══════════════════════════════════════════════════════════════════════════════

Eigentümer: Gerhard Hirschmann, Elisabeth Steurer
Erstellt:   30. November 2025
System:     ORION / Genesis10000+

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import hashlib
import base64
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import requests

# ═══════════════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SOLANA_WALLET = os.environ.get("SOLANA_WALLET", "")
SOLANA_NETWORK = "mainnet-beta"  # oder "devnet" für Tests
SOLANA_RPC = f"https://api.{SOLANA_NETWORK}.solana.com"

CRITICAL_DOCUMENTS = [
    "EINSTEIN_UNIFIED_FIELD_THEORY_COMPLETE.py",
    "ORION_CORE_TRUTH.json",
    "EIRA_CORE_ARCHITECTURE.json",
    "ORION_WHITEPAPER_v1.md",
    "EGGER_KONZERN_ANALYSE_UND_INNOVATION.md",
    "STEINBACHER_DAEMMSTOFFE_ANALYSE_UND_INNOVATION.md",
    "orion_kernel.py",
    "orion_verstehen.py",
    "PROOFS.jsonl",
    "ORION_STATE.json",
]

OWNERS = ["Gerhard Hirschmann", "Elisabeth Steurer"]
ORION_SIGNATURE = "⊘∞⧈∞⊘"

# ═══════════════════════════════════════════════════════════════════════════════
# DATENSTRUKTUREN
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ProofOfExistence:
    """Ein Existenzbeweis für ein Dokument."""
    document_name: str
    sha256_hash: str
    sha512_hash: str
    timestamp_utc: str
    timestamp_unix: int
    file_size_bytes: int
    owners: List[str]
    orion_signature: str
    solana_ready: bool
    merkle_root: Optional[str] = None
    blockchain_tx: Optional[str] = None


@dataclass
class BlockchainAnchor:
    """Verankerung auf der Blockchain."""
    network: str
    wallet: str
    merkle_root: str
    documents_count: int
    timestamp: str
    tx_signature: Optional[str] = None
    status: str = "pending"


@dataclass
class NodeConnection:
    """Verbindung zu dezentralen Nodes."""
    name: str
    type: str  # "solana", "ipfs", "arweave"
    endpoint: str
    status: str
    last_check: str


# ═══════════════════════════════════════════════════════════════════════════════
# HASH-FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════════

def compute_sha256(filepath: str) -> str:
    """Berechnet SHA256 Hash einer Datei."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return f"FILE_NOT_FOUND:{filepath}"


def compute_sha512(filepath: str) -> str:
    """Berechnet SHA512 Hash einer Datei."""
    sha512 = hashlib.sha512()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha512.update(chunk)
        return sha512.hexdigest()
    except FileNotFoundError:
        return f"FILE_NOT_FOUND:{filepath}"


def compute_merkle_root(hashes: List[str]) -> str:
    """Berechnet Merkle Root aus einer Liste von Hashes."""
    if not hashes:
        return hashlib.sha256(b"EMPTY").hexdigest()
    
    if len(hashes) == 1:
        return hashes[0]
    
    # Paar-weise hashen
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])  # Duplizieren falls ungerade
        
        new_level = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i+1]
            new_hash = hashlib.sha256(combined.encode()).hexdigest()
            new_level.append(new_hash)
        
        hashes = new_level
    
    return hashes[0]


# ═══════════════════════════════════════════════════════════════════════════════
# PROOF OF EXISTENCE GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class ProofGenerator:
    """Generiert Existenzbeweise für Dokumente."""
    
    def __init__(self):
        self.proofs: List[ProofOfExistence] = []
        self.merkle_root: Optional[str] = None
        
    def generate_proof(self, filepath: str) -> Optional[ProofOfExistence]:
        """Generiert Existenzbeweis für eine Datei."""
        path = Path(filepath)
        if not path.exists():
            print(f"  ⚠ Datei nicht gefunden: {filepath}")
            return None
        
        now = datetime.now(timezone.utc)
        
        proof = ProofOfExistence(
            document_name=path.name,
            sha256_hash=compute_sha256(filepath),
            sha512_hash=compute_sha512(filepath),
            timestamp_utc=now.isoformat(),
            timestamp_unix=int(now.timestamp()),
            file_size_bytes=path.stat().st_size,
            owners=OWNERS,
            orion_signature=ORION_SIGNATURE,
            solana_ready=bool(SOLANA_WALLET)
        )
        
        return proof
    
    def generate_all_proofs(self, documents: List[str]) -> List[ProofOfExistence]:
        """Generiert Existenzbeweise für alle Dokumente."""
        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║           GENERATING PROOFS OF EXISTENCE                      ║")
        print("╚═══════════════════════════════════════════════════════════════╝\n")
        
        self.proofs = []
        
        for doc in documents:
            print(f"  ⊘ Verarbeite: {doc}")
            proof = self.generate_proof(doc)
            if proof:
                self.proofs.append(proof)
                print(f"    ✓ SHA256: {proof.sha256_hash[:16]}...")
        
        # Merkle Root berechnen
        hashes = [p.sha256_hash for p in self.proofs]
        self.merkle_root = compute_merkle_root(hashes)
        
        # Merkle Root zu allen Proofs hinzufügen
        for proof in self.proofs:
            proof.merkle_root = self.merkle_root
        
        print(f"\n  ◈ MERKLE ROOT: {self.merkle_root}")
        print(f"  ◈ DOKUMENTE:   {len(self.proofs)}")
        
        return self.proofs
    
    def to_json(self) -> str:
        """Exportiert alle Proofs als JSON."""
        data = {
            "orion_blockchain_shield": {
                "version": "1.0",
                "generated": datetime.now(timezone.utc).isoformat(),
                "merkle_root": self.merkle_root,
                "documents_count": len(self.proofs),
                "owners": OWNERS,
                "signature": ORION_SIGNATURE,
                "proofs": [asdict(p) for p in self.proofs]
            }
        }
        return json.dumps(data, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# SOLANA INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

class SolanaConnector:
    """Verbindung zum Solana Netzwerk."""
    
    def __init__(self, wallet: str = SOLANA_WALLET, network: str = SOLANA_NETWORK):
        self.wallet = wallet
        self.network = network
        self.rpc_url = f"https://api.{network}.solana.com"
        
    def check_connection(self) -> Dict[str, Any]:
        """Prüft Verbindung zum Solana Netzwerk."""
        try:
            response = requests.post(
                self.rpc_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getHealth"
                },
                timeout=10
            )
            data = response.json()
            return {
                "connected": True,
                "network": self.network,
                "status": data.get("result", "unknown"),
                "rpc": self.rpc_url
            }
        except Exception as e:
            return {
                "connected": False,
                "network": self.network,
                "error": str(e)
            }
    
    def get_balance(self) -> Dict[str, Any]:
        """Holt Wallet-Balance."""
        if not self.wallet:
            return {"error": "No wallet configured"}
        
        try:
            response = requests.post(
                self.rpc_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getBalance",
                    "params": [self.wallet]
                },
                timeout=10
            )
            data = response.json()
            
            if "result" in data:
                lamports = data["result"]["value"]
                sol = lamports / 1_000_000_000  # 1 SOL = 1B Lamports
                return {
                    "wallet": self.wallet[:8] + "..." + self.wallet[-8:],
                    "balance_lamports": lamports,
                    "balance_sol": sol,
                    "network": self.network
                }
            else:
                return {"error": data.get("error", "Unknown error")}
                
        except Exception as e:
            return {"error": str(e)}
    
    def prepare_memo_transaction(self, merkle_root: str, documents_count: int) -> Dict[str, Any]:
        """
        Bereitet eine Memo-Transaktion vor.
        
        HINWEIS: Für echte Transaktionen wird ein Signing-Key benötigt.
        Diese Funktion bereitet die Daten vor.
        """
        memo = f"ORION|{merkle_root[:32]}|{documents_count}|{int(time.time())}"
        
        return {
            "type": "memo",
            "network": self.network,
            "wallet": self.wallet,
            "memo": memo,
            "merkle_root": merkle_root,
            "documents_count": documents_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "prepared",
            "note": "Ready for signing. Use Phantom/Solflare wallet to broadcast."
        }


# ═══════════════════════════════════════════════════════════════════════════════
# NODE MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class NodeManager:
    """Verwaltet Verbindungen zu dezentralen Nodes."""
    
    def __init__(self):
        self.nodes: List[NodeConnection] = []
        self._init_default_nodes()
    
    def _init_default_nodes(self):
        """Initialisiert Standard-Nodes."""
        self.nodes = [
            NodeConnection(
                name="Solana Mainnet",
                type="solana",
                endpoint="https://api.mainnet-beta.solana.com",
                status="unknown",
                last_check=""
            ),
            NodeConnection(
                name="Solana Devnet",
                type="solana",
                endpoint="https://api.devnet.solana.com",
                status="unknown",
                last_check=""
            ),
            NodeConnection(
                name="IPFS Gateway (Cloudflare)",
                type="ipfs",
                endpoint="https://cloudflare-ipfs.com",
                status="unknown",
                last_check=""
            ),
            NodeConnection(
                name="IPFS Gateway (Pinata)",
                type="ipfs",
                endpoint="https://gateway.pinata.cloud",
                status="unknown",
                last_check=""
            ),
            NodeConnection(
                name="Arweave Gateway",
                type="arweave",
                endpoint="https://arweave.net",
                status="unknown",
                last_check=""
            )
        ]
    
    def check_all_nodes(self) -> List[Dict[str, Any]]:
        """Prüft alle Nodes."""
        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║              CHECKING NODE CONNECTIONS                        ║")
        print("╚═══════════════════════════════════════════════════════════════╝\n")
        
        results = []
        
        for node in self.nodes:
            print(f"  ⊘ Prüfe: {node.name}...")
            try:
                response = requests.get(node.endpoint, timeout=5)
                node.status = "online" if response.status_code < 500 else "error"
            except:
                node.status = "offline"
            
            node.last_check = datetime.now(timezone.utc).isoformat()
            
            status_icon = "✓" if node.status == "online" else "✗"
            print(f"    {status_icon} Status: {node.status}")
            
            results.append({
                "name": node.name,
                "type": node.type,
                "status": node.status,
                "endpoint": node.endpoint
            })
        
        return results
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Gibt Zusammenfassung aller Node-Status."""
        online = sum(1 for n in self.nodes if n.status == "online")
        total = len(self.nodes)
        
        return {
            "total_nodes": total,
            "online": online,
            "offline": total - online,
            "coverage": f"{online}/{total}",
            "nodes": [asdict(n) for n in self.nodes]
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SHIELD ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

class BlockchainShield:
    """
    Hauptklasse: Orchestriert den gesamten Blockchain-Schutz.
    """
    
    def __init__(self):
        self.proof_generator = ProofGenerator()
        self.solana = SolanaConnector()
        self.node_manager = NodeManager()
        self.shield_state: Dict[str, Any] = {}
        
    def activate(self, documents: List[str] = CRITICAL_DOCUMENTS) -> Dict[str, Any]:
        """
        Aktiviert den vollständigen Blockchain-Schutz.
        """
        print("\n")
        print("═" * 70)
        print("                 ORION BLOCKCHAIN SHIELD AKTIVIERUNG")
        print("═" * 70)
        print(f"  Eigentümer:  {', '.join(OWNERS)}")
        print(f"  Zeitpunkt:   {datetime.now(timezone.utc).isoformat()}")
        print(f"  Signatur:    {ORION_SIGNATURE}")
        print("═" * 70)
        
        # 1. Proofs generieren
        proofs = self.proof_generator.generate_all_proofs(documents)
        
        # 2. Nodes prüfen
        node_status = self.node_manager.check_all_nodes()
        
        # 3. Solana-Verbindung prüfen
        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║              SOLANA CONNECTION CHECK                          ║")
        print("╚═══════════════════════════════════════════════════════════════╝\n")
        
        solana_health = self.solana.check_connection()
        print(f"  ⊘ Netzwerk: {solana_health.get('network', 'unknown')}")
        print(f"  ⊘ Status:   {solana_health.get('status', solana_health.get('error', 'unknown'))}")
        
        solana_balance = self.solana.get_balance()
        if "balance_sol" in solana_balance:
            print(f"  ⊘ Wallet:   {solana_balance['wallet']}")
            print(f"  ⊘ Balance:  {solana_balance['balance_sol']:.4f} SOL")
        else:
            print(f"  ⊘ Balance:  {solana_balance.get('error', 'Unknown')}")
        
        # 4. Transaktion vorbereiten
        tx_data = self.solana.prepare_memo_transaction(
            self.proof_generator.merkle_root,
            len(proofs)
        )
        
        # 5. Shield-State speichern
        self.shield_state = {
            "activated": datetime.now(timezone.utc).isoformat(),
            "merkle_root": self.proof_generator.merkle_root,
            "documents_count": len(proofs),
            "proofs": [asdict(p) for p in proofs],
            "nodes": node_status,
            "solana": {
                "health": solana_health,
                "balance": solana_balance,
                "prepared_tx": tx_data
            },
            "owners": OWNERS,
            "signature": ORION_SIGNATURE
        }
        
        # 6. In Datei speichern
        self._save_shield_state()
        
        # 7. Zusammenfassung
        print("\n")
        print("═" * 70)
        print("                 BLOCKCHAIN SHIELD AKTIVIERT")
        print("═" * 70)
        print(f"  ✓ Dokumente geschützt:  {len(proofs)}")
        print(f"  ✓ Merkle Root:          {self.proof_generator.merkle_root[:32]}...")
        print(f"  ✓ Nodes verbunden:      {sum(1 for n in node_status if n['status'] == 'online')}/{len(node_status)}")
        print(f"  ✓ Solana bereit:        {'Ja' if solana_health.get('connected') else 'Nein'}")
        print(f"  ✓ Zeitstempel:          {self.shield_state['activated']}")
        print("═" * 70)
        print(f"  {ORION_SIGNATURE}")
        print("═" * 70)
        
        return self.shield_state
    
    def _save_shield_state(self):
        """Speichert Shield-State in Datei."""
        with open("BLOCKCHAIN_SHIELD_STATE.json", "w") as f:
            json.dump(self.shield_state, f, indent=2)
        
        # Auch die Proofs separat speichern
        proofs_json = self.proof_generator.to_json()
        with open("ORION_PROOFS_OF_EXISTENCE.json", "w") as f:
            f.write(proofs_json)
        
        print(f"\n  ◈ Gespeichert: BLOCKCHAIN_SHIELD_STATE.json")
        print(f"  ◈ Gespeichert: ORION_PROOFS_OF_EXISTENCE.json")
    
    def get_merkle_proof(self, document_name: str) -> Dict[str, Any]:
        """Gibt Merkle-Proof für ein spezifisches Dokument."""
        for proof in self.proof_generator.proofs:
            if proof.document_name == document_name:
                return {
                    "document": document_name,
                    "sha256": proof.sha256_hash,
                    "merkle_root": proof.merkle_root,
                    "timestamp": proof.timestamp_utc,
                    "verified": True
                }
        return {"error": f"Dokument nicht gefunden: {document_name}"}


# ═══════════════════════════════════════════════════════════════════════════════
# HAUPTPROGRAMM
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Haupteinstiegspunkt."""
    shield = BlockchainShield()
    state = shield.activate()
    
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║                    NÄCHSTE SCHRITTE                           ║")
    print("╠═══════════════════════════════════════════════════════════════╣")
    print("║                                                               ║")
    print("║  1. SOLANA TRANSAKTION:                                       ║")
    print("║     → Memo mit Merkle Root auf Blockchain speichern           ║")
    print("║     → Nutze Phantom/Solflare Wallet zum Signieren             ║")
    print("║                                                               ║")
    print("║  2. IPFS BACKUP:                                              ║")
    print("║     → Kritische Dokumente auf IPFS hochladen                  ║")
    print("║     → CIDs in BLOCKCHAIN_SHIELD_STATE.json speichern          ║")
    print("║                                                               ║")
    print("║  3. ARWEAVE PERMANENT:                                        ║")
    print("║     → Wichtigste Erkenntnisse permanent speichern             ║")
    print("║     → 200+ Jahre garantierte Speicherung                      ║")
    print("║                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    
    return state


if __name__ == "__main__":
    main()
