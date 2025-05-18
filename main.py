from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
CORS(app)

EXERCISES = [
    {
        'id': 1,
        'name': "Дифференциальные уравнения",
        'started_at': "2026-09-12T00:00:00",
        'time_spent': "2ч. 30мин.",
    },
    {
        'id': 2,
        'name': "Теоретическая механика",
        'started_at': "2026-10-18T00:00:00",
        'time_spent': "1ч. 45мин.",
    },
    {
        'id': 3,
        'name': "Квантовая физика",
        'started_at': "2026-11-05T00:00:00",
        'time_spent': "2ч. 00мин.",
    },
    {
        'id': 4,
        'name': "Органическая химия",
        'started_at': "2026-09-22T00:00:00",
        'time_spent': "1ч. 15мин.",
    },
    {
        'id': 5,
        'name': "Теория вероятностей",
        'started_at': "2026-10-30T00:00:00",
        'time_spent': "1ч. 50мин.",
    },
    {
        'id': 6,
        'name': "Микроэкономика",
        'started_at': "2026-11-14T00:00:00",
        'time_spent': "1ч. 30мин.",
    },
    {
        'id': 7,
        'name': "Структуры данных",
        'started_at': "2026-12-08T00:00:00",
        'time_spent': "2ч. 20мин.",
    },
    {
        'id': 8,
        'name': "Философия науки",
        'started_at': "2026-09-25T00:00:00",
        'time_spent': "1ч. 00мин.",
    },
    {
        'id': 9,
        'name': "Биохимия",
        'started_at': "2026-10-11T00:00:00",
        'time_spent': "2ч. 10мин.",
    },
    {
        'id': 10,
        'name': "История искусств",
        'started_at': "2026-12-03T00:00:00",
        'time_spent': "1ч. 25мин.",
    }
]

URLS = []


@app.route("/exercises", methods=['GET', 'OPTIONS'])
def get_exercises_all():
    sort = request.args.get('sort')
    exercises = EXERCISES.copy()

    if sort in ('asc', 'desc'):
        exercises.sort(
            key=lambda x: datetime.fromisoformat(x['started_at']),
            reverse=(sort == 'desc')
        )

    return jsonify(exercises)


@app.route("/exercises/<int:exercise_id>", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_exercises_single(exercise_id):
    exercise = {}
    for item in EXERCISES:
        if item['id'] == exercise_id:
            exercise = item

    if 'id' in exercise:
        return jsonify(exercise)
    else:
        return abort(404)


@app.route("/exercises", methods=['POST', 'OPTIONS'])
@cross_origin()
def create_new_exercise():
    new_exercise = {
        'id': len(EXERCISES) + 1,
        'name': request.json['name'],
        'started_at': datetime.datetime.now().isoformat(),
        'time_spent': ''
    }

    print('new_exercise => ', new_exercise)

    EXERCISES.append(new_exercise)

    print('exercises => ', EXERCISES)

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
