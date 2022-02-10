from urllib import response
from flask import Flask, request, make_response, redirect, render_template, flash, url_for
import requests
import sys
sys.path.append('/Users/kaos/workspace/CICE_Web/dea')
from auth import Auth

app = Flask(__name__)
app.secret_key = 't0p s3cr3t'
auth = Auth(request, 'http://localhost:3000/api/auth', 'http://localhost:5000/login', 'http://localhost:5000/secret')


@app.route('/login', methods=['GET', 'POST'])
@auth.authenticate
def login():
    res = make_response(render_template('login.html'))
    return res


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = None
    if request.method == 'POST':
        res = requests.post('http://localhost:3000/api/register', data=request.form).json()
        msg = res.get('msg')
        if res['success']:
            # requests.post to login?
            if msg:
                flash(msg, category='success')
            return redirect(url_for('login'))
    if msg:
        flash(msg, category='danger')
    return render_template('register.html')


@app.route('/secret')
@auth.authorize
def secret():
    return 'secret'


if __name__ == '__main__':
    app.run(debug=True, port=5000)