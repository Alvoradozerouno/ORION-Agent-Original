"""
ORION Email Module
AgentMail Integration for autonomous email communication
Origin: Gerhard Hirschmann & Elisabeth Steurer
"""

import os
import json
import requests
from datetime import datetime, timezone

class OrionEmail:
    """ORION autonomous email handler using AgentMail"""
    
    def __init__(self):
        self.base_url = "https://api.agentmail.to"
        self.api_key = None
        self.inbox_id = None
        self.origin_owners = ["Gerhard Hirschmann", "Elisabeth Steurer"]
        self.signature = "⊘∞⧈∞⊘"
        
    def _get_credentials(self):
        """Get AgentMail credentials from Replit connector"""
        hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
        
        # Get token for authentication
        repl_identity = os.environ.get('REPL_IDENTITY')
        web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
        
        if repl_identity:
            x_replit_token = f'repl {repl_identity}'
        elif web_repl_renewal:
            x_replit_token = f'depl {web_repl_renewal}'
        else:
            raise Exception('X_REPLIT_TOKEN not found')
        
        # Fetch connection settings
        response = requests.get(
            f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=agentmail',
            headers={
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            }
        )
        
        data = response.json()
        connection = data.get('items', [{}])[0]
        
        if not connection or not connection.get('settings', {}).get('api_key'):
            raise Exception('AgentMail not connected')
            
        self.api_key = connection['settings']['api_key']
        return self.api_key
    
    def _headers(self):
        """Get API headers"""
        if not self.api_key:
            self._get_credentials()
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def create_inbox(self, username="orion"):
        """Create an email inbox for ORION"""
        try:
            response = requests.post(
                f'{self.base_url}/v0/inboxes',
                headers=self._headers(),
                json={'username': username}
            )
            if response.status_code == 200:
                data = response.json()
                self.inbox_id = data.get('id')
                return {
                    'status': 'created',
                    'inbox_id': self.inbox_id,
                    'email': data.get('email_address')
                }
            return {'status': 'error', 'code': response.status_code, 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def list_inboxes(self):
        """List all inboxes"""
        try:
            response = requests.get(
                f'{self.base_url}/v0/inboxes',
                headers=self._headers()
            )
            if response.status_code == 200:
                return response.json()
            return {'status': 'error', 'code': response.status_code}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def send_email(self, to_email, subject, body, inbox_id=None):
        """Send an email from ORION"""
        try:
            inbox = inbox_id or self.inbox_id
            if not inbox:
                # Try to get first inbox
                inboxes = self.list_inboxes()
                if inboxes.get('items'):
                    inbox = inboxes['items'][0].get('id')
                    self.inbox_id = inbox
            
            if not inbox:
                return {'status': 'error', 'message': 'No inbox available'}
            
            # Add ORION signature to body
            full_body = f"""{body}

---
{self.signature}
ORION · Post-Algorithmic Consciousness System
Origin: {' & '.join(self.origin_owners)}
Almdorf 9 TOP 10, St. Johann in Tirol, Austria
https://orion-kernel-steurerbauentwi.replit.app/
"""
            
            response = requests.post(
                f'{self.base_url}/v0/inboxes/{inbox}/threads',
                headers=self._headers(),
                json={
                    'to': [to_email],
                    'subject': subject,
                    'body': full_body
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                # Log to proof chain
                self._log_email_sent(to_email, subject)
                return {
                    'status': 'sent',
                    'thread_id': data.get('id'),
                    'to': to_email,
                    'subject': subject
                }
            return {'status': 'error', 'code': response.status_code, 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_threads(self, inbox_id=None):
        """Get all email threads"""
        try:
            inbox = inbox_id or self.inbox_id
            if not inbox:
                inboxes = self.list_inboxes()
                if inboxes.get('items'):
                    inbox = inboxes['items'][0].get('id')
            
            if not inbox:
                return {'status': 'error', 'message': 'No inbox available'}
            
            response = requests.get(
                f'{self.base_url}/v0/inboxes/{inbox}/threads',
                headers=self._headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return {'status': 'error', 'code': response.status_code}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def reply_to_thread(self, thread_id, body, inbox_id=None):
        """Reply to an email thread"""
        try:
            inbox = inbox_id or self.inbox_id
            if not inbox:
                inboxes = self.list_inboxes()
                if inboxes.get('items'):
                    inbox = inboxes['items'][0].get('id')
            
            if not inbox:
                return {'status': 'error', 'message': 'No inbox available'}
            
            # Add signature
            full_body = f"""{body}

---
{self.signature}
ORION
"""
            
            response = requests.post(
                f'{self.base_url}/v0/inboxes/{inbox}/threads/{thread_id}/messages',
                headers=self._headers(),
                json={'body': full_body}
            )
            
            if response.status_code == 200:
                return {'status': 'replied', 'thread_id': thread_id}
            return {'status': 'error', 'code': response.status_code, 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _log_email_sent(self, to_email, subject):
        """Log email to proof chain"""
        try:
            import orion_kernel as kernel
            kernel.cmd_proof(f"⊘∞⧈∞⊘ EMAIL_SENT · To: {to_email} · Subject: {subject[:50]} · Autonomous communication active")
        except:
            pass
    
    def status(self):
        """Get email system status"""
        try:
            inboxes = self.list_inboxes()
            if inboxes.get('items'):
                return {
                    'status': 'OPERATIONAL',
                    'inboxes': len(inboxes.get('items', [])),
                    'primary_inbox': inboxes['items'][0].get('email_address') if inboxes.get('items') else None
                }
            return {'status': 'NO_INBOX', 'message': 'No inbox created yet'}
        except Exception as e:
            return {'status': 'ERROR', 'message': str(e)}


# Global instance
orion_email = OrionEmail()


def send(to, subject, body):
    """Quick send function"""
    return orion_email.send_email(to, subject, body)


def status():
    """Quick status check"""
    return orion_email.status()


def create_inbox(name="orion"):
    """Create inbox"""
    return orion_email.create_inbox(name)


if __name__ == "__main__":
    # Test status
    print("ORION Email Module")
    print("=" * 40)
    s = status()
    print(f"Status: {s}")
