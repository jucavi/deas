import secrets
from functools import wraps
import requests
from flask import make_response, redirect

class Auth:
    def __init__(self, request, api_uri, login_uri, redirect_uri):
        self.request = request
        self.api_uri = api_uri
        self.login_uri = login_uri
        self.redirect_uri = redirect_uri

    @property
    def token(self):
        return secrets.token_hex()


    def authenticate(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)

            if self.request.method == 'POST':
                dic_form = dict(self.request.form)
                dic_form['token'] = self.token

                res_api = requests.put(self.api_uri, data=dic_form).json()
                if res_api['success']:
                    res = make_response(redirect(self.redirect_uri))
                    res.set_cookie('token', res_api['cookie']['token'])
                    res.set_cookie('id', res_api['cookie']['id'])

            return res
        return wrapper


    def authorize(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.request.method == 'GET':
                res_api = requests.get(self.api_uri, data=self.request.cookies).json()
                if res_api['success']:
                    return func(*args, **kwargs)
            return redirect(self.login_uri)
        return wrapper
