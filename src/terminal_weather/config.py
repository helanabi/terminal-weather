# SPDX-License-Identifier: GPL-3.0-or-later

"""Configuration management constants and functions."""

import os
import re
import sys
from . import util

CONF_FILE = None # automatically set by init_conf()
CONF_SPEC = {
    "cumulative": ("geoip-url", "geoip-fields", "key"),
    "singleton": (
        "days",
        "location",
        "geocoordinates",
        "when",
        "fields",
        "units",
        "debug",
        "json",
        "time-format"
    )
}

DEFAULTS = {
    "when": "now",
    "fields": "city,desc,temp",
    "time-format": "%a %e %b %l %p",
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
                if not re.match('[a-z]+(-[a-z]+)*=', line):
                    print("Error: invalid configuration entry:" + entry,
                          file=sys.stderr)
                    sys.exit(3)
                store_line(conf_spec, conf, line)
    except Exception as e:
        util.error(f"An error occured while reading configuration file\n{e}",
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
        util.error("unable to locate configuration file", exit_code=3)

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
    if util.prompt(f"Do you agree? (yes/no):") != "yes":
        return
    
    try:
        with open(CONF_FILE, mode='a') as cf:
            cf.write(f"\n{name}={value}\n")
    except Exception as e:
        util.error(str(e), exit_code=1)
