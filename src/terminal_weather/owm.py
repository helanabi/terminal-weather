# SPDX-License-Identifier: GPL-3.0-or-later

"""OpenWeatherMap related data and procedures."""

MAX_DAYS = 5 # maximum number of days in weather forecasts
INTERVAL = 3 # number of hours between weather data records

# todo: change to namedtuples
FIELDS = (
    # label, unit
    ("city", ''),
    ("desc", ''),
    ("temp", "temp"),
    ("feels_like", "temp"),
    ("temp_min", "temp"),
    ("temp_max", "temp"),
    ("pressure", "pressure"),
    ("humidity", "percent"),
    ("sea_level", "pressure"),
    ("grnd_level", "pressure"),
    ("visibility", "distance"),
    ("wind_speed", "speed"),
    ("wind_deg", "angle"),
    ("wind_gust", "speed"),
    ("rain", "volume"),
    ("clouds", "percent"),
    ("sunrise", ''),
    ("sunset", '')
)

UNITS = {
    # standard, metric, imperial
    "temp": ('K', "°C", "°F"),
    "pressure": ("hPa",)*3,
    "percent": ('%',)*3,
    "distance": ('m',)*3,
    "speed": ("m/s", "m/s", 'mph'),
    "angle": ('°',)*3,
    "volume": ("mm",)*3, # I know volume is 3D. It isn't my fault!
}

def list_fields():
    return tuple(map(lambda t: t[0], FIELDS))

def get_unit(field, sys):
    systems = ("standard", "metric", "imperial")
    unit_type = next(filter(lambda t: t[0] == field, FIELDS))[1]
    return unit_type and UNITS[unit_type][systems.index(sys)]

def grep_weather(weather_dict, field):
    """Find the value of a field in an OWM response dictionary."""
    if field == "desc":
        return weather_dict["weather"][0].get("description")
    elif field in ("temp",
                   "feels_like",
                   "temp_min",
                   "temp_max",
                   "pressure",
                   "humidity",
                   "sea_level",
                   "grnd_level"):
        return weather_dict["main"].get(field)
    elif field in ("dt", "visibility", "timezone"):
        return weather_dict.get(field)
    elif field.startswith("wind_"):
        metric = field.split('_', maxsplit=1)[1]
        return weather_dict.get("wind") and weather_dict["wind"].get(metric)
    # todo: process rain.3h
    elif field == "rain":
        return weather_dict.get("rain") \
            and weather_dict["rain"].get("1h") \
            and f"{weather_dict["rain"]["1h"]} (1h)"
    elif field == "clouds":
        return weather_dict.get("clouds") and weather_dict["clouds"].get("all") 
    elif field in ("sunrise","sunset"):
        return weather_dict["sys"].get(field)
    elif field == "city":
        return weather_dict.get("name")

def grep_forecast(forecast_dict, field):
    if field in ("timezone", "sunrise", "sunset"):
        return forecast_dict.get("city") and forecast_dict["city"].get(field)
    if field == "city":
        return forecast_dict.get("city", {}).get("name")
