import db
from flask import Flask, request, make_response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sys

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)

def check_password(user, password):
    try:
        # return check_password_hash(user['password'], password)
        return user['password'] == password
    except:
        return False

def get_user(email):
    with db.get_db() as con:
        return con.execute('SELECT * FROM user WHERE email=?', (email, )).fetchone()


def set_token(_id, token):
    with db.get_db() as con:
        con.execute('UPDATE user SET token=? WHERE id=?;', (token, _id))
        con.commit()

def get_token(_id):
    with db.get_db() as con:
        return con.execute('SELECT token FROM user WHERE id=?', (_id, )).fetchone()

@app.route('/api')
def api():
    return 'api'


@app.route('/api/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        token = request.form.get('token')
        user = get_user(email)
        if not user:
            return {'success': False}

        if check_password(user, password):
            set_token(user['id'], token)
            return {'success': True, 'cookie': {'id': user['id'], 'token': token}}

        return {'success': False}

    elif request.method == 'GET':
        db_token = get_token(request.form.get('id'))
        if db_token:
            return {'success': db_token['token'] == request.form.get('token')}

        return {'success': False}


if __name__ == '__main__':
    app.run(debug=True, port=3000)