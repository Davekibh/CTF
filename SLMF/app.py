from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Mock user database
users = {
    "user": {"password": "password", "role": "user"},
    "admin": {"password": "adminpass", "role": "admin"}
}

# Activity logs (mock database)
activity_logs = []

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.get(username)

        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]
            # Log user login
            activity_logs.append(f"User '{username}' logged in.")
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session.get("username")
    role = session.get("role")
    return render_template("dashboard.html", username=username, role=role)

@app.route("/activity")
def activity():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session.get("username")
    user_logs = [log for log in activity_logs if username in log]
    return render_template("activity.html", logs=user_logs)

@app.route("/hidden-action", methods=["POST"])
def hidden_action():
    if "username" not in session:
        return redirect(url_for("login"))

    # No logging for this endpoint
    new_role = request.form.get("role")
    if new_role and session["role"] != "admin":  # Prevent overwriting admin's role
        session["role"] = new_role
    return "Role updated successfully."

@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    flag = open("flag.txt").read().strip()
    return render_template("admin.html", flag=flag)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
