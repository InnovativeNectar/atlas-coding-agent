import time
from typing import List, Dict, Any
from datetime import datetime

class Heartbeat:
    """Telemetry and status monitoring for Atlas."""

    def __init__(self):
        self.start_time = time.time()
        self.vitals = {
            "tasks_completed": 0,
            "errors_encountered": 0,
            "llm_calls": 0,
            "last_active": datetime.now().isoformat()
        }
        self.logs: List[str] = []

    def pulse(self, status: str):
        """Record a heartbeat event."""
        self.vitals["last_active"] = datetime.now().isoformat()
        log_entry = f"[{self.vitals['last_active']}] {status}"
        self.logs.append(log_entry)
        # In a real app, this could also write to a local telemetry file

    def get_status_report(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": round(uptime, 2),
            **self.vitals,
            "recent_logs": self.logs[-5:]
        }
