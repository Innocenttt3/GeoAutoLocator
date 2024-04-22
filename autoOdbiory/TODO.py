from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

users = {
    "user1": "password1",
    "user2": "password2"
}
def check_user(username, password):
    return username in users and users[username] == password

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_user(username, password):
            return redirect(url_for("panel"))
        else:
            return render_template("login.html", message="Nieprawidłowe dane logowania.")
    return render_template("login.html", message=None)

@app.route("/panel", methods=["GET"])
def panel():
    return render_template("panel.html")


if __name__ == "__main__":
    app.run(debug=True)
