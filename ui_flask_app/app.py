from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        url = request.form['url']
       
        result = subprocess.getoutput(f"echo '{url}' | python3 ../scanner.py")
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

