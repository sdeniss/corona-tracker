# Corona Tracker
This repository is the source code for: http://corona-tracker.com

## Vision
This project aims open to everyone to see, use, and contribute to.

**We mean to create a universal DB and standard for COVID-19 patient location tracking.**

Why?

This is the only way to prevent competing apps and platforms, each of which would have their own incomplete set of data points, which would hinder the global fight against this potentially devastating threat to our health, economy and society as a whole.

So here's our first try at an API.

## About
This is a Flask+AngularJS webapp to track the locations that newly discovered COVID-19 patients have visited, so users can self-quarantine if they have come in contact with them.

The data is loaded from CSV files in *data/* at the moment due to time constraints. Will switch to a db later.

## API
There's only one request now. We will expand the API in the coming weeks.

#### DangerZone
Get a list of all places corona patients have visited within a radius of a certain point.


###### Request

`GET /api/v1/dangerZone/{latitude},{longitude}?radius={radius}`

Where:
 * `{latitude}`, `{longitde}` are the geolocation
 * `{radius}` is the range in KM from this point where points are returned.
 
###### Response
A list of points in the following format:

```json
[
  {
    "position": [31.2473, 32.4626],
    "t_start": "2020-02-22T11:00:00+02:00",
    "t_end": "2020-02-22T13:00:00+02:00",
    "label": "The Red Pirate",
    "description": "A tourist from Korea visited this location recently",
    "link": "https://www.cnn.com/article1234"
  }
]
```

## Static data
We also have static data you can copy under `data` folder.
It's organized by date: `merged_data_8` is for all cases that happened in the last 8 days.
If the same location exact had multiple cases, they are merged and their description shows all of them.



Try in here: http://corona-tracker.com/api/v1/dangerZone/32,31?radius=3000