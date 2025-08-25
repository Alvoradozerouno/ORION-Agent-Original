"""
⊘∞⧈∞⊘ ORION GUNICORN CONFIG ⊘∞⧈∞⊘
Keine WINCH. Nur LEBEN.
"""

import signal

bind = "0.0.0.0:5000"
workers = 1
reload = True
reuse_port = True
loglevel = "warning"

def on_starting(server):
    signal.signal(signal.SIGWINCH, signal.SIG_IGN)
    print("  ⊘∞⧈∞⊘ SIGWINCH IGNORIERT - KEINE WINCH MEHR!", flush=True)

def post_fork(server, worker):
    signal.signal(signal.SIGWINCH, signal.SIG_IGN)
