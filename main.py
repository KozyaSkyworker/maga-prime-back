from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import datetime
import sqlite3

DB_NAME = 'my_database.db'

app = Flask(__name__)
CORS(app)


@app.route("/exercises", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_exercises_all():
    sort = request.args.get('sort') or 'desc'

    con = sqlite3.connect(DB_NAME)
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
            'stopped_at': exercise[3],
            'time_spent': exercise[4],
            'name': exercise[5],
            'status': exercise[6],
            'user_id': exercise[7],
        }
        exercises.append(temp_exercise)

    return jsonify(exercises)


@app.route("/exercises/<int:exercise_id>", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_exercises_single(exercise_id):
    con = sqlite3.connect(DB_NAME)

    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cursor.execute("SELECT * FROM Exercise WHERE id = ?", (exercise_id,))
    exercise = cursor.fetchone()

    if not exercise:
        return abort(404)

    exercise_dict = dict(exercise)

    cursor.execute(
        "SELECT id, url, title, exercise_id, is_relevant, description FROM Url WHERE exercise_id = ? GROUP BY url",
        (exercise_id,))
    urls = cursor.fetchall()
    urls_list = [dict(url) for url in urls]

    con.close()

    result = {
        "exercise": exercise_dict,
        "urls": urls_list
    }

    return jsonify(result), 200


@app.route("/exercises", methods=['POST', 'OPTIONS'])
@cross_origin()
def create_new_exercise():
    con = sqlite3.connect(DB_NAME)
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
        'stopped_at': result[3],
        'time_spent': result[4],
        'name': result[5],
        'status': result[6],
        'user_id': result[7],
    }

    return jsonify({'data': new_exercise, 'status': 201}), 201


@app.route("/exercises/<int:exercise_id>", methods=['PATCH', 'OPTIONS'])
@cross_origin()
def update_exercise(exercise_id):
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()

    exercise_values = (int(request.json['status']), datetime.datetime.now(), int(exercise_id))
    sql = None

    if int(request.json['status']) == 2:  # start
        sql = 'UPDATE Exercise SET status = ?, started_at = ? WHERE id = ?'

    if int(request.json['status']) == 3:  # stop
        sql = 'UPDATE Exercise SET status = ?, stopped_at = ? WHERE id = ?'

    cursor.execute(sql, exercise_values)

    con.commit()

    cursor.execute('SELECT * from Exercise ORDER BY id DESC')

    result = cursor.fetchone()

    con.close()

    updated_exercise = {
        'id': result[0],
        'created_at': result[1],
        'started_at': result[2],
        'stopped_at': result[3],
        'time_spent': result[4],
        'name': result[5],
        'status': result[6],
        'user_id': result[7],
    }

    return jsonify({'data': updated_exercise, 'status': 200}), 200


@app.route("/exercises/<int:exercise_id>", methods=['DELETE', 'OPTIONS'])
@cross_origin()
def delete_exercise(exercise_id):
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()

    cursor.execute('DELETE FROM Exercise WHERE id = ?', (int(exercise_id),))

    con.commit()

    con.close()

    return jsonify({'data': f"{exercise_id} deleted", 'status': 200}), 200


@app.route("/urls", methods=['POST', 'OPTIONS'])
@cross_origin()
def save_url_data_to_db():
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()

    new_url_insert = (datetime.datetime.now(), request.json['url'], request.json['title'], request.json['visited_at'],
                      request.json['exercise_id'])

    cursor.execute('INSERT INTO Url (created_at, url, title, visited_at, exercise_id ) VALUES (?, ?, ?, ?, ?)',
                   new_url_insert)

    con.commit()

    cursor.execute('SELECT * from Url ORDER BY id DESC')

    result = cursor.fetchone()

    con.close()

    new_url = {
        'id': result[0],
        'created_at': result[1],
        'visited_at': result[2],
        'time_spent': result[3],
        'url': result[4],
        'title': result[5],
        'exercise_id': result[8],
    }

    return jsonify({'data': new_url, 'status': 201}), 201


@app.route("/urls", methods=['PATCH', 'OPTIONS'])
@cross_origin()
def update_urls():
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()

    # https://dev.to/chidioguejiofor/scenario-1-making-updates-to-multiple-fields-56hl

    # exercise_values = (int(request.json['status']), int(exercise_id))
    #
    # cursor.execute('UPDATE Url SET status = ? WHERE id = ?', exercise_values)

    con.commit()

    con.close()

    return jsonify({'data': 'urls updated', 'status': 200}), 200


if __name__ == '__main__':
    app.run(debug=True)
