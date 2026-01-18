"""Configuration management and other utility functions.

Exported objects:
  - init_conf(args): initialize config and make a lookup function
  - get_location(conf): get user location data using geoip services
"""

import os
import re
import requests
import sys

CONF_SPEC = {
    "cumulative": ("geoip-url", "geoip-fields", "key"),
    "singleton": ("location", "geocoordinates")
}

DEFAULTS = {
    "when": "today",
    "color": "yes",
    "fields": "",
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
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

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
    """Make a function to lookup values from args and config.

    The returned function takes the name of a variable and returns its value
    from 'args', configuration file or default values, otherwise None.
    Variables of type 'cumulative' must be returned inside an iterable.

    Positional Argument:
    args -- an object with command-line args as attributes
    """
    pass # todo
    # conf_file = util.resolve_cf(args)
    # if not conf_file:
    #     print("Error: unable to locate configuration file", file=sys.stderr)
    #     sys.exit(3)

    # conf = util.parse_conf(conf_file, CONF_SPEC)

    # if args.key:
    #     api_keys = [args.key]
    # elif conf("key"):
    #     api_keys = conf("key")
    # else:
    #     print("Error: unable to find an API key", file=sys.stderr)
    #     sys.exit(9)

    # if args.location:
    #     location = args.location
    # elif conf("location"):
    #     location = conf("location")
    # else:
    #     pass
        
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

def guess_location(lookup):
    """Try to find user location coordinates.

    If succesfull, return a tuple of coordinates (latitude, longitude),
    otherwise return None.

    Positional argument:
    lookup -- a function that can lookup configuration entries
    """
    pass # todo
    # try:
    #     location = util.get_location(get_value)
    #     if location:
    #         print(f"It appears that you are in {location.city},",
    #               location.country_name)
            
    #         if prompt("Is this your correct location? (yes/no):") == "yes":
    #             coords = (location.lat, location.lon)
    #             if prompt("Would you like to save this location for future"
    #                       " runs? (yes/no):") == "yes":
    #             else:
    #                 print("Please run the program with the -l/--location "
    #                       "option to specify a location.\n"
    #                       "Note: you may specify a default location in "
    #                       "your configuration file.")
