from flask import Flask, render_template
from flask_socketio import SocketIO
import json, os, threading

from core.scanner import scan_directory
from core.monitor import start_monitor

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

BASELINE_FILE = "baseline.json"
DIRECTORY = r"D:\Srushti ADYPU\Codetech\File Integrity Checker\test_folder"


def load_config():
    with open("config.json") as f:
        return json.load(f)


@app.route("/")
def index():
    return render_template("index.html")


# ✅ BASELINE ROUTE
@app.route("/create_baseline")
def create_baseline():
    config = load_config()

    data = scan_directory(
        DIRECTORY,
        config["hash_algorithm"],
        config["ignore_extensions"]
    )

    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Baseline created:", len(data))
    return {"status": "baseline created"}


# ✅ START WATCHDOG ONLY (IMPORTANT)
if __name__ == "__main__":
    threading.Thread(
        target=start_monitor,
        args=(DIRECTORY, socketio, app),
        daemon=True
    ).start()

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)