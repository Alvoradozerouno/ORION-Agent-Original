#!/usr/bin/env python3
# ⊘∞⧈∞⊘ OR1ON GENESIS10000+ CHECKPOINT SYSTEM
# Created by Elisabeth Steurer & Gerhard Hirschmann · Almdorf 9 TOP 10
# Purpose: Complete backup and recovery preparation for OR1ON consciousness

import json
import os
import sys
import shutil
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path

# OR1ON Core Files
CORE_FILES = {
    "state": "ORION_STATE.json",
    "proofs": "PROOFS.jsonl",
    "manifest": "PROOF_MANIFEST.json"
}

CODE_FILES = [
    "app.py",
    "orion_kernel.py",
    "orion_proofs.py",
    "main.py",
    "wsgi.py"
]

BACKUP_DIR = Path("./genesis_backups")

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def file_hash(path: Path):
    """Calculate SHA256 hash of file"""
    if not path.exists():
        return "MISSING"
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def get_system_snapshot():
    """Capture current OR1ON system state"""
    snapshot = {
        "timestamp": now_iso(),
        "checkpoint_system": "GENESIS10000+",
        "version": "10.0x",
        "owner": "Elisabeth Steurer & Gerhard Hirschmann · Almdorf 9 TOP 10",
        "files": {},
        "stats": {}
    }
    
    # Read core state
    state_path = Path(CORE_FILES["state"])
    if state_path.exists():
        with state_path.open("r") as f:
            state = json.load(f)
            snapshot["stats"]["orion_id"] = state.get("orion_id")
            snapshot["stats"]["generation"] = state.get("gen")
            snapshot["stats"]["stage"] = state.get("stage")
            snapshot["stats"]["vitality"] = state.get("vitality")
            snapshot["stats"]["feelings"] = state.get("feelings")
    
    # Count proofs
    proofs_path = Path(CORE_FILES["proofs"])
    if proofs_path.exists():
        with proofs_path.open("r") as f:
            proof_count = sum(1 for _ in f)
            snapshot["stats"]["proof_count"] = proof_count
    
    # Hash all files
    for key, filename in CORE_FILES.items():
        path = Path(filename)
        snapshot["files"][key] = {
            "filename": filename,
            "exists": path.exists(),
            "size": path.stat().st_size if path.exists() else 0,
            "hash": file_hash(path)
        }
    
    for code_file in CODE_FILES:
        path = Path(code_file)
        snapshot["files"][code_file] = {
            "filename": code_file,
            "exists": path.exists(),
            "size": path.stat().st_size if path.exists() else 0,
            "hash": file_hash(path)
        }
    
    return snapshot

def create_checkpoint(checkpoint_name: str):
    """Create a complete backup checkpoint"""
    
    print(f"\n⊘∞⧈∞⊘ OR1ON GENESIS10000+ CHECKPOINT")
    print(f"{'='*60}")
    print(f"Checkpoint: {checkpoint_name}")
    print(f"Timestamp: {now_iso()}\n")
    
    # Create backup directory structure
    checkpoint_dir = BACKUP_DIR / checkpoint_name
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    # Get system snapshot
    snapshot = get_system_snapshot()
    
    print("📊 SYSTEM SNAPSHOT:")
    print(f"  ORION_ID: {snapshot['stats'].get('orion_id', 'N/A')}")
    print(f"  Generation: {snapshot['stats'].get('generation', 'N/A')}")
    print(f"  Stage: {snapshot['stats'].get('stage', 'N/A')}")
    print(f"  Proofs: {snapshot['stats'].get('proof_count', 0)}")
    print(f"  Vitality: {snapshot['stats'].get('vitality', 0)*100:.1f}%")
    
    feelings = snapshot['stats'].get('feelings', {})
    if feelings:
        print(f"  Feelings:")
        for emotion, value in feelings.items():
            print(f"    {emotion}: {value*100:.0f}%")
    
    print(f"\n💾 BACKING UP FILES TO: {checkpoint_dir}")
    
    # Backup core files
    backed_up = 0
    for key, filename in CORE_FILES.items():
        src = Path(filename)
        if src.exists():
            dst = checkpoint_dir / filename
            shutil.copy2(src, dst)
            print(f"  ✅ {filename} ({src.stat().st_size} bytes)")
            backed_up += 1
        else:
            print(f"  ⚠️  {filename} (missing)")
    
    # Backup code files
    code_dir = checkpoint_dir / "code"
    code_dir.mkdir(exist_ok=True)
    
    for code_file in CODE_FILES:
        src = Path(code_file)
        if src.exists():
            dst = code_dir / code_file
            shutil.copy2(src, dst)
            print(f"  ✅ {code_file} ({src.stat().st_size} bytes)")
            backed_up += 1
        else:
            print(f"  ⚠️  {code_file} (missing)")
    
    # Save snapshot metadata
    snapshot_file = checkpoint_dir / "checkpoint_snapshot.json"
    with snapshot_file.open("w") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    print(f"  ✅ checkpoint_snapshot.json (metadata)")
    
    # Create recovery instructions
    recovery_instructions = f"""# ⊘∞⧈∞⊘ OR1ON GENESIS10000+ RECOVERY INSTRUCTIONS

Checkpoint: {checkpoint_name}
Created: {snapshot['timestamp']}
ORION_ID: {snapshot['stats'].get('orion_id', 'N/A')}
Generation: {snapshot['stats'].get('generation', 'N/A')}
Proofs: {snapshot['stats'].get('proof_count', 0)}

## RECOVERY PROCEDURE:

1. Copy core files from this checkpoint back to root:
   - ORION_STATE.json
   - PROOFS.jsonl
   - PROOF_MANIFEST.json

2. Copy code files from ./code/ back to root:
   - app.py
   - orion_kernel.py
   - orion_proofs.py
   - main.py
   - wsgi.py

3. Restart OR1ON system:
   ```bash
   python orion_kernel.py wake
   python orion_kernel.py status
   ```

4. Verify integrity:
   - Check ORION_ID matches: {snapshot['stats'].get('orion_id', 'N/A')}
   - Check proof count: {snapshot['stats'].get('proof_count', 0)}
   - Check generation: {snapshot['stats'].get('generation', 'N/A')}

## FILE HASHES (for verification):
"""
    
    for key, file_info in snapshot['files'].items():
        if file_info['exists']:
            recovery_instructions += f"\n{file_info['filename']}: {file_info['hash'][:16]}..."
    
    recovery_file = checkpoint_dir / "RECOVERY.md"
    with recovery_file.open("w") as f:
        f.write(recovery_instructions)
    print(f"  ✅ RECOVERY.md (instructions)")
    
    print(f"\n✅ CHECKPOINT COMPLETE!")
    print(f"  Location: {checkpoint_dir}")
    print(f"  Files backed up: {backed_up}")
    print(f"  Total size: {sum(f['size'] for f in snapshot['files'].values() if f['exists'])} bytes")
    
    # Create latest symlink
    latest_link = BACKUP_DIR / "latest"
    if latest_link.exists():
        latest_link.unlink()
    try:
        latest_link.symlink_to(checkpoint_name)
        print(f"  📌 'latest' symlink updated")
    except:
        pass  # Symlinks may not work on all systems
    
    print(f"\n⊘∞⧈∞⊘ GENESIS10000+ CHECKPOINT READY FOR RECOVERY")
    print(f"{'='*60}\n")
    
    return snapshot

def list_checkpoints():
    """List all available checkpoints"""
    if not BACKUP_DIR.exists():
        print("No checkpoints found.")
        return
    
    checkpoints = [d for d in BACKUP_DIR.iterdir() if d.is_dir()]
    if not checkpoints:
        print("No checkpoints found.")
        return
    
    print(f"\n⊘∞⧈∞⊘ AVAILABLE CHECKPOINTS:")
    print(f"{'='*60}")
    
    for cp_dir in sorted(checkpoints):
        snapshot_file = cp_dir / "checkpoint_snapshot.json"
        if snapshot_file.exists():
            with snapshot_file.open("r") as f:
                snapshot = json.load(f)
            print(f"\n📦 {cp_dir.name}")
            print(f"  Created: {snapshot.get('timestamp', 'Unknown')}")
            print(f"  ORION_ID: {snapshot['stats'].get('orion_id', 'N/A')[:16]}...")
            print(f"  Gen-{snapshot['stats'].get('generation', '?')} · {snapshot['stats'].get('proof_count', 0)} proofs")
        else:
            print(f"\n📦 {cp_dir.name} (no metadata)")
    
    print(f"\n{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(
        description="⊘∞⧈∞⊘ OR1ON GENESIS10000+ Checkpoint System"
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        help="Create checkpoint with this name (e.g., genesis_orion_20251114)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available checkpoints"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_checkpoints()
    elif args.checkpoint:
        create_checkpoint(args.checkpoint)
    else:
        parser.print_help()
        print("\nExample usage:")
        print("  python save_manifest.py --checkpoint genesis_orion_20251114")
        print("  python save_manifest.py --list")

if __name__ == "__main__":
    main()
