import json
from datetime import datetime
from os import listdir
from os.path import join, dirname

from flask import Flask, render_template, jsonify

from csv2json import update_json

app = Flask(__name__)


def check():
    assert not update_json('data/data.json'), "data/data.json is not up-to-date. Please run python3 csv2json.py"


check()


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/api/dangerZone')
def api_dz():
    points = []
    with open('data/merged_data_all_original.json') as f:
        points = json.load(f)
    return jsonify(list(points))


@app.route('/api/v1/dangerZone/<position>')
def public_api_dz(position):
    with open('data/data.json') as f:
        points = json.load(f)
    return jsonify(list(points))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
