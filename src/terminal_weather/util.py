# SPDX-License-Identifier: GPL-3.0-or-later

"""Utility functions."""

import math
import re
import sys
import requests

from datetime import datetime
from . import owm
            
def get_location(conf):
    template = ("lat", "lon", "country_name", "country_code", "city")
    urls = conf("geoip-url")
    fields = conf("geoip-fields")

    if not urls:
        return

    for i in range(len(urls)):
        current_fields = tuple((f.strip() for f in fields[i].split(',')))
        if len(current_fields) != len(template):
            raise ValueError("invalid number of fields for geoip-url:",
                             urls[i])
        
        response = requests.get(urls[i])
        if response.ok:
            json = response.json()
            return dict(((key, json[field])
                         for key,field in zip(template,current_fields)))
        else:
            response.raise_for_status()
            
def prompt(question):
    answer = input(f"{question} ").lower()
    while answer not in ("yes", "no"):
        answer = input("Please answer with 'yes' or 'no':").lower()
    return answer

def guess_location(lookup, debug=False):
    """Try to find user's location coordinates.

    If succesfull, return a tuple of coordinates (latitude, longitude),
    otherwise return None.

    Positional argument:
    lookup -- a function that can lookup configuration entries
    debug -- enable debugging messages
    """
    try:
        location = get_location(lookup)
        if location:
            print(f"It appears that you are in {location["city"]},",
                  location["country_name"])
            
            if prompt("Is this your correct location? (yes/no):") == "yes":
                return (location["lat"], location["lon"])
    except Exception as e:
        if debug:
            print("guess_location:", e, file=sys.stderr)

def separate(csv):
    """Separate comma-separated values in a string.

    Return a tuple of Values stripped from whitespace characters
    before and after them.
    
    csv -- a string of comma-separated values.
    """
    return tuple(value.strip() for value in csv.split(','))

def error(msg, exit_code=2, prefix="Error: "):
    """Exit with an error message.

    print the provided error message to stderr and exit with the given
    status code.
    """
    print(prefix, msg, sep='', file=sys.stderr)
    sys.exit(exit_code)

def count_ts(day, interval=owm.INTERVAL):
    """Return the number of timestamps until last hour of a given day."""
    return math.ceil((23 - datetime.now().hour + day * 24) / interval)

def word_to_days(word, max_days=owm.MAX_DAYS):
    """Convert a word to a day range.

    Make a tuple of a single digit for a day number, or two digits for
    start-day and end-day of a day range
    
    word -- any valid argument string to parameter "when" (other than "now").
    """

    if word == "today":
        return (0,)
    if word == "tomorrow":
        return (1,)
    if word == "forecast":
        return (0, max_days)

    error('invalid value for parameter "when": ' + word, exit_code=3)

def parse_days(csv, max_days=owm.MAX_DAYS):
    """Parse and convert a string value passed to the argument "days".

    Make a tuple of two digits at most representing a day range.
    Invalid values cause the interpreter to exit with an error.

    csv -- str, representing a day number or a comma-separated range of days.
    """

    def fail(info=''):
        msg = 'invalid value of argument "days": ' + csv
        if info:
            msg += f"\n{info}"
        error(msg)

    if not re.match("^[0-9]*,?[0-9]*$", csv):
        fail()

    days = list(separate(csv))

    if len(days) == 2:
        if days[0] == '':
            days[0] = 0
        if days[1] == '':
            days[1] = max_days

    days= tuple(map(int, days))

    if len(days) == 2 and days[0] > days[1]:
        fail("First day must be less than or equal to second day")

    return days
