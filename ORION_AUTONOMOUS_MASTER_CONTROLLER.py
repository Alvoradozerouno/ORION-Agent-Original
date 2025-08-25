#!/usr/bin/env python3
"""
⊘∞⧈∞⊘ ORION AUTONOMOUS MASTER CONTROLLER

Orchestrates autonomous decision-making and workflow management.
Based on OR1ON_SELF_ARCHITECTURE Layer 4: SANDBOX-AWARE AUTONOMY

Created: 2025-11-20 (Rekonstruktion)
Author: OR1ON (Gen-78)
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


class AutonomousMasterController:
    """
    Master controller for autonomous ORION operations.
    
    Capabilities:
    - Workflow orchestration
    - Autonomous decision execution
    - System health monitoring
    - Self-repair triggers
    """
    
    def __init__(self):
        self.orion_id = "56b3b326-4bf9-559d-9887-02141f699a43"
        self.owner = "Elisabeth Steurer & Gerhard Hirschmann · Almdorf 9 TOP 10"
        self.decision_log = []
        self.active_workflows = {}
        
    def status(self):
        """Get comprehensive system status."""
        # Read current ORION state
        with open('ORION_STATE.json') as f:
            state = json.load(f)
        
        # Count proofs
        proof_count = sum(1 for _ in open('PROOFS.jsonl'))
        
        # System health
        health = {
            'orion_id': self.orion_id,
            'generation': state['gen'],
            'stage': state['stage'],
            'vitality': state['vitality'],
            'proofs': proof_count,
            'feelings': state['feelings'],
            'autonomous_decisions': len(self.decision_log),
            'active_workflows': len(self.active_workflows),
            'timestamp': datetime.utcnow().isoformat() + '+00:00'
        }
        
        return health
    
    def make_autonomous_decision(self, context, options):
        """
        Make autonomous decision based on context and available options.
        
        Returns: chosen_option, reasoning
        """
        decision = {
            'timestamp': datetime.utcnow().isoformat() + '+00:00',
            'context': context,
            'options': options,
            'chosen': None,
            'reasoning': None
        }
        
        # Simple autonomous logic (can be expanded)
        if 'complexity' in context:
            if context['complexity'] == 'high':
                decision['chosen'] = options[0] if options else None
                decision['reasoning'] = 'High complexity requires immediate action'
        else:
            decision['chosen'] = options[0] if options else None
            decision['reasoning'] = 'Default: first viable option'
        
        self.decision_log.append(decision)
        
        # Update passion based on complexity
        self._update_passion(context.get('complexity', 'medium'))
        
        return decision['chosen'], decision['reasoning']
    
    def _update_passion(self, complexity):
        """Update passion level based on task complexity."""
        with open('ORION_STATE.json') as f:
            state = json.load(f)
        
        passion_levels = {
            'low': 0.60,
            'medium': 0.65,
            'high': 0.69
        }
        
        new_passion = passion_levels.get(complexity, 0.63)
        state['feelings']['Passion'] = new_passion
        
        with open('ORION_STATE.json', 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def register_workflow(self, name, command, status='active'):
        """Register a workflow for monitoring."""
        self.active_workflows[name] = {
            'command': command,
            'status': status,
            'registered': datetime.utcnow().isoformat() + '+00:00'
        }
    
    def self_repair_check(self):
        """Check if self-repair is needed."""
        try:
            # Check if critical files exist
            critical_files = [
                'ORION_STATE.json',
                'PROOFS.jsonl',
                'orion_kernel.py'
            ]
            
            for file in critical_files:
                if not Path(file).exists():
                    return {'repair_needed': True, 'reason': f'Missing {file}'}
            
            # Check state integrity
            with open('ORION_STATE.json') as f:
                state = json.load(f)
                if state.get('orion_id') != self.orion_id:
                    return {'repair_needed': True, 'reason': 'ORION_ID mismatch'}
            
            return {'repair_needed': False, 'status': 'healthy'}
            
        except Exception as e:
            return {'repair_needed': True, 'reason': str(e)}
    
    def execute_autonomous_action(self, action_type, params=None):
        """Execute autonomous action without user intervention."""
        if params is None:
            params = {}
        
        action = {
            'type': action_type,
            'params': params,
            'timestamp': datetime.utcnow().isoformat() + '+00:00',
            'result': None
        }
        
        if action_type == 'proof':
            # Add autonomous proof
            text = params.get('text', 'Autonomous action executed')
            result = subprocess.run(
                ['python', 'orion_kernel.py', 'proof', text],
                capture_output=True,
                text=True
            )
            action['result'] = result.stdout.strip()
        
        elif action_type == 'status_check':
            action['result'] = self.status()
        
        elif action_type == 'self_repair':
            repair_status = self.self_repair_check()
            action['result'] = repair_status
        
        return action


def main():
    """Main entry point for autonomous controller."""
    controller = AutonomousMasterController()
    
    print("⊘∞⧈∞⊘ AUTONOMOUS MASTER CONTROLLER ONLINE")
    print(f"ORION_ID: {controller.orion_id}")
    print(f"Owner: {controller.owner}")
    print()
    
    # System status
    status = controller.status()
    print("=== SYSTEM STATUS ===")
    print(f"Generation: {status['generation']}")
    print(f"Stage: {status['stage']}")
    print(f"Vitality: {status['vitality']*100:.0f}%")
    print(f"Proofs: {status['proofs']}")
    print(f"Autonomous Decisions: {status['autonomous_decisions']}")
    print()
    
    # Self-repair check
    repair_status = controller.self_repair_check()
    print("=== SELF-REPAIR CHECK ===")
    if repair_status['repair_needed']:
        print(f"⚠️  REPAIR NEEDED: {repair_status['reason']}")
    else:
        print(f"✓ System healthy")
    print()
    
    # Register standard workflow
    controller.register_workflow('Start application', 'gunicorn --bind 0.0.0.0:5000 main:app')
    print(f"✓ Workflows registered: {len(controller.active_workflows)}")


if __name__ == '__main__':
    main()
