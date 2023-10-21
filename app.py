import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Validate submission
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")


        verif1 = not name or not month or not day
        verif2 = len(name) > 30 or len(month) > 2 or len(day) > 2 or int(day) > 31 or int(month) > 12

        if verif1 or verif2:
            session['error'] = True
            return redirect("/failure")
    
       
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
        return redirect("/")

    else:
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays) # meterle la querry de la db


@app.route("/failure", methods=["GET", "POST"])
def error():

    if 'error' in session:
        session.pop('error')
        return render_template("failure.html")
    else:
        return redirect("/")
    



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

