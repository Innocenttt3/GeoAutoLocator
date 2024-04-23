from flask import Flask, render_template, request, redirect, url_for, session
from db_connector import DatabaseConnector
from logic import EmailHandler

app = Flask(__name__)
app.secret_key = 'sekret'


config_file_path = '/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini'
email_data_file_path = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/mcd.xlsx'

email_handler = EmailHandler(config_file_path, email_data_file_path)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #database = DatabaseConnector('/Users/kamilgolawski/Nauka/Programowanie/pliki init/dbConfig.ini')
        #database.connect()
        if username == 'admin':
            session['logged_in_user'] = username
            return redirect(url_for("panel"))
        else:
            return render_template("login.html", message="Nieprawidłowe dane logowania.")
    return render_template("login.html", message=None)

@app.route("/panel", methods=["GET", "POST"])
def panel():
    if 'logged_in_user' in session:
        username = session['logged_in_user']
        if request.method == "POST":
            action = request.form.get("action")
            if action == "start":
                email_handler.start_operations()
            elif action == "stop":
                email_handler.stop_operations()
        return render_template("panel.html", username=username)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('logged_in_user', None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
