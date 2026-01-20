# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import sys
import owmlib
from . import owm
from . import util

VERSION = "Terminal-weather version 0.1.0"
COPYRIGHT = """Copyright (C) 2026 Hassan El anabi
Terminal-weather comes with ABSOLUTELY NO WARRANTY.
You may redistribute copies of Terminal-weather
under the terms of the GNU General Public License.
For more information about these matters, see the file named COPYING."""

def parse_args():
    parser = argparse.ArgumentParser(
        prog="weather",
        description="Get current weather and forecasts for upcoming days"
    )

    parser.add_argument("when", nargs="?",
                        choices=["now", "forecast"],
                        help="show weather data for the specified time period"
                        " (default: forecast)")
    parser.add_argument("-c", "--conf", help="configuration file")
    parser.add_argument("-C", "--color", choices=["yes", "no"],
                        help="enable colored output (default: yes). "
                        "This option is ignored when -j/--json is used")
    parser.add_argument("-f", "--fields", help="specify a comma-separated list"
                        " of fields to show, or 'all' to show all fields. "
                        "Available fields are: desc, temp, feels_like, "
                        "temp_min, temp_max, pressure, humidity, sea_level, "
                        "grnd_level, visibility, wind_speed, wind_deg, "
                        "wind_gust, rain, clouds, sunrise, sunset.")
    parser.add_argument("-j", "--json", action="store_true",
                        help="show results in raw json format")
    parser.add_argument("-k", "--key", help="OpenWeatherMap API key")
    parser.add_argument("-u", "--units",
                        choices=["metric", "imperial", "standard"],
                        help="(default: metric)")
    parser.add_argument("-v", "--version", action="store_true",
                        help="show software version and copyright notice")

    ex_group = parser.add_mutually_exclusive_group()

    ex_group.add_argument("-g", "--geocoordinates",
                          help="geocoordintes of the form: latitude,longitude")
    ex_group.add_argument("-l", "--location",
                          help="a location of the format: city[,country]")

    args = parser.parse_args()
    return args

def prompt(question):
    answer = input(question).lower()
    while answer not in ("yes", "no"):
        answer = input("Please answer with 'yes' or 'no':").lower()
    return answer

def main():
    args = parse_args()
    if args.version:
        print(VERSION)
        print(COPYRIGHT)
        sys.exit(0)

    get_value = util.init_conf(args)

    api_keys = get_value("key")
    if not api_keys:
        util.error("unable to find any API keys", exit_code=3)

    location = None
    coords = None

    if args.geocoordinates:
        coords = args.geocoordinates
    elif args.location:
        location = args.location
    elif get_value("geocoordinates"):
        coords = get_value("geocoordinates")
    elif get_value("location"):
        location = args.location
    else:
        coords = util.guess_location(get_value)

    if not (coords or location):
        util.error("one of 'geocoordinates' or 'location' must be specified"
                   " to get the corresponding weather data")

    if not coords:
        location_parts = util.separate(location)
        if len(location_parts) > 2 or not location_parts[0]:
            util.error(f"invalid location string: {location}")

        try:
            geo_response = owmlib.geo_direct(
                location_parts[0],
                api_keys[-1],
                country=location_parts[1] if len(location_parts) == 2 else '',
                limit=1
            )
        except Exception as e:
            util.error(str(e), exit_code=9)

        coords = (geo_response[0]["lat"], geo_response[0]["lon"])

    else:
        coords = util.separate(coords)
        if len(coords) != 2:
            util.error(f"invalid geocoordinates string: {coords}")

    when = get_value("when")

    if when == "now":
        data_func = owmlib.weather
    else:
        data_func = owmlib.forecast

    try:
        weather_data = data_func(
            *coords,
            api_keys[-1],
            units=get_value("units")
        )
    except Exception as e:
        util.error(str(e), exit_code=9)

    if when == "forecast":
        print("Under development")
        sys.exit(0)

    fields_str = get_value("fields")

    if fields_str == "all":
        fields = owm.FIELDS
    else:
        fields = util.separate(fields_str)
        if not set(fields) <= set(owm.FIELDS):
            util.error("invalid fields: "
                       + ' '.join(set(fields) - set(owm.FIELDS)))

    delim = '\n'
    sep = ": "

    print(delim.join(
        sep.join((field, str(owm.get_field(weather_data, field)))) \
        for field in fields
    ))
