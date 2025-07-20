from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Function to fetch all chargers from the database
def get_all_chargers():
    conn = sqlite3.connect("data/chargers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chargers")
    chargers = cursor.fetchall()
    conn.close()
    return chargers

# Homepage route 
@app.route("/")
def home():
    chargers = get_all_chargers()
    return render_template("index.html", chargers=chargers)

if __name__ == "__main__":
    app.run(debug=True)