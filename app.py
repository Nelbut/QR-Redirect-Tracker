from flask import Flask, redirect, request, send_file, render_template_string
import csv
from datetime import datetime
import os
from collections import Counter

app = Flask(__name__)

LOG_FILE = "qr_scans.csv"

# -------------------------
# Logging function
# -------------------------
def log_scan(code_name, user_agent, ip):
    """
    Appends a scan to the CSV file.
    Creates the file with headers if it doesn't exist.
    """
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "code", "ip", "user_agent"])
        writer.writerow([datetime.now(), code_name, ip, user_agent])

# -------------------------
# Home route
# -------------------------
@app.route("/", methods=["GET"])
def home():
    """
    Main page - logs a 'direct' visit if someone types/copies the URL.
    """
    log_scan("direct_visit", request.headers.get("User-Agent"), request.remote_addr)
    return "QR redirect tracker is running! Visit /qr1 or /qr2 for QR redirects."

# -------------------------
# QR redirect routes
# -------------------------
@app.route("/qr1", methods=["GET"])
def qr1():
    log_scan("qr1", request.headers.get("User-Agent"), request.remote_addr)
    return redirect("https://www.focuscalisthenics.co.uk")  # Change if needed

@app.route("/qr2", methods=["GET"])
def qr2():
    log_scan("qr2", request.headers.get("User-Agent"), request.remote_addr)
    return redirect("https://www.focuscalisthenics.co.uk")  # Change if needed

# -------------------------
# Logs download route
# -------------------------
@app.route("/logs", methods=["GET"])
def logs():
    if os.path.exists(LOG_FILE):
        return send_file(LOG_FILE)
    return "No logs yet."

# -------------------------
# Dashboard route
# -------------------------
@app.route("/dashboard", methods=["GET"])
def dashboard():
    if not os.path.exists(LOG_FILE):
        return "No scans yet."

    counter = Counter()
    with open(LOG_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            counter[row["code"]] += 1

    # Simple HTML table for display
    html = """
    <h1>QR Scan Dashboard</h1>
    <table border="1" cellpadding="5">
      <tr><th>Code</th><th>Number of Scans</th></tr>
      {% for code, count in counts.items() %}
        <tr><td>{{ code }}</td><td>{{ count }}</td></tr>
      {% endfor %}
    </table>
    """
    return render_template_string(html, counts=counter)

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
