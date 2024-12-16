import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create Users Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    # Insert some test data
    c.execute('INSERT OR IGNORE INTO users (username, password) VALUES ("admin", "supersecurepassword")')
    c.execute('INSERT OR IGNORE INTO users (username, password) VALUES ("guest", "guestpassword")')
    conn.commit()
    conn.close()

# Route: Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vulnerable SQL Query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            if username == "admin":
                return redirect(url_for('admin'))
            return "Login successful! But you're not admin."
        return "Invalid credentials!"
    return render_template('login.html')

# Route: Admin Page
@app.route('/admin')
def admin():
    return render_template('admin.html', flag="CTF{SQL_1nj3cti0n_Success}")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
