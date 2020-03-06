import csv
import json

# Returns true if json was updated
def update_json(json_filename):
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


    previous_data = ''
    try:
        with open(json_filename, 'r') as f:
            previous_data = f.read()
    except FileNotFoundError:
        # Do nothing
        pass

               
    with open(json_filename, 'w+', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    # Compare current to previous
    current_data = ''
    with open(json_filename, 'r') as f:
        current_data = f.read()
    
    if (current_data == previous_data):
        print("No changes to " + json_filename)
        return False
    else:
        print("There were changes to " + json_filename)
        return True

if __name__ == '__main__':
    update_json('data/data.json')


