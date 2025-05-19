
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERNAME = "amarpanel1234"
PASSWORD = "amarpanel1234"

KEY_DIR = "keys"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        if user == USERNAME and pw == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Incorrect credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/panel/<game>", methods=["GET", "POST"])
def panel(game):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    keys = []
    error = ""
    if request.method == "POST":
        duration = request.form["duration"]
        count = int(request.form["count"])
        filename = f"{KEY_DIR}/{game}{duration}.txt"

        if not os.path.isfile(filename):
            error = "File does not exist."
        else:
            with open(filename, "r") as f:
                lines = f.read().splitlines()

            if len(lines) < count:
                error = f"Not enough keys available in {game}{duration}.txt"
            else:
                keys = lines[:count]
                with open(filename, "w") as f:
                    f.write("\n".join(lines[count:]))

    return render_template("panel.html", game=game, keys=keys, error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
