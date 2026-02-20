import detectors.failed_login
print(detectors.failed_login.__file__)
import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Any
from detectors.failed_login import FailedLoginDetector
from detectors.error_detector import ErrorKeywordDetector
def now_ts()-> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def write_alerts(alerts: List[Tuple[str, str, Dict[str, Any]]],text_path: str, jsonl_path: str)-> None:
    Path(text_path).parent.mkdir(parents=True, exist_ok=True)
    Path(jsonl_path).parent.mkdir(parents=True, exist_ok=True)
    with open(text_path, "a", encoding="utf-8") as ft, open(jsonl_path, "a", encoding="utf-8") as fj:
        for severity, message, meta in alerts:
            ts = now_ts()
            ft.write(f"{ts} | {severity} | {message}\n")
            event = {"timestamp": ts, "severity": severity, "message": message, "meta": meta}
            fj.write(json.dumps(event) + "\n")
def classify_counts(line: str, counts: Dict[str, int]) -> None:
    if line.startswith("INFO"):
        counts["INFO"] +=1
    elif line.startswith("WARNING"):
        counts["WARNING"] +=1
    elif line.startswith("ERROR"):
        counts["ERROR"] +=1
def process_line(line: str, detectors, counts)-> List[Tuple[str, str, Dict[str, Any]]]:
    alerts=[]
    classify_counts(line, counts)
    for det in detectors:
        out = det.process_line(line)
        if out:
            severity, msg, meta = out
            alerts.append((severity, msg, meta))
    return alerts
def run_once(log_file: str, config: dict) ->None:
    detectors = [
        FailedLoginDetector(
            threshold=config["failed_login_threshold"],
            window_seconds=config["failed_login_window_seconds"],
            cooldown_seconds=config["cooldown_seconds"],
        ),
        ErrorKeywordDetector(keywords=config.get("error_keywords", [])),
    ]
    counts = {"INFO":0, "WARNING":0, "ERROR": 0}
    all_alerts = []
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            all_alerts.extend(process_line(line, detectors, counts))
    write_alerts(all_alerts, config["alert_output_text"], config["alert_output_jsonl"])
    print(f"Run complete. INFO:{counts['INFO']} WARNING:{counts['WARNING']} ERROR:{counts['ERROR']} Alerts:{len(all_alerts)}")
def watch(log_file: str, config: dict, poll_seconds: float = 0.5) -> None:
    detectors = [
        FailedLoginDetector(
            threshold=config["failed_login_threshold"],
            window_seconds=config["failed_login_window_seconds"],
            cooldown_seconds=config["cooldown_seconds"],
        ),
        ErrorKeywordDetector(keywords=config.get("error_keywords", [])),
    ]
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    print(f"Watching log file: {log_file} (Ctrl+C to stop)")
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(poll_seconds)
                continue
            line = line.strip()
            alerts=process_line(line, detectors, counts)
            if alerts:
                write_alerts(alerts, config["alert_output_text"], config["alert_output_jsonl"])
                for sev, msg, _meta in alerts:
                    print(f"{now_ts()} | {sev} | {msg}")
def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as cf:
        return json.load(cf)
def main():
    parser = argparse.ArgumentParser(description="Infrastructure Log Monitoring & Alerting System")
    parser.add_argument("--config", default="config.json", help="Path to config.json")
    parser.add_argument("--log", default="sample_logs/system.log", help="Path to log file")
    parser.add_argument("--mode", choices=["once", "watch"], default="once", help="Run once or watch continuously")
    args = parser.parse_args()
    config=load_config(args.config)
    if args.mode =="once":
        run_once(args.log, config)
    else:
        watch(args.log, config)
if __name__ == "__main__":
    main()
               
#with open("config.json", "r") as config_file:
    #config = json.load(config_file)
#log_file = "sample_logs/system.log"
#incident_file = config["alert_output_file"]
#FAILED_THRESHOLD = config["failed_login_threshold"]
#failed_logins = {}
#alerts = []
#counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
#with open(log_file, "r") as file:
    #logs = file.readlines()
#for line in logs:
    #line = line.strip()
    #if line.startswith("INFO"):
     #   counts["INFO"] +=1
    #elif line.startswith("WARNING"):
     #   counts["WARNING"] +=1
    #elif line.startswith("ERROR"):
     #   counts["ERROR"] +=1
      #  alerts.append(("HIGH", line))
    #if "Failed login attempt" in line:
     #   ip = line.split("from ")[1]
      #  failed_logins[ip] = failed_logins.get(ip,0)+1
#for ip, count in failed_logins.items():
 #   if count >= FAILED_THRESHOLD:
  #      message = f"Multiple failed logins from {ip} ({count} attempts)"
   #     alerts.append(("CRITICAL",message))
    #    counts["CRITICAL"] +=1
#with open(incident_file, "w") as file:
 #   for severity, message in alerts:
  #      timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   #     file.write(f"{timestamp}|{severity}|{message}\n")
#print("Monitoring complete.")
#print(f"INFO: {counts['INFO']} | WARNING: {counts['WARNING']} | ERROR: {counts['ERROR']} | CRITICAL: {counts['CRITICAL']}")
#print(f"Alerts written to: {incident_file}")