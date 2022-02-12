from flask import Flask, request, make_response, redirect, render_template, flash, url_for
import requests
import sys
sys.path.append('/Users/kaos/workspace/CICE_Web/dea')
from auth import Auth
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = 't0p s3cr3t'
CORS(app, supports_credentials=True)
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
            # if msg:
            #     flash(msg, category='success')
            # return redirect(url_for('login'))
    if msg:
        flash(msg, category='danger')
    return render_template('register.html')


@app.route('/logout')
def logout():
    res = make_response(redirect(url_for('login')))
    res.set_cookie('token', '')
    res.set_cookie('id', '')

    return res


@app.route('/secret')
@auth.authorize
def secret():
    return '<h1>Secret</h1>'


@app.route('/deas', methods=['GET', 'POST'])
@cross_origin(methods=['POST'], expose_headers='*')
def deas():
    if request.method == 'POST':
        print(request.form)
        print(request.args)
        print(request.get_json())
        print(request.data)
        # lat, long = form['lat'], form['long']
    return render_template('deas.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)