# SPDX-License-Identifier: GPL-3.0-or-later

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

def get_field(owm_dict, field):
    """Find the value of a field in an OWM response dictionary."""
    if field == "desc":
        return owm_dict["weather"][0].get("description")
    elif field in ("temp",
                   "feels_like",
                   "temp_min",
                   "temp_max",
                   "pressure",
                   "humidity",
                   "sea_level",
                   "grnd_level"):
        return owm_dict["main"].get(field)
    elif field == "visibility":
        return owm_dict.get("visibility")
    elif field.startswith("wind_"):
        metric = field.split('_', maxsplit=1)[1]
        return owm_dict.get("wind") and owm_dict["wind"].get(metric)
    elif field == "rain":
        return owm_dict.get("rain") \
            and owm_dict["rain"].get("1h") \
            and f"{owm_dict["rain"]["1h"]} (1h)"
    elif field == "clouds":
        return owm_dict.get("clouds") and owm_dict["clouds"].get("all") 
    elif field in ("sunrise","sunset"):
        return owm_dict["sys"].get(field)
