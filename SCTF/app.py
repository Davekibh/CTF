from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database initialization (only for first run)
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    with open("setup.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check credentials
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("search"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if "username" not in session:
        return redirect(url_for("login"))

    results = []
    if request.method == "POST":
        query = request.form.get("query")
        
        # Vulnerable SQL query
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username LIKE '%{query}%'")
        results = cursor.fetchall()
        conn.close()

    return render_template("search.html", results=results)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    # Initialize the database (run only once)
    init_db()
    app.run(debug=True)
