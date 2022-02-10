from flask import Flask, request, make_response, redirect, render_template
from functools import wraps
import requests
import sys
sys.path.append('/Users/kaos/workspace/CICE_Web/dea')
from auth import Auth

app = Flask(__name__)
auth = Auth(request, 'http://localhost:3000/api/auth', 'http://localhost:5000/login', 'http://localhost:5000/secret')


@app.route('/login', methods=['GET', 'POST'])
@auth.authenticate
def login():
    res = make_response(render_template('login.html'))
    return res


@app.route('/secret')
@auth.authorize
def secret():
    return 'secret'


if __name__ == '__main__':
    app.run(debug=True, port=5000)