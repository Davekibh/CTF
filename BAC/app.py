from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# Dummy user data
users = {
    "guest": {"password": "guest123", "membership": "basic"}
}

flag = "CTF{Br0k3n_Acc3ss_C0ntr0l}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            resp = make_response(redirect(url_for('profile')))
            resp.set_cookie('username', username)
            resp.set_cookie('membership', users[username]['membership'])
            return resp
        return "Invalid credentials!", 401
    return render_template('login.html')


@app.route('/profile')
def profile():
    username = request.cookies.get('username')
    membership = request.cookies.get('membership')
    if not username:
        return redirect(url_for('login'))
    return render_template('profile.html', username=username, membership=membership)


@app.route('/vip')
def vip():
    membership = request.cookies.get('membership')
    if membership == 'premium':
        return render_template('vip.html', flag=flag)
    return "403 Forbidden: Access Denied", 403


if __name__ == '__main__':
    app.run(debug=True)
