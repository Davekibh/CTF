from flask import Flask, request, render_template

app = Flask(__name__, static_folder='static')


# Route: Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Search Page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        return render_template('result.html', query=query)
    return render_template('search.html')

# Route: Flag (Accessible via directory traversal or XSS exploit)
@app.route('/static/flag.txt')
def flag():
    return "CTF{Outdated_Component_Flag}"

if __name__ == '__main__':
    app.run(debug=True)
