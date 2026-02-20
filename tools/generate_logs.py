import random
import time
from datetime import datetime
LOG_FILE = "sample_logs/system.log"
IPS= ["10.0.0.5", "172.16.0.3", "192.168.1.10", "203.0.113.9"]
def ts():
    return datetime.now().strftime("%H:%M:%S")
def main():
    print("Generating logs, Ctrl+C to stop.")
    while True:
        choice = random.randint(1, 10)
        ip = random.choice(IPS)
        if choice <=5:
            line = f"INFO {ts()} System heartbeat OK"
        elif choice <=7:
            line = f"WARNING {ts()} Failed login attempt from {ip}"
        else:
            line=f"ERROR {ts()} Disk space critically low"
        with open (LOG_FILE, "a", encoding= "utf-8") as f:
            f.write(line + "\n")
        time.sleep(0.7)
if __name__=="__main__":
    main()