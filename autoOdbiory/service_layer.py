from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from logic import EmailHandler
import os
import configparser
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sekret'
UPLOAD_FOLDER = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/autoOdbiory/server storage'
RESULTS_FOLDER = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/autoOdbiory/results'
CONFIG_FILE_PATH = '/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini'

email_handler = EmailHandler(CONFIG_FILE_PATH)
service_config = configparser.ConfigParser()
service_config.read(CONFIG_FILE_PATH)

users = []
for section in service_config.sections():
    if section.startswith('USER'):
        user_data = {
            'username': service_config.get(section, 'Username'),
            'password': service_config.get(section, 'Password')
        }
        users.append(user_data)


def get_json_file_path_with_current_date(directory: str, prefix: str = "data", suffix: str = ".json") -> str:
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{prefix}_{formatted_datetime}{suffix}"
    file_path = os.path.join(directory, file_name)
    return file_path


def get_latest_json_file(directory: str) -> str:
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    if not json_files:
        return None
    latest_file = max(json_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    return os.path.join(directory, latest_file)


@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password_input = request.form["password"]
        for user in users:
            if username == user['username'] and password_input == user['password']:
                session['logged_in_user'] = username
                return redirect(url_for("upload"))
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
        json_path = get_json_file_path_with_current_date(RESULTS_FOLDER)
        if request.method == "POST":
            action = request.form.get("action")
            if action == "start":
                email_handler.set_email_data_file_path(email_data_file_path)
                email_handler.start_operations()
            elif action == "stop":
                email_handler.stop_operations(json_path)
                return redirect(url_for("download"))
        return render_template("panel.html", username=username, email_handler=email_handler)
    else:
        return redirect(url_for("login"))



@app.route("/download", methods=["GET"])
def download():
    json_path = get_latest_json_file(RESULTS_FOLDER)
    if json_path:
        return send_file(json_path, as_attachment=True)
    else:
        return "Brak plików JSON do pobrania"


if __name__ == "__main__":
    app.run(debug=True)
