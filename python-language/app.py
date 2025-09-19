from flask import Flask, render_template
from scheduler import load_employees_from_csv, schedule_week

app = Flask(__name__)

@app.route("/")
def index():
    employees = load_employees_from_csv("employee.csv")
    schedule = schedule_week(employees)
    return render_template("schedule.html", schedule=schedule)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
