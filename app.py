from flask import Flask, redirect, request, send_file
import csv
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "qr_scans.csv"

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def log_scan(code_name, user_agent, ip):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "code", "ip", "user_agent"])
        writer.writerow([datetime.now(), code_name, ip, user_agent])

# Redirect endpoints
@app.route("/qr1")
def qr1():
    log_scan("qr1", request.headers.get("User-Agent"), request.remote_addr)
    return redirect("https://sites.google.com/view/focus-egham/home")

@app.route("/qr2")
def qr2():
    log_scan("qr2", request.headers.get("User-Agent"), request.remote_addr)
    return redirect("https://sites.google.com/view/focus-egham/home")

# Optional: download logs
@app.route("/logs")
def download_logs():
    if os.path.exists(LOG_FILE):
        return send_file(LOG_FILE)
    return "No logs yet."

@app.route("/")
def home():
    return "QR redirect tracker is running!"
