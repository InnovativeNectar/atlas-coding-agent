import time
import json
import os
from typing import List, Dict, Any
from datetime import datetime

class Heartbeat:
    """Telemetry and status monitoring for Atlas (Persistent Singleton)."""
    _instance = None
    _file_path = "/root/projects/atlas-coding-agent/atlas_vitals.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Heartbeat, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "r") as f:
                    data = json.load(f)
                    self.start_time = data.get("start_time", time.time())
                    self.vitals = data.get("vitals", {
                        "tasks_completed": 0,
                        "errors_encountered": 0,
                        "llm_calls": 0,
                        "last_active": datetime.now().isoformat()
                    })
                    self.logs = data.get("logs", [])
            except:
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.start_time = time.time()
        self.vitals = {
            "tasks_completed": 0,
            "errors_encountered": 0,
            "llm_calls": 0,
            "last_active": datetime.now().isoformat()
        }
        self.logs = []

    def _save(self):
        with open(self._file_path, "w") as f:
            json.dump({
                "start_time": self.start_time,
                "vitals": self.vitals,
                "logs": self.logs
            }, f)

    def save(self):
        """Manually trigger a save of the vitals."""
        self._save()

    def pulse(self, status: str):
        """Record a heartbeat event."""
        self.vitals["last_active"] = datetime.now().isoformat()
        log_entry = f"[{self.vitals['last_active']}] {status}"
        self.logs.append(log_entry)
        if len(self.logs) > 50:
            self.logs = self.logs[-50:]
        self._save()

    def get_status_report(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": round(uptime, 2),
            **self.vitals,
            "recent_logs": self.logs[-10:]
        }

