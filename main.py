from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import datetime
import sqlite3

con = sqlite3.connect('my_database.db')
cursor = con.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS User
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                created_at DEFAULT TIMESTAMP,
                first_name TEXT NOT NULL, 
                sur_name TEXT NOT NULL, 
                last_name TEXT, 
                role INTEGER,
                is_deleted INTEGER,
                username TEXT,
                password TEXT)
            """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Exercise
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                created_at TIMESTAMP,
                started_at TIMESTAMP,
                time_spent TEXT,
                name TEXT NOT NULL, 
                status INTEGER DEFAULT 1,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)  REFERENCES User (id))
            """)

con.commit()
con.close()

app = Flask(__name__)
CORS(app)

EXERCISES = [
    {
        'id': 1,
        'name': "Дифференциальные уравнения",
        'started_at': "2026-09-12T00:00:00",
        'time_spent': "2ч. 30мин.",
        'status': 1
    },
    {
        'id': 2,
        'name': "Теоретическая механика",
        'started_at': "2026-10-18T00:00:00",
        'time_spent': "1ч. 45мин.",
        'status': 2
    },
    {
        'id': 3,
        'name': "Квантовая физика",
        'started_at': "2026-11-05T00:00:00",
        'time_spent': "2ч. 00мин.",
        'status': 3
    },
    {
        'id': 4,
        'name': "Органическая химия",
        'started_at': "2026-09-22T00:00:00",
        'time_spent': "1ч. 15мин.",
        'status': 3
    },
    {
        'id': 5,
        'name': "Теория вероятностей",
        'started_at': "2026-10-30T00:00:00",
        'time_spent': "1ч. 50мин.",
        'status': 3
    },
    {
        'id': 6,
        'name': "Микроэкономика",
        'started_at': "2026-11-14T00:00:00",
        'time_spent': "1ч. 30мин.",
        'status': 3
    },
    {
        'id': 7,
        'name': "Структуры данных",
        'started_at': "2026-12-08T00:00:00",
        'time_spent': "2ч. 20мин.",
        'status': 3
    },
    {
        'id': 8,
        'name': "Философия науки",
        'started_at': "2026-09-25T00:00:00",
        'time_spent': "1ч. 00мин.",
        'status': 3
    },
    {
        'id': 9,
        'name': "Биохимия",
        'started_at': "2026-10-11T00:00:00",
        'time_spent': "2ч. 10мин.",
        'status': 3
    },
    {
        'id': 10,
        'name': "История искусств",
        'started_at': "2026-12-03T00:00:00",
        'time_spent': "1ч. 25мин.",
        'status': 3
    }
]

URLS = []


@app.route("/exercises", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_exercises_all():
    sort = request.args.get('sort') or 'desc'

    con = sqlite3.connect('my_database.db')
    cursor = con.cursor()

    cursor.execute(f'SELECT * FROM Exercise ORDER BY id {sort}')

    result = cursor.fetchall()

    con.close()

    exercises = []
    for exercise in result:
        temp_exercise = {
            'id': exercise[0],
            'created_at': exercise[1],
            'started_at': exercise[2],
            'time_spent': exercise[3],
            'name': exercise[4],
            'status': exercise[5],
            'user_id': exercise[6],
        }
        exercises.append(temp_exercise)

    return jsonify(exercises)


@app.route("/exercises/<int:exercise_id>", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_exercises_single(exercise_id):
    con = sqlite3.connect('my_database.db')
    cursor = con.cursor()

    cursor.execute('SELECT * from Exercise WHERE id = ?', (int(exercise_id),))

    result = cursor.fetchone()

    con.close()

    if result:
        exercise = {
            'id': result[0],
            'created_at': result[1],
            'started_at': result[2],
            'time_spent': result[3],
            'name': result[4],
            'status': result[5],
            'user_id': result[6],
        }

        return jsonify(exercise)
    else:
        return abort(404)


@app.route("/exercises", methods=['POST', 'OPTIONS'])
@cross_origin()
def create_new_exercise():
    con = sqlite3.connect('my_database.db')
    cursor = con.cursor()

    new_exercise_insert = (request.json['name'], request.json['user_id'], datetime.datetime.now())

    cursor.execute('INSERT INTO Exercise (name, user_id, created_at) VALUES (?, ?, ?)', new_exercise_insert)

    con.commit()

    cursor.execute('SELECT * from Exercise ORDER BY id DESC')

    result = cursor.fetchone()

    con.close()

    new_exercise = {
        'id': result[0],
        'created_at': result[1],
        'started_at': result[2],
        'time_spent': result[3],
        'name': result[4],
        'status': result[5],
        'user_id': result[6],
    }

    return jsonify({'data': new_exercise, 'status': 201}), 201


@app.route("/urls", methods=['POST', 'OPTIONS'])
@cross_origin()
def save_url_data_to_db():
    new_url = {
        'id': len(URLS) + 1,
        'url': request.json['url'],
        'is_relevant': request.json['is_relevant'],
        'exercise_id': 1
    }

    print('new url => ', new_url)

    URLS.append(new_url)

    print('urls => ', URLS)

    return jsonify({'new_url': new_url}), 201


if __name__ == '__main__':
    app.run(debug=True)
