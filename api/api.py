from crypt import methods
import db
from flask import Flask, request
import uuid
from flask_cors import CORS
import utm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)

def check_password(user, password):
    try:
        return check_password_hash(user['password'], password)
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


def create_user(email, password):
    with db.get_db() as con:
        con.execute('INSERT INTO user VALUES (?, ?, ?, ?);', (str(uuid.uuid4()), email, generate_password_hash(password), None))
        # con.commit()

def get_deas():
    with db.get_db() as con:
        return con.execute('SELECT * FROM dea;').fetchall()


@app.route('/api')
def api():
    return 'api'


@app.route('/api/auth', methods=['GET', 'PUT'])
def auth():
    if request.method == 'PUT':
        email = request.form.get('email')
        password = request.form.get('password')
        token = request.form.get('token')
        user = get_user(email)
        if not user:
            return {'success': False, 'cookie': {}, 'msg': 'User not found.'}

        if check_password(user, password):
            set_token(user['id'], token)
            return {'success': True, 'cookie': {'id': user['id'], 'token': token}}

        return {'success': False, 'cookie': {}, 'msg': 'Incorrect password.'}


    elif request.method == 'GET':
        db_token = get_token(request.form.get('id'))
        if db_token:
            return {'success': db_token['token'] == request.form.get('token')}

        return {'success': False}


@app.route('/api/register', methods=['POST'])
def register():
    msg = None
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        msg = 'Email required.'
    if not password:
        msg = 'Password required.'

    if not msg:
        create_user(email, password)
        return {'success': True, 'msg': 'User successfully created!'}
    return {'success': False, 'msg': msg}


@app.route('/api/deas', methods=['POST'])
def deas():
    try:
        form = request.form
        lat, long = float(form['lat']), float(form['lon'])
        size = int(form['size'])
        deas = get_deas()
    except:
        pass
    else:
        if deas:
            deas_by_distance = []
            for dea in deas:
                pos_x, pos_y, *_ = utm.from_latlon(lat, long)
                dea_x, dea_y = dea['x'], dea['y']
                distance = ((pos_x - dea_x) ** 2 + (pos_y - dea_y) ** 2) ** .5
                deas_by_distance.append([*tuple(dea)[:3], distance])
            deas_by_distance.sort(key=lambda x: x[-1])
            return {'success': True, 'deas': deas_by_distance[:size]}
    return {'success': False, 'deas': []}


if __name__ == '__main__':
    app.run(debug=True, port=3000)