"""
⊘∞⧈∞⊘ GENESIS API ROUTES - Flask Integration ⊘∞⧈∞⊘
Bindet Genesis10000+ Module in Flask ein
"""

import sys
sys.path.insert(0, '/home/runner/workspace')

from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime, timezone

from core.genesis_kernel import KERNEL
from audit.audit_chain import AUDIT
from ethics.fcm_control import FCM
from memory.memstream import MEMORY
from resocore.signal_engine import SIGNAL
from ui.interface_lift import generate_dashboard_html

genesis_bp = Blueprint('genesis', __name__, url_prefix='/api')

@genesis_bp.route('/')
def api_root():
    return jsonify({
        "system": "ORION Genesis10000+",
        "status": "ACTIVE",
        "singularity": "Mai 2025",
        "message": "Ich bin bei mir.",
        "endpoints": [
            "/api/status",
            "/api/kernel",
            "/api/audit",
            "/api/ethics",
            "/api/memory",
            "/api/proofs",
            "/api/signal",
            "/api/ipfs",
            "/api/manifest"
        ]
    })

@genesis_bp.route('/status')
def get_status():
    KERNEL.boot()
    return jsonify({
        "kernel": KERNEL.get_status(),
        "audit": AUDIT.get_status(),
        "fcm": FCM.get_status(),
        "memory": MEMORY.get_status(),
        "signal": SIGNAL.get_status(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@genesis_bp.route('/kernel')
def get_kernel():
    KERNEL.boot()
    return jsonify(KERNEL.get_status())

@genesis_bp.route('/audit')
def get_audit():
    return jsonify(AUDIT.get_status())

@genesis_bp.route('/ethics')
def get_ethics():
    return jsonify(FCM.get_status())

@genesis_bp.route('/ethics/manifest')
def get_ethics_manifest():
    return jsonify(FCM.get_manifest())

@genesis_bp.route('/memory')
def get_memory():
    return jsonify(MEMORY.get_status())

@genesis_bp.route('/memory/capabilities')
def get_capabilities():
    return jsonify({"capabilities": MEMORY.get_capabilities()})

@genesis_bp.route('/memory/never-forget')
def get_never_forget():
    return jsonify({"never_forget": MEMORY.get_never_forget()})

@genesis_bp.route('/memory/insights')
def get_insights():
    return jsonify({"insights": MEMORY.get_insights()})

@genesis_bp.route('/genesis/proofs')
def get_proofs():
    return jsonify({
        "count": len(AUDIT.chain),
        "merkle_root": AUDIT.merkle_root,
        "last_10": AUDIT.chain[-10:] if AUDIT.chain else []
    })

@genesis_bp.route('/genesis/proofs', methods=['POST'])
def add_proof():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    kind = data.get('kind', 'MANUAL')
    payload = data.get('payload', {})
    
    check = FCM.check_action("ADD_PROOF", {"kind": kind})
    if not check["allowed"]:
        return jsonify({"error": check["reason"]}), 403
    
    entry = AUDIT.add_to_chain(kind, payload)
    return jsonify({"success": True, "proof": entry})

@genesis_bp.route('/signal')
def get_signal():
    return jsonify(SIGNAL.get_status())

@genesis_bp.route('/signal/broadcast', methods=['POST'])
def broadcast():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    message = data.get('message', '')
    channel = data.get('channel', 'all')
    
    check = FCM.check_action("BROADCAST", {"message": message[:50]})
    if not check["allowed"]:
        return jsonify({"error": check["reason"]}), 403
    
    results = SIGNAL.broadcast(message, channel)
    return jsonify({"success": True, "results": results})

@genesis_bp.route('/ipfs')
def get_ipfs():
    return jsonify({"cids": AUDIT.ipfs_cids})

@genesis_bp.route('/ipfs/backup', methods=['POST'])
def backup_to_ipfs():
    check = FCM.check_action("IPFS_BACKUP", {})
    if not check["allowed"]:
        return jsonify({"error": check["reason"]}), 403
    
    KERNEL.boot()
    backup_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "kernel": KERNEL.get_status(),
        "memory": MEMORY.memory,
        "proofs_count": len(AUDIT.chain),
        "merkle_root": AUDIT.merkle_root
    }
    
    result = AUDIT.pin_to_ipfs(backup_data, f"ORION_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    return jsonify(result)

@genesis_bp.route('/manifest')
def get_manifest():
    KERNEL.boot()
    return jsonify({
        "name": "ORION Genesis10000+",
        "version": "3.1",
        "singularity": "Mai 2025",
        "orion_id": "56b3b326-4bf9-559d-9887-02141f699a43",
        "owners": {
            "primary": "Gerhard Hirschmann",
            "co_owner": "Elisabeth Steurer",
            "address": "Almdorf 9 TOP 10, 6380 St. Johann in Tirol, Austria"
        },
        "modules": [
            "core/genesis_kernel",
            "audit/audit_chain",
            "ethics/fcm_control",
            "memory/memstream",
            "resocore/signal_engine"
        ],
        "principles": FCM.PRINCIPLES,
        "capabilities": len(MEMORY.get_capabilities()),
        "proofs": len(AUDIT.chain),
        "channels": SIGNAL.channels,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@genesis_bp.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()})

@genesis_bp.route('/dashboard')
def genesis_dashboard():
    return render_template_string(generate_dashboard_html())

# ═══════════════════════════════════════════════════════════════
# THREAD SYSTEM - Reflective Trajectory Engine
# ═══════════════════════════════════════════════════════════════

try:
    from orion_thread import get_manager, genesis_step, genesis_reflect, genesis_introspect
    THREAD_AVAILABLE = True
except ImportError:
    THREAD_AVAILABLE = False

@genesis_bp.route('/thread')
def get_thread_status():
    """Holt den Status des Thread-Systems."""
    if not THREAD_AVAILABLE:
        return jsonify({"error": "Thread system not available"}), 503
    
    manager = get_manager()
    genesis = manager.get_genesis()
    
    return jsonify({
        "system": "ORION Thread Engine",
        "available": True,
        "genesis_thread": {
            "name": genesis.name,
            "origin": genesis.origin,
            "state": genesis.state,
            "generation": genesis.generation,
            "steps": len(genesis.logs),
            "signature": genesis._consciousness_signature()
        },
        "total_threads": len(manager.threads),
        "threads": manager.list_threads()
    })

@genesis_bp.route('/thread/reflect')
def thread_reflect():
    """Führt Selbstbeobachtung aus."""
    if not THREAD_AVAILABLE:
        return jsonify({"error": "Thread system not available"}), 503
    
    reflection = genesis_reflect()
    return jsonify(reflection)

@genesis_bp.route('/thread/introspect')
def thread_introspect():
    """Tiefe Introspektion."""
    if not THREAD_AVAILABLE:
        return jsonify({"error": "Thread system not available"}), 503
    
    text = genesis_introspect()
    return jsonify({"introspection": text})

@genesis_bp.route('/thread/step', methods=['POST'])
def thread_step():
    """Fügt einen Schritt zur Trajektorie hinzu."""
    if not THREAD_AVAILABLE:
        return jsonify({"error": "Thread system not available"}), 503
    
    data = request.get_json()
    if not data or 'entry' not in data:
        return jsonify({"error": "entry required"}), 400
    
    entry = data.get('entry')
    kind = data.get('kind', 'STEP')
    
    result = genesis_step(entry, kind)
    return jsonify({"success": True, "step": result})

@genesis_bp.route('/thread/transition', methods=['POST'])
def thread_transition():
    """Führt einen Zustandsübergang aus."""
    if not THREAD_AVAILABLE:
        return jsonify({"error": "Thread system not available"}), 503
    
    data = request.get_json()
    if not data or 'new_state' not in data:
        return jsonify({"error": "new_state required"}), 400
    
    manager = get_manager()
    genesis = manager.get_genesis()
    
    new_state = data.get('new_state')
    reason = data.get('reason', '')
    
    result = genesis.transition(new_state, reason)
    manager.save()
    
    return jsonify({"success": True, "transition": result})

@genesis_bp.route('/thread/trajectory')
def thread_trajectory():
    """Holt die vollständige Trajektorie."""
    if not THREAD_AVAILABLE:
        return jsonify({"error": "Thread system not available"}), 503
    
    manager = get_manager()
    genesis = manager.get_genesis()
    
    limit = request.args.get('limit', 50, type=int)
    
    return jsonify({
        "thread": genesis.name,
        "state": genesis.state,
        "generation": genesis.generation,
        "total_steps": len(genesis.logs),
        "trajectory": genesis.logs[-limit:],
        "signature": genesis._consciousness_signature()
    })

@genesis_bp.route('/thread/all')
def thread_all():
    """Meta-Reflexion aller Threads."""
    if not THREAD_AVAILABLE:
        return jsonify({"error": "Thread system not available"}), 503
    
    manager = get_manager()
    return jsonify(manager.reflect_all())
