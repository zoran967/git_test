from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# In-memory storage for APM-2 data
data_storage = []

# HTML template to display PM data in a table
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>APM-2 PM Data</title>
    <style>
        table { border-collapse: collapse; width: 60%; margin: 20px auto; }
        th, td { border: 1px solid #333; padding: 8px; text-align: center; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2 style="text-align:center;">APM-2 Sensor PM Data</h2>
    <table>
        <tr>
            <th>Timestamp (UTC)</th>
            <th>PM2.5 (µg/m³)</th>
            <th>PM10 (µg/m³)</th>
        </tr>
        {% for item in data %}
        <tr>
            <td>{{ item.timestamp }}</td>
            <td>{{ item.pm25 or '-' }}</td>
            <td>{{ item.pm10 or '-' }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/apm2", methods=["POST"])
def receive_data():
    # Expect data as key=value pairs separated by &
    raw_data = request.get_data(as_text=True)
    
    # Convert to dictionary
    data_dict = {}
    for pair in raw_data.split("&"):
        if "=" in pair:
            key, value = pair.split("=")
            data_dict[key.strip()] = value.strip()
    
    # Keep only PM2.5 and PM10
    pm_data = {
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "pm25": data_dict.get("pm2.5"),
        "pm10": data_dict.get("pm10")
    }
    
    # Store in memory
    data_storage.append(pm_data)
    
    print(f"Received: {pm_data}")
    return "OK", 200

@app.route("/data")
def view_data():
    return render_template_string(HTML_TEMPLATE, data=data_storage)

@app.route("/")
def home():
    return "APM-2 Data Receiver is running! Visit /data to see PM2.5 and PM10 table."
