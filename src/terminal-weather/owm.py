# SPDX-License-Identifier: GPL-3.0-or-later

from functools import partial

FIELDS = (
    "desc",
    "temp",
    "feels_like",
    "temp_min",
    "temp_max",
    "pressure",
    "humidity",
    "sea_level",
    "grnd_level",
    "visibility",
    "wind_speed",
    "wind_deg",
    "wind_gust",
    "rain",
    "clouds",
    "sunrise",
    "sunset"
)

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
    elif field == "visibility":
        return weather_dict.get("visibility")
    elif field.startswith("wind_"):
        metric = field.split('_', maxsplit=1)[1]
        return weather_dict.get("wind") and weather_dict["wind"].get(metric)
    elif field == "rain":
        return weather_dict.get("rain") \
            and weather_dict["rain"].get("1h") \
            and f"{weather_dict["rain"]["1h"]} (1h)"
    elif field == "clouds":
        return weather_dict.get("clouds") and weather_dict["clouds"].get("all") 
    elif field in ("sunrise","sunset"):
        return weather_dict["sys"].get(field)

def grep_forecast(forecast_dict, field):
    if field in ("sunrise", "sunset"):
        return forecast_dict.get("city") and forecast_dict["city"].get(field)

def print_ts(weather_dict,
             fields,
             sep,
             field_delim,
             end='\n',
             lookup=grep_weather):
    """Extract and print specific fields from a weather dictionary."""

    print(field_delim.join(
        sep.join((field, str(lookup(weather_dict, field)))) \
        for field in fields
    ), end=end)

def print_forecast(forecast_dict, fields, sep, field_delim, ts_delim):
    """Extract and print a list of weather timestamps for specific fields."""

    # Separate daylight fields
    daylight_fields = tuple(f for f in ("sunrise", "sunset") if f in fields)
    fields = tuple(f for f in fields if f not in daylight_fields)
    
    print_data = partial(print_ts, sep=sep, field_delim=field_delim)

    if not forecast_dict.get("list"):
        return

    timestamps = forecast_dict["list"]
    for i, ts in enumerate(timestamps):
        print_data(ts, fields, end='')
        if i < len(timestamps) - 1:
            print(ts_delim, end='')

    if daylight_fields:
        if timestamps:
            print(ts_delim, end='')
        daylight_data = dict(
            (f, grep_forecast(forecast_dict, f)) for f in daylight_fields
        )
        print_data(daylight_data,
                 daylight_fields,
                 lookup=lambda d,k: d.get(k),
                 end='')
    print()
