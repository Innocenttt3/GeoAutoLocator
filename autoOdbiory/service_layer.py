from flask import Flask, render_template, request, redirect, url_for, session
from db_connector import DatabaseConnector

app = Flask(__name__)
app.secret_key = 'sekret'

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #database = DatabaseConnector("/Users/kamilgolawski/Nauka/Programowanie/pliki init/dbConfig.ini")
        #database.connect()
        if True:
            session['logged_in_user'] = username
            return redirect(url_for("panel"))
        else:
            return render_template("login.html", message="Nieprawidłowe dane logowania.")
    return render_template("login.html", message=None)

@app.route("/panel", methods=["GET"])
def panel():
    if 'logged_in_user' in session:
        username = session['logged_in_user']
        return render_template("panel.html", username=username)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('logged_in_user', None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
