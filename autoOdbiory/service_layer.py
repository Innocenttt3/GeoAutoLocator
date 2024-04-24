from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from logic import EmailHandler
import os

app = Flask(__name__)
app.secret_key = 'sekret'
UPLOAD_FOLDER = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/autoOdbiory/server storage'
CONFIG_FILE_PATH = '/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini'

# Inicjalizacja globalnej instancji EmailHandler
email_handler = EmailHandler(CONFIG_FILE_PATH)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == 'admin':
            session['logged_in_user'] = username
            return redirect(url_for("upload"))
        else:
            return render_template("login.html", message="Nieprawidłowe dane logowania.")
    return render_template("login.html", message=None)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if 'logged_in_user' in session:
        username = session['logged_in_user']
        existing_files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        if request.method == "POST":
            selected_file = request.form.get("selected_file")
            if selected_file:
                session['email_data_file_path'] = os.path.join(UPLOAD_FOLDER, selected_file)
                return redirect(url_for("panel"))
            elif 'file' in request.files:
                file = request.files['file']
                if file.filename != '':
                    saved_file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
                    file.save(saved_file_path)
                    session['email_data_file_path'] = saved_file_path
                    return redirect(url_for("panel"))
        return render_template("upload.html", username=username, existing_files=existing_files)
    else:
        return redirect(url_for("login"))

@app.route("/panel", methods=["GET", "POST"])
def panel():
    if 'logged_in_user' in session:
        username = session['logged_in_user']
        email_data_file_path = session.get('email_data_file_path')

        if request.method == "POST":
            action = request.form.get("action")
            if action == "start":
                email_handler.set_email_data_file_path(email_data_file_path)
                email_handler.start_operations()
            elif action == "stop":
                email_handler.stop_operations()

        return render_template("panel.html", username=username, email_handler=email_handler)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('logged_in_user', None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
