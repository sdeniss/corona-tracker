import csv
import json

def read_csv(filename):
    result = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            place_name = row['label'].strip()
            location = row['position'].split(',')
            lat = float(location[0].strip())
            lon = float(location[1].strip())
            # TODO: Switch order to lat, lon in next version ;)
            location = lon, lat
            t_start = row['start time'].strip()
            t_end = row['end time'].strip()
            description = row['description'].strip()
            link = row['link'].strip()
            # TODO: Set radius in CSV file, not here
            result.append({"position": location,
                            "label": place_name,
                            "description": description,
                            "t_start": t_start,
                            "t_end": t_end,
                            "radius": 15,
                            "link": link})

    return result

with open('data/data.json', 'w', encoding='utf-8') as f:
    json.dump(read_csv('data/data.csv'), f, ensure_ascii=False, indent=4)
