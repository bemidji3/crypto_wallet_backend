#!/usr/bin/env python3
from flask import Flask, request, send_file
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

with open('.secret', 'r') as f:
    secrets = json.loads(f.read())
    api_key = secrets['api_key']


@app.route('/new-user', methods=['POST'])
def user_create():
    my_request = request.get_json()

    print(my_request)

    res = False

    if my_request['api_key'] == api_key:
        db_entry = build_db_entry(my_request)
        res = write_to_file(db_entry)

    if res:
        return json.loads('{ "status": 200 }')
    else:
        return json.loads('{ "status" : 400, "error" : "api_key" }')


@app.route('/get-user-stats', methods=['POST'])
def get_user_stats():
    my_request = request.get_json()
    print(my_request)

    if my_request['api_key'] == api_key:
        return send_file('db/db.txt', attachment_filename='database.txt')
    else:
        return json.loads('{ "status" : 400, "error" : "api_key" }')


def write_to_file(my_request):
    print('writing to file')
    with open("db/db.txt", "a") as my_file:
        my_file.write(str(my_request) + ",\n")
    return True


def build_db_entry(my_request):
    db_entry = {'first_name': my_request['first_name'], 'last_name': my_request['last_name'],
                'email': my_request['email'], 'timestamp': my_request['timestamp']}

    return str(db_entry)


if __name__ == '__main__':
    app.run()
