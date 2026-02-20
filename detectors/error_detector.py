from typing import List, Optional, Tuple, Dict, Any
class ErrorKeywordDetector:
    def __init__(self, keywords: List[str]):
        self.keywords = [k.strip() for k in keywords if k and k.strip()]
    def process_line(self, line: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        if not line.startswith("ERROR"):
            return None
        for kw in self.keywords:
            if kw in line:
                msg = f"Error keyword matched: {kw} | {line}"
                meta = {"keyword": kw}
                return ("HIGH", msg, meta)
            return ("MEDIUM", f"Generic error: {line}", {"keyword":None})