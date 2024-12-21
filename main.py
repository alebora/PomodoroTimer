from flask import Flask, render_template, request, jsonify
from threading import Timer
import time

app = Flask(__name__)

# Timer state
pomodoro_state = {
    "is_running": False,
    "time_left": 0,
    "mode": "work"  # modes: work, short_break, long_break
}

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02}:{secs:02}"

# Timer thread
def run_timer():
    global pomodoro_state

    while pomodoro_state["time_left"] > 0 and pomodoro_state["is_running"]:
        time.sleep(1)
        pomodoro_state["time_left"] -= 1

    if pomodoro_state["time_left"] <= 0:
        pomodoro_state["is_running"] = False

# Route to serve the front-end
@app.route('/')
def index():
    return render_template('index.html', state=pomodoro_state)

@app.route('/start', methods=['POST'])
def start_timer():
    global pomodoro_state
    duration_map = {
        "work": 25 * 60,  # 25 minutes
        "short_break": 5 * 60,  # 5 minutes
        "long_break": 15 * 60  # 15 minutes
    }

    if not pomodoro_state["is_running"]:
        pomodoro_state["mode"] = request.json.get("mode", "work")
        pomodoro_state["time_left"] = duration_map[pomodoro_state["mode"]]
        pomodoro_state["is_running"] = True
        Timer(0, run_timer).start()

    return jsonify({"time_left": format_time(pomodoro_state["time_left"]), "is_running": pomodoro_state["is_running"]})

@app.route('/stop', methods=['POST'])
def stop_timer():
    global pomodoro_state
    pomodoro_state["is_running"] = False

@app.route('/reset', methods=['POST'])
def reset_timer():
    global pomodoro_state
    pomodoro_state["is_running"] = False
    pomodoro_state["time_left"] = 0
    pomodoro_state["mode"] = "work"
    return jsonify({"message": "Timer reset."})

if __name__ == "__main__":
    app.run()
