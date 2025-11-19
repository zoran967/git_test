from flask import Flask, request, render_template_string
import datetime
import csv
import os

app = Flask(__name__)

# Correct writable folder for Render
DATA_FILE = "/opt/render/project/src/pm_data.csv"

# Create the CSV with headers once
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "pm2.5", "pm10"])

@app.route("/apm2", methods=["POST"])
def receive():
    pm25 = request.form.get("pm2.5")
    pm10 = request.form.get("pm10")
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Append data to CSV
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([ts, pm25, pm10])

    print("RECEIVED:", pm25, pm10)
    return "OK"

@app.route("/data")
def data():
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline="") as f:
            rows = list(csv.reader(f))

    html = """
    <h1>PM Sensor Data</h1>
    <table border="1" cellpadding="5">
        <tr><th>Timestamp</th><th>PM2.5</th><th>PM10</th></tr>
        {% for r in rows[1:] %}
            <tr><td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td></tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, rows=rows)

@app.route("/")
def home():
    return "APM server running!"

