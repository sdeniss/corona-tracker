import csv
import json
from datetime import date, datetime, timedelta, timezone

def get_points_from_csv():
    result = []
    with open('data/data.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            place_name = row['label'].strip()
            location = row['position'].split(',')
            lat = float(location[0].strip())
            lon = float(location[1].strip())
            # TODO: Switch order to lat, lon in next version ;)
            location = lon, lat
            # TODO: Deprecate t_start, t_end as we have unix timestamps
            t_start = row['start time'].strip()
            t_end = row['end time'].strip()
            t_start_unix_timestamp = datetime.fromisoformat(t_start).timestamp()
            t_end_unix_timestamp = datetime.fromisoformat(t_end).timestamp()
            date_end = str(datetime.fromisoformat(t_end).date())

            description = row['description'].strip()
            link = row['link'].strip()
            # TODO: Set radius in CSV file, not here
            result.append({"position": location,
                            "label": place_name,
                            "description": description,
                            "t_start": t_start,
                            "t_end": t_end,
                            "date_end": date_end,
                            "t_start_ts": t_start_unix_timestamp,
                            "t_end_ts": t_end_unix_timestamp,
                            "radius": 15,
                            "link": link})
    return result

              
def _textulize_visit_datetime(point):
    start = point['t_start']
    end = point['t_end']
    dt_start = datetime.fromisoformat(start)
    dt_end = datetime.fromisoformat(end)
    return '%s בין השעות %s-%s' % (dt_start.strftime('%d/%m'), dt_start.strftime('%H:%M'), dt_end.strftime('%H:%M'))


def _textulize_visit_time(point):
    start = point['t_start']
    end = point['t_end']
    dt_start = datetime.fromisoformat(start)
    dt_end = datetime.fromisoformat(end)
    return '%s-%s' % (dt_start.strftime('%H:%M'), dt_end.strftime('%H:%M'))


# Returns only points that are from last daysAgo days
def filter_points(points, daysAgo):
    daysAgoDate = datetime.now() - timedelta(days=daysAgo)
    daysAgoDate = daysAgoDate.timestamp()
    # We use end time to get all cases with time overlap
    return [p for p in points if daysAgoDate < p["t_end_ts"]]

# Merges points in the same location and adds a nice HTML description
def merge_points_original(points):
    visit_dict = {}
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
            point['description'] += '<li>' + _textulize_visit_datetime(p_)

        result.append(point)

    return result


# Merges points in the same location and adds a nice HTML description
def merge_points_by_date(points, daysAgo):
    if daysAgo is not None:
        points = filter_points(points, daysAgo)
    visit_dict = {}
    for point in points:
        pos = str(tuple(point['position'])) + str(point['date_end'])
        if pos not in visit_dict:
            visit_dict[pos] = [point]
        else:
            visit_dict[pos].append(point)

    result = []

    for points in visit_dict.values():
        point = dict(points[0])
        
        if len(points) > 1:
            point['description'] += '<br><br><b>שעות ביקור: </b><br>'
            for p_ in points:
                point['description'] += '<li>' + _textulize_visit_time(p_)
        else:
            point['description'] += '<br><br><b>שעות ביקור: </b>%s<br>' % _textulize_visit_time(point)

        result.append(point)

    return result


if __name__ == '__main__':
    points = get_points_from_csv()

    with open('data/data.json', 'w+', encoding='utf-8') as f:
        json.dump(points, f, ensure_ascii=False, indent=4)

    for daysAgo in range(15):
        with open('data/merged_data_%d.json' % daysAgo, 'w', encoding='utf-8') as f:
            result = merge_points_by_date(points, daysAgo)
            print(result)
            json.dump(result, f, ensure_ascii=False, indent=4)

    with open('data/merged_data_all.json', 'w', encoding='utf-8') as f:
        json.dump(merge_points_by_date(points, None), f, ensure_ascii=False, indent=4)

    with open('data/merged_data_all_original.json', 'w', encoding='utf-8') as f:
        json.dump(merge_points_original(points), f, ensure_ascii=False, indent=4)
