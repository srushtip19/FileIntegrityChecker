import os
from datetime import datetime

LOG_FILE = "logs/fim.log"

def log_event(message):
    os.makedirs("logs", exist_ok=True)

    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")