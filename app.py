import json
from datetime import datetime
from os import listdir
from os.path import join, dirname

from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/api/dangerZone')
def api_dz():
    with open('merged_points.json') as f:
        return jsonify(json.load(f))


@app.route('/api/v1/dangerZone/<position>')
def public_api_dz(position):
    with open('points.json') as f:
        return jsonify(json.load(f))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
