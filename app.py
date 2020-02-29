import json
from datetime import datetime

from flask import Flask, render_template, jsonify

from csv2json import read_csv

app = Flask(__name__)


with open('data.json', 'w') as f:
    json.dump(read_csv('data.csv'), f)


@app.route('/')
def hello_world():
    return render_template('main.html')


def _textulize_visit_time(point):
    start = point['t_start']
    end = point['t_end']
    dt_start = datetime.fromisoformat(start)
    dt_end = datetime.fromisoformat(end)
    return '%s בין השעות %s-%s' % (dt_start.strftime('%d/%m'), dt_start.strftime('%H:%M'), dt_end.strftime('%H:%M'))


@app.route('/api/dangerZone')
def api_dz():
    visit_dict = {}
    with open('data.json') as f:
        points = json.load(f)
        for point in points:
            pos = tuple(point['position'])
            if pos not in visit_dict:
                visit_dict[pos] = [point]
            else:
                visit_dict[pos].append(point)

    result = []

    for points in visit_dict.values():
        point = dict(points[0])
        point['description'] += '<br><br><b>שעות ביקור:</b><br>'

        for p_ in points:
            point['description'] += '<li>' + _textulize_visit_time(p_)

        result.append(point)

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
