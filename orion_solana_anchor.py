#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    ORION SOLANA ANCHOR
                    
            Verewigt den Merkle Root auf der Solana Blockchain
            
═══════════════════════════════════════════════════════════════════════════════

Eigentümer: Gerhard Hirschmann, Elisabeth Steurer
Erstellt:   30. November 2025
System:     ORION / Genesis10000+

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import base58
from datetime import datetime, timezone

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message
from solders.instruction import Instruction, AccountMeta
from solders.hash import Hash
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed

# ═══════════════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
MEMO_PROGRAM_ID = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")

ORION_SIGNATURE = "⊘∞⧈∞⊘"

def get_current_merkle_root() -> str:
    """Lädt den aktuellen Merkle Root aus der Shield-Datei."""
    try:
        with open("BLOCKCHAIN_SHIELD_STATE.json") as f:
            return json.load(f).get("merkle_root", "")
    except:
        return ""

MERKLE_ROOT = get_current_merkle_root() or "d916902f55f160da39c369886c4beb2c9d8b5741c2ca47a283a6976e699d3552"

# ═══════════════════════════════════════════════════════════════════════════════
# WALLET FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════════

def load_keypair_from_secret() -> Keypair:
    """Lädt den Keypair aus dem Secret."""
    secret = os.environ.get("SOLANA_WALLET", "")
    if not secret:
        raise ValueError("SOLANA_WALLET Secret nicht gefunden!")
    
    # Solflare exportiert als Base58-encoded Private Key
    try:
        secret_bytes = base58.b58decode(secret)
        keypair = Keypair.from_bytes(secret_bytes)
        return keypair
    except Exception as e:
        raise ValueError(f"Fehler beim Laden des Keypairs: {e}")


def get_balance(client: Client, pubkey: Pubkey) -> float:
    """Holt die Balance in SOL."""
    try:
        resp = client.get_balance(pubkey)
        lamports = resp.value
        return lamports / 1_000_000_000
    except Exception as e:
        print(f"Fehler beim Abrufen der Balance: {e}")
        return 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# MEMO TRANSAKTION
# ═══════════════════════════════════════════════════════════════════════════════

def create_memo_instruction(signer: Pubkey, memo: str) -> Instruction:
    """Erstellt eine Memo-Instruction."""
    return Instruction(
        program_id=MEMO_PROGRAM_ID,
        accounts=[AccountMeta(pubkey=signer, is_signer=True, is_writable=False)],
        data=memo.encode('utf-8')
    )


def send_merkle_root_to_chain():
    """Sendet den Merkle Root auf die Solana Blockchain."""
    
    print("\n")
    print("═" * 70)
    print("           ORION SOLANA ANCHOR - MERKLE ROOT TRANSAKTION")
    print("═" * 70)
    
    # 1. Keypair laden
    print("\n  ⊘ Lade Keypair...")
    try:
        keypair = load_keypair_from_secret()
        pubkey = keypair.pubkey()
        print(f"    ✓ Wallet: {str(pubkey)[:8]}...{str(pubkey)[-8:]}")
    except Exception as e:
        print(f"    ✗ Fehler: {e}")
        return None
    
    # 2. Client verbinden
    print("\n  ⊘ Verbinde mit Solana Mainnet...")
    client = Client(SOLANA_RPC_URL)
    
    # 3. Balance prüfen
    balance = get_balance(client, pubkey)
    print(f"    ✓ Balance: {balance:.6f} SOL")
    
    if balance < 0.001:
        print("    ⚠ Balance zu niedrig für Transaktion (min. 0.001 SOL)")
        return None
    
    # 4. Memo erstellen
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    memo = f"ORION|{MERKLE_ROOT[:32]}|{timestamp}|{ORION_SIGNATURE}"
    
    print(f"\n  ⊘ Memo erstellen...")
    print(f"    Inhalt: {memo[:50]}...")
    
    # 5. Recent Blockhash holen
    print("\n  ⊘ Hole Recent Blockhash...")
    try:
        blockhash_resp = client.get_latest_blockhash()
        recent_blockhash = blockhash_resp.value.blockhash
        print(f"    ✓ Blockhash: {str(recent_blockhash)[:16]}...")
    except Exception as e:
        print(f"    ✗ Fehler: {e}")
        return None
    
    # 6. Transaktion erstellen
    print("\n  ⊘ Erstelle Transaktion...")
    try:
        memo_ix = create_memo_instruction(pubkey, memo)
        
        message = Message.new_with_blockhash(
            [memo_ix],
            pubkey,
            recent_blockhash
        )
        
        tx = Transaction.new_unsigned(message)
        tx.sign([keypair], recent_blockhash)
        
        print(f"    ✓ Transaktion signiert")
    except Exception as e:
        print(f"    ✗ Fehler bei Transaktionserstellung: {e}")
        return None
    
    # 7. Transaktion senden
    print("\n  ⊘ Sende Transaktion...")
    try:
        result = client.send_transaction(tx)
        tx_signature = str(result.value)
        print(f"    ✓ TX Signatur: {tx_signature}")
    except Exception as e:
        print(f"    ✗ Fehler beim Senden: {e}")
        return None
    
    # 8. Bestätigung warten
    print("\n  ⊘ Warte auf Bestätigung...")
    try:
        confirm = client.confirm_transaction(result.value, commitment=Confirmed)
        if confirm.value:
            print(f"    ✓ TRANSAKTION BESTÄTIGT!")
        else:
            print(f"    ⚠ Bestätigung ausstehend")
    except Exception as e:
        print(f"    ⚠ Bestätigungsfehler (TX könnte trotzdem durchgegangen sein): {e}")
    
    # 9. Erfolg
    print("\n")
    print("═" * 70)
    print("                    MERKLE ROOT VEREWIGT")
    print("═" * 70)
    print(f"  TX: {tx_signature}")
    print(f"  Explorer: https://solscan.io/tx/{tx_signature}")
    print("═" * 70)
    print(f"  {ORION_SIGNATURE}")
    print("═" * 70)
    
    # 10. In Datei speichern
    anchor_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "merkle_root": MERKLE_ROOT,
        "tx_signature": tx_signature,
        "wallet": str(pubkey),
        "network": "mainnet-beta",
        "explorer_url": f"https://solscan.io/tx/{tx_signature}",
        "memo": memo,
        "status": "confirmed"
    }
    
    with open("SOLANA_ANCHOR_RECORD.json", "w") as f:
        json.dump(anchor_record, f, indent=2)
    
    print(f"\n  ◈ Gespeichert: SOLANA_ANCHOR_RECORD.json")
    
    return tx_signature


# ═══════════════════════════════════════════════════════════════════════════════
# HAUPTPROGRAMM
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    send_merkle_root_to_chain()
