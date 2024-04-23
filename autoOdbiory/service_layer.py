from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

from db_connector import DatabaseConnector
from logic import EmailHandler

app = Flask(__name__)
app.secret_key = 'sekret'


config_file_path = '/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini'

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #database = DatabaseConnector('/Users/kamilgolawski/Nauka/Programowanie/pliki init/dbConfig.ini')
        #database.connect()
        if username == 'admin':
            session['logged_in_user'] = username
            return redirect(url_for("upload"))
        else:
            return render_template("login.html", message="Nieprawidłowe dane logowania.")
    return render_template("login.html", message=None)


from flask import request, redirect, url_for

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if 'logged_in_user' in session:
        username = session['logged_in_user']
        if request.method == "POST" and 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                saved_file_path = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/autoOdbiory/server storage/' + secure_filename(file.filename)
                file.save(saved_file_path)
                session['email_data_file_path'] = saved_file_path
                return redirect(url_for("panel"))
        return render_template("upload.html", username=username)
    else:
        return redirect(url_for("login"))

@app.route("/panel", methods=["GET", "POST"])
def panel():
    if 'logged_in_user' in session:
        email_data_file_path = session.get('email_data_file_path')
        email_handler = EmailHandler(config_file_path, email_data_file_path)
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
