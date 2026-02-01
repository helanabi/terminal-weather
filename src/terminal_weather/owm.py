# SPDX-License-Identifier: GPL-3.0-or-later

"""OpenWeatherMap related data and procedures."""

MAX_DAYS = 5

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
    elif field in ("dt", "visibility", "timezone"):
        return weather_dict.get(field)
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
    if field in ("timezone", "sunrise", "sunset"):
        return forecast_dict.get("city") and forecast_dict["city"].get(field)
