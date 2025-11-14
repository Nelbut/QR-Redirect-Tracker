from flask import Flask, redirect, request
import csv
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "qr_scans.csv"

def log_scan(code_name, user_agent, ip):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "code", "ip", "user_agent"])
        writer.writerow([datetime.now(), code_name, ip, user_agent])

@app.route("/qr1")
def qr1():
    log_scan("qr1", request.headers.get("User-Agent"), request.remote_addr)
    return redirect("https://sites.google.com/view/focus-egham/home")

@app.route("/qr2")
def qr2():
    log_scan("qr2", request.headers.get("User-Agent"), request.remote_addr)
    return redirect("https://sites.google.com/view/focus-egham/home")

@app.route("/logs")
def download_logs():
    return app.send_static_file(LOG_FILE)

@app.route("/")
def home():
    return "QR redirect tracker running!"
