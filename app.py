import json
from datetime import datetime
from os import listdir
from os.path import join, dirname

from flask import Flask, render_template, jsonify

import csv2json

app = Flask(__name__)

points = []
merged_points = []

def load():
    global points
    global merged_points
    points = csv2json.get_points_from_csv()
    merged_points = csv2json.merge_points_original(points)


load()


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/api/dangerZone')
def api_dz():
    global merged_points
    return jsonify(list(merged_points))


@app.route('/api/v1/dangerZone/<position>')
def public_api_dz(position):
    global points
    return jsonify(list(points))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
