import time
from typing import Dict, List, Tuple, Optional
class FailedLoginDetector:
    def __init__(self, threshold: int, window_seconds: int, cooldown_seconds:int):
        self.threshold=threshold
        self.window_seconds=window_seconds
        self.cooldown_seconds=cooldown_seconds
        self.attempts: Dict[str, List[float]]={}
        self.last_alert_time: Dict[str, float]={}
    def process_line(self, line: str)->Optional[Tuple[str, str, dict]]:
        if "Failed login attempt" not in line or "from " not in line:
            return None
        ip = line.split("from ", 1)[1].strip()
        now = time.time()
        recent = [t for t in self.attempts.get(ip, []) if now - t <=self.window_seconds]
        recent.append(now)
        self.attempts[ip]= recent
        last_alert = self.last_alert_time.get(ip,0)
        if len(recent) >= self.threshold and (now - last_alert) >=self.cooldown_seconds:
            self.last_alert_time[ip] = now
            msg = f"Multiple failed logins from {ip} ({len(recent)} attempts in {self.window_seconds}s)"
            meta = {"ip": ip,
                    "count": len(recent),
                    "window_seconds": self.window_seconds
                }
            return ("CRITICAL", msg, meta)
        return None