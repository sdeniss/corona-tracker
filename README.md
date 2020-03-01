# Corona Tracker
This repository is the source code for: http://corona-tracker.com

## Vision
This project ais open to everyone to see, use, and contribute to.

**We mean to create a universal DB and standard for COVID-19 patient location tracking.**

Why?

The only way to prevent competing apps and platforms, each of which would have their own incomplete set of data points, would hinder the global fight against this potentially devastating threat to our health, economy and society as a whole.

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
    "t_start": 152947445,
    "t_end": 154847374,
    "label": "The Red Pirate",
    "description": "A tourist from Korea visited this location recently",
    "link": "https://www.cnn.com/article1234"
  }
]
```
