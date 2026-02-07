# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import json
import sys
import owmlib

from requests.exceptions import ConnectionError
from . import config
from . import output
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
    period_meg = parser.add_mutually_exclusive_group()
    period_meg.add_argument("when", nargs="?",
                        choices=["now", "today", "tomorrow", "forecast"],
                        help="show weather data for the specified time period"
                        f" (default: {config.DEFAULTS['when']})")
    parser.add_argument("-c", "--conf", help="configuration file")
    period_meg.add_argument("-d", "--days",
                            help="show weather forecasts for the specified "
                            "day or a range of the form: [start],[end]")
    parser.add_argument("-D", "--debug", action="store_true",
                        help="enable debugging messages")
    parser.add_argument("-f", "--fields",
                        help="specify a comma-separated list of fields to show"
                        f" (default: {config.DEFAULTS['fields']}), or 'all' to "
                        "show all fields. Available fields are: city, desc, "
                        "temp, feels_like, temp_min, temp_max, pressure, "
                        "humidity, sea_level, grnd_level, visibility, "
                        "wind_speed, wind_deg, wind_gust, rain, clouds, "
                        "sunrise, sunset")
    parser.add_argument("-j", "--json", action="store_true",
                        help="show results in raw json format")
    parser.add_argument("-k", "--key", help="OpenWeatherMap API key")
    parser.add_argument("-u", "--units",
                        choices=["metric", "imperial", "standard"],
                        help=f"(default: {config.DEFAULTS['units']})")
    location_meg = parser.add_mutually_exclusive_group()
    location_meg.add_argument("-g", "--geocoordinates",
                          help="geocoordintes of the form: latitude,longitude")
    location_meg.add_argument("-l", "--location",
                          help="a location of the form: city[,country]")
    parser.add_argument("-v", "--version", action="store_true",
                        help="show software version and copyright notice")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.version:
        print(VERSION)
        print(COPYRIGHT)
        sys.exit(0)

    get_value = config.init_conf(args)

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
        location = get_value("location")
    else:
        coords = util.guess_location(get_value, debug=get_value("debug"))
        if coords and \
           util.prompt("Would you like to save this location for future runs? "
                       "(yes/no):") == "yes":
            config.write_conf("geocoordinates", ','.join(map(str, coords)))

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
        if isinstance(coords, str):
            coords = util.separate(coords)
            if len(coords) != 2:
                util.error(f"invalid geocoordinates string: {coords}")

    fields_str = get_value("fields")
    all_fields = owm.list_fields()

    if fields_str == "all":
        fields = all_fields
    else:
        fields = util.separate(fields_str)
        if not set(fields) <= set(all_fields):
            util.error("invalid fields: "
                       + ' '.join(set(fields) - set(all_fields)))

    days = None
    
    if args.days:
        days = util.parse_days(args.days)
    elif args.when and args.when != "now":
        days = util.word_to_days(args.when)
    elif not args.when and get_value("days"):
        days = util.parse_days(get_value("days"))
    elif get_value("when") != "now":
        days = util.word_to_days(get_value("when"))

    units = get_value("units")
    api_params = { "units": units }
    format_params = { "sep": "\t", "field_delim": "\n", "units": units }

    if days:
        data_func = owmlib.forecast
        print_func = output.print_forecast
        format_params.update(ts_delim='\n---\n',
                             time_format=get_value("time-format"),
                             start_day=days[0],
                             end_day=days[-1])
        api_params["cnt"] = util.count_ts(days[-1])
    else:
        data_func = owmlib.weather
        print_func = output.print_ts

    try:
        weather_data = data_func(*coords, api_keys[-1], **api_params)

        if args.json:
            print(json.dumps(weather_data))
        else:
            print_func(weather_data, fields, **format_params)

    except Exception as e:
        util.error(f"An error occured while trying to fetch data.\n{e}",
                   exit_code=9,
                   prefix='')
