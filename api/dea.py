import sqlite3
import requests
from os import path
import json

cwd = path.dirname(__file__)
url = 'https://datos.comunidad.madrid/catalogo/dataset/35609dd5-9430-4d2e-8198-3eeb277e5282/resource/c38446ec-ace1-4d22-942f-5cc4979d19ed/download/desfibriladores_externos_fuera_ambito_sanitario.json'
con = sqlite3.connect(path.join(cwd, 'deas.db'))
deas_json_file = path.join(cwd, 'deas.json')


def load_data():
    if path.exists(deas_json_file):
        with open(deas_json_file) as f:
            print('Loading json file...')
            deas = json.load(f)
    else:
        try:
            deas = requests.get(url).json()
            print('DEAS successfully downloaded')
            with open(path.join(cwd, 'deas.json'), 'w') as f:
                json.dump(deas, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print('Error:', e)

    return deas


def generate_db_data(deas):
    db_data = map(lambda dea:(
        dea['codigo_dea'],
        dea['direccion_ubicacion'].title(),
        f"{dea['direccion_via_nombre']}, {dea['direccion_portal_numero']}".title(),
        int(dea['direccion_coordenada_x']),
        int(dea['direccion_coordenada_y'])), deas)

    return db_data


def populate_db(db_data):
    try:
        for dea in db_data:
            with con:
                con.execute('''INSERT INTO deas VALUES (?, ?, ?, ?, ?);''', (*dea,))
        print('All data saved in deas.db')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    with con:
        con.execute('DROP TABLE IF EXISTS deas;')
        con.execute('CREATE TABLE deas (id TEXT UNIQUE PRIMARY KEY, name TEXT, address TEXT, x REAL, y REAL);')
    deas = load_data().get('data')
    db_data = generate_db_data(deas)
    if deas:
        populate_db(db_data)