from flask import Flask, render_template, request
import sqlite3
from distance import ev_ranges  # Your EV model → range data

app = Flask(__name__)

# Fetch all chargers from DB
def get_all_chargers():
    conn = sqlite3.connect("data/chargers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chargers")
    chargers = cursor.fetchall()
    conn.close()
    return chargers

@app.route("/", methods=["GET", "POST"])
def home():
    chargers = get_all_chargers()
    selected_model = None
    selected_range = None
    selected_units = "KM" # default is now kilometers

    if request.method == "POST":
        selected_model = request.form.get("ev_model")
        selected_unit = request.form.get("unit", "km")
        range_km = ev_ranges.get(selected_model)
        if range_km:
            if selected_unit == "miles":
                selected_range = round(range_km * 0.621371, 1)
            else:
                selected_range = range_km

    return render_template(
        "index.html",
        chargers=chargers,
        ev_models=sorted(ev_ranges.keys()),
        selected_model=selected_model,
        selected_range=selected_range,
        selected_unit=selected_unit,
    )

if __name__ == "__main__":
    app.run(debug=True)