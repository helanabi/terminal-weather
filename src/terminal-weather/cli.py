import argparse
import sys
from . import util

VERSION = "Terminal-weather 0.1.0"
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
                        choices=["now", "today", "tomorrow", "forecast"],
                        help="show weather data for the specified time period"
                        " (default: today)")
    parser.add_argument("-c", "--conf", help="configuration file")
    parser.add_argument("-C", "--color", choices=["yes", "no"],
                        help="enable colored output (default: yes). "
                        "This option is ignored when -j/--json is used")
    parser.add_argument("-f", "--fields", help="specify a comma-separated list"
                        " of fields to show, or 'all' to show all fields. "
                        "Available fields are: feels_like, uvi, wind, humidity"
                        ", pressure, daylight")
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
        print("Error: unable to find an API key", file=sys.stderr)
        sys.exit(3)

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
        print("Error: one of 'geocoordinates' or 'location' must be specified"
              " to get the corresponding weather data", file=sys.stderr)
        sys.exit(2)
