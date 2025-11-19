from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route("/apm2", methods=["POST"])
def receive_data():
    data = request.get_data(as_text=True)

    # Save incoming data to a file
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(data)

    print("Received:")
    print(data)

    return "OK", 200

@app.route("/")
def home():
    return "APM-2 Data Receiver is running!"
