import json
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
JSONL_PATH = "alerts/incident_log.jsonl"
def parse_timestamp(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts.replace("Z", ""))
    except Exception:
        return datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
def main():
    events=[]
    with open(JSONL_PATH, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    if not events:
        print("No events found. Generate alerts first (run monitor.py).")
        return
    sev_counts=Counter(e.get("severity", "UNKNOWN") for e in events)
    buckets=defaultdict(int)
    for e in events:
        ts=parse_timestamp(e.get("timestamp", ""))
        key=ts.replace(second=0, microsecond=0)
        buckets[key] +=1
    times = sorted(buckets.keys())
    counts=[buckets[t] for t in times]
    ip_counts = Counter()
    for e in events:
        meta = e.get("meta") or {}
        ip = meta.get("ip")
        if ip:
            ip_counts[ip] +=1
    plt.figure()
    labels = list(sev_counts.keys())
    values = [sev_counts[k] for k in labels]
    plt.bar(labels, values)
    plt.title("Alert Count by Severity")
    plt.xlabel("Severity")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("alerts/dashboard_severity.png", dpi=200)

    plt.figure()
    plt.plot(times, counts, marker="o")
    plt.title("Alerts Over Time (per minute)")
    plt.xlabel("Time")
    plt.ylabel("Alerts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("alerts/dashboard_timeline.png", dpi=200)

    print("\n Dashboard generated:")
    print(" - alerts/dashboard_severity.png")
    print(" - alerts/dashboard_timeline.png")

    if ip_counts:
        print("\n Top IPs:")
        for ip, c in ip_counts.most_common(5):
            print(f" - {ip}: {c}")
if __name__ == "__main__":
    main()