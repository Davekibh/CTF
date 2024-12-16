from flask import Flask, request, render_template, redirect, url_for, make_response

app = Flask(__name__)

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

        # Weak authentication logic
        if username == "admin" and password == "password123":
            resp = make_response(redirect(url_for('admin')))
            resp.set_cookie('auth', 'admin')
            return resp
        return "Invalid credentials!"
    return render_template('login.html')

# Route: Admin Page (Accessible via cookie manipulation)
@app.route('/admin')
def admin():
    auth = request.cookies.get('auth')
    if auth == 'admin':
        return render_template('admin.html', flag="CTF{Auth_Failure_Bypassed}")
    return "403 Forbidden: Unauthorized Access", 403

if __name__ == '__main__':
    app.run(debug=True)
