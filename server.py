from flask import Flask, request, render_template_string
import datetime
import csv
import os

app = Flask(__name__)

DATA_FILE = "pm_data.csv"

# Ensure CSV file exists with headers
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "pm2.5", "pm10"])

@app.route("/apm2", methods=["POST"])
def receive_data():
    pm25 = request.form.get("pm2.5")
    pm10 = request.form.get("pm10")
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, pm25, pm10])

    print(f"Received PM2.5={pm25} PM10={pm10}")
    return "OK", 200

@app.route("/data")
def show_data():
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

    table_html = """
    <table border="1" cellpadding="5">
        <tr>
            <th>Timestamp (UTC)</th>
            <th>PM2.5</th>
            <th>PM10</th>
        </tr>
        {% for row in rows[1:] %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(table_html, rows=rows)

@app.route("/")
def home():
    return "APM-2 Data Receiver is running!"
