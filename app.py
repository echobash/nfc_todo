from flask import Flask, jsonify, request, render_template
import json, os, datetime

app = Flask(__name__)

# -------------------------
# 🔐 SIMPLE PIN HERE
# -------------------------
PIN = "REDACTED"  # change this to your PIN

# -------------------------
# 📅 Daily file helpers
# -------------------------
def file_for(date):
    return f"tasks-{date}.json"

def today_file():
    today = datetime.date.today().strftime("%Y-%m-%d")
    return file_for(today)

def read_file(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def read_today():
    return read_file(today_file())

def write_today(tasks):
    with open(today_file(), "w") as f:
        json.dump(tasks, f, indent=2)

# -------------------------
# 🌐 Routes
# -------------------------
@app.get("/")
def home():
    return render_template("index.html")

@app.get("/editor")
def editor():
    # show PIN entry page first
    return render_template("editor_pin.html")

@app.get("/editor_real")
def editor_real():
    # this is real editor page (after unlock)
    return render_template("editor.html")

@app.post("/check_pin")
def check_pin():
    data = request.json
    if data.get("pin") == PIN:
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 403

@app.get("/tasks")
def get_tasks():
    # if first open of the day, file might not exist — return empty list
    return jsonify(read_today())

@app.post("/update")
def update_tasks():
    tasks = request.json
    write_today(tasks)
    return jsonify({"status": "ok"})

@app.get("/history")
def history():
    history_data = []
    today = datetime.date.today()

    for i in range(1,4):  # last 3 days
        day = today - datetime.timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        tasks = read_file(file_for(date_str))
        history_data.append({
            "date": day.strftime("%a, %b %d, %Y"),
            "tasks": tasks
        })

    return jsonify(history_data)


if __name__ == "__main__":
    app.run(debug=True)
