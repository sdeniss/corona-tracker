import csv


def read_csv(filename):
    result = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            place_name = row['label'].strip()
            location = row['position']
            location = row['position'].split(',')
            location = float(location[0].strip()), float(location[1].strip())
            t_start = row['start time'].strip()
            t_end = row['end time'].strip()
            descriptioin = row['description'].strip()
            link = row['link'].strip()
            # TODO: Set radius in CSV file, not here
            result.append({"position": location,
                            "label": place_name,
                            "description": descriptioin,
                            "t_start": t_start,
                            "t_end": t_end,
                            "radius": 15,
                            "link": link})

    return result

