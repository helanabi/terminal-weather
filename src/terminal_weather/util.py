# SPDX-License-Identifier: GPL-3.0-or-later

"""Utility functions."""

import math
import requests
import sys

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

def count_ts(day=owm.MAX_DAYS):
    """Return the number of timestamps until last hour of a given day.

    timestamps are spaced with 3-hour intervals. Counting starts from the last
    hour, and continues until the last hour of the given day.

    day -- int, 0 means today, each successive day is 1 greater.
    """
    # todo: implement function

    return 3
    
    # now = datetime.now()
    # next_day = { # each day ends at 00:00 of the next day 
    #     "today": now.day+1,
    #     "tomorrow": now.day+2
    # }

    # if end not in next_day:
    #     return

    # # todo: fix month boundary bug (e.i. today=30)
    # delta = datetime(now.year, now.month, next_day[end], 0, 0) - now
    # return math.ceil(delta.total_seconds() / 3600 / 3)

def word_to_days(word):
    """Convert a word to a day range.

    Make a tuple of a single digit for a day number, or two digits for
    start-day and end-day of a day range
    
    word -- any valid argument string to parameter "when"
    """
    # todo: implement function

    if word == "today":
        return (0,)
    else:
        return (1,)

def parse_days(csv):
    """Parse and convert a string value passed to the argument "days".

    Make a tuple of two digits at most, from a string representing a day number
    or a comma-separated range of days. Empty strings become None, and invalid
    values cause the interpreter to exit with an error.
    """
    # todo: implement function
    return (2,3)
