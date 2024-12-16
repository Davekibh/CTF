import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Route: Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Fetch URL Content
@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    if request.method == 'POST':
        url = request.form['url']
        try:
            # SSRF Vulnerability: Server fetches URL directly without validation
            response = requests.get(url)
            return render_template('fetch.html', content=response.text)
        except Exception as e:
            return f"Error fetching the URL: {e}"
    return render_template('fetch.html', content=None)

@app.route('/flag.txt')
def flag():
    return "CTF{SSRF_Exploit_Success}"
    

if __name__ == '__main__':
    app.run(debug=True)

