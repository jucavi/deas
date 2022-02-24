from flask import Flask, request, make_response, redirect, render_template, flash, url_for
import requests
from flask_cors import CORS
import os
import sys

path = os.getcwd()

sys.path.append(os.path.dirname(path))
from auth import Auth

app = Flask(__name__)
app.secret_key = 't0p s3cr3t'
CORS(app)
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
            return redirect(url_for('login'), code=307)
    if msg:
        flash(msg, category='danger')
    return render_template('register.html')


@app.route('/logout')
def logout():
    res = make_response(redirect(url_for('login')))
    res.set_cookie('token', '')
    res.set_cookie('id', '')
    return redirect(url_for('login'))


@app.route('/secret')
@auth.authorize
def secret():
    return '<h1>Secret</h1>'


@app.route('/')
@app.route('/finder', methods=['GET', 'POST'])
def finder():
    if request.method == 'POST':
        try:
            form = request.form
            res = requests.post('http://localhost:3000/api/deas', data=form).json()
            return res
            # return render_template('finder.html', deas=res['deas'])
        except Exception as e:
            print(e)
    return render_template('finder.html', deas=[])


@app.route('/<_>')
def missing(_):
    return url_for('finder')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
