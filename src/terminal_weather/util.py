# SPDX-License-Identifier: GPL-3.0-or-later

"""Configuration management and other utility functions."""

import math
import os
import re
import requests
import sys

from datetime import datetime

CONF_FILE = None # automatically set by init_conf()
CONF_SPEC = {
    "cumulative": ("geoip-url", "geoip-fields", "key"),
    "singleton": (
        "location",
        "geocoordinates",
        "when",
        "color",
        "fields",
        "units",
        "debug",
        "json"
    )
}

DEFAULTS = {
    "when": "now",
    "color": "yes",
    "fields": "desc,temp",
    "units": "metric"
}

def store_line(spec, conf, line):
    key, value = (s.strip() for s in line.split(sep="=", maxsplit=1))
    cumulative = False

    category = tuple(category for category in spec
                if key in spec[category])

    if not category:
        print("Error: unrecognized configuration variable:",
              key,
              file=sys.stderr)
        sys.exit(3)

    if category[0] == "cumulative":
        cumulative = True

    old_value = conf.get(key)
    if old_value == None:
        conf[key] = [value] if cumulative else value
    elif isinstance(old_value, list) and cumulative:
        old_value.append(value)
    elif not isinstance(old_value, list) and cumulative:
        raise ValueError("cumulative variable stores a non-list value:", key)
    elif not cumulative:
        print("Error: multiple values were assigned to non-cumulative "
              "configuration variable:",
              key,
              file=sys.stderr)
        sys.exit(3)

def parse_conf(path, conf_spec):
    conf = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if not re.search('^[a-z]+(-[a-z]+)*=', line):
                    print("Error: invalid configuration entry:" + entry,
                          file=sys.stderr)
                    sys.exit(3)
                store_line(conf_spec, conf, line)
    except Exception as e:
        error(f"An error occured while reading configuration file\n{e}",
              exit_code=1,
              prefix='')

    return lambda name: conf.get(name)
    
def resolve_cf(args):
    def mkfile(*name_parts):
        if not all(name_parts):
            return False
        name = os.path.join(*name_parts)
        return os.path.isfile(name) and name
    
    for cf in (
            args.conf,
            os.getenv("TERMINAL_WEATHER_CF"),
            mkfile(os.getenv("XDG_CONFIG_HOME"), "terminal-weather", "conf"),
            mkfile(os.getenv("HOME"), ".config", "terminal-weather", "conf"),
            mkfile(os.getenv("HOME"), ".terminal-weather")
    ):
        if cf:
            return cf

def init_conf(args):
    """Make a function to lookup values from args, config and defaults.

    The returned function takes the name of a variable and returns its value
    from 'args', configuration file or default values, otherwise None.
    Variables of type 'cumulative' must be returned inside an iterable.

    Positional Argument:
    args -- an object with command-line args as attributes
    """
    conf_file = resolve_cf(args)
    if not conf_file:
        error("unable to locate configuration file", exit_code=3)

    global CONF_FILE
    CONF_FILE = conf_file
    conf = parse_conf(conf_file, CONF_SPEC)

    def lookup(var):
        try:
            value = getattr(args, var)
            if value:
                if var in CONF_SPEC["cumulative"]:
                    value = (value,)
                return value
        except AttributeError as e:
            pass

        value = conf(var)
        if value:
            return value

        return DEFAULTS.get(var)

    return lookup

def write_conf(name, value):
    print("The following configuration file will be updated:\n" + CONF_FILE)
    if prompt(f"Do you agree? (yes/no):") != "yes":
        return
    
    try:
        with open(CONF_FILE, mode='a') as cf:
            cf.write(f"\n{name}={value}\n")
    except Exception as e:
        error(str(e), exit_code=1)
            
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
    
    csv -- a string of comma-separated values
    """
    return tuple(value.strip() for value in csv.split(','))

def error(msg, exit_code=2, prefix="Error: "):
    """Exit with an error message.

    print the provided error message to stderr and exit with the given
    status code.
    """
    print(prefix, msg, sep='', file=sys.stderr)
    sys.exit(exit_code)

def count_ts(end):
    """Return the number of timestamps until a given time.

    timestamps are spaced with 3-hour intervals. Counting starts from the last
    hour.

    end -- string describing a point in time at which counting stops.
    """

    now = datetime.now()
    next_day = { # each day ends at 00:00 of the next day 
        "today": now.day+1,
        "tomorrow": now.day+2
    }

    if end not in next_day:
        return

    delta = datetime(now.year, now.month, next_day[end], 0, 0) - now
    return math.ceil(delta.total_seconds() / 3600 / 3)
