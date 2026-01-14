#!/usr/bin/env python

import argparse
import os
import sys

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
    parser.add_argument("when", nargs="?", default="today",
                        choices=["now", "today", "tomorrow", "forecast"],
                        help="show weather data for the specified time period"
                        " (default: today)")
    parser.add_argument("-c", "--conf", help="configuration file")
    parser.add_argument("-C", "--color", default="yes", choices=["yes", "no"],
                        help="enable colored output (default: yes). "
                        "This option is ignored when -j/--json is used")
    parser.add_argument("-f", "--fields", help="specify a comma-separated list"
                        " of fields to show, or 'all' to show all fields. "
                        "Available fields are: feels_like, uvi, wind, humidity"
                        ", pressure, daylight")
    parser.add_argument("-j", "--json", action="store_true",
                        help="show results in raw json format")
    parser.add_argument("-k", "--key", help="OpenWeatherMap API key")
    parser.add_argument("-l", "--location",
                        help="must be in the format: city[,country]")
    parser.add_argument("-u", "--units", default="metric",
                        choices=["metric", "imperial", "standard"],
                        help="(default: metric)")
    parser.add_argument("-v", "--version", action="store_true",
                        help="show software version and copyright notice")
    args = parser.parse_args()
    return args

def main(args):
    if args.version:
        print(VERSION)
        print(COPYRIGHT)
        sys.exit(0)

if __name__ == "__main__":
    main(parse_args())
