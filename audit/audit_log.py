import json
from datetime import datetime

AUDIT_FILE = "audit/audit_log.json"

def log_event(actor, action, target, details):
    event = {
        "timestamp": datetime.now().isoformat(),
        "actor": actor,
        "action": action,
        "target": target,
        "details": details
    }

    try:
        with open(AUDIT_FILE, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(event)

    with open(AUDIT_FILE, "w") as f:
        json.dump(logs, f, indent=2)
