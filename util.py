#!/usr/bin/env python

import re
import sys

def parse_values(values):
    """Return a tuple from a string of comma separated values
    Values may be double-quoted
    """
    if len(values) == 0:
        return ('',)

    if values[0] == '"':
        chunks = values[1:].split(sep='"', maxsplit=1)
        if len(chunks) == 1:
            raise ValueError("unmatched double quote")
        else:
            next_value, rest = chunks
            if len(rest) == 0:
                return (next_value,)
            elif rest[0] == ',':
                return (next_value,) + parse_values(rest[1:])
            else:
                raise ValueError(
                    "unexpected quote before:"
                    + rest
                    + "\nNote: add a comma (,) to separate quoted values."
                )
    else:
        chunks = values.split(sep=',', maxsplit=1)
        if len(chunks) == 1:
            return (chunks[0],)
        else:
            next_value, rest = chunks
            return (next_value,) + parse_values(rest)

def update_conf(root, key, value):
    if root.get(key) == None:
        root[key] = [value]
    elif isinstance(root[key], list):
        root[key].append(value)
    else:
        raise ValueError(f"key '{key}' stores a non-list value:", value)

def store_line(conf, line):
    key, value = line.split(sep="=", maxsplit=1)
    key = key.split('-')
    value = parse_values(value)
    pointer = conf
    for i in range(len(key)):
        if i+1 == len(key):
            update_conf(pointer, key[i], value)
        else:
            next_pointer = pointer.get(key[i])
            if not isinstance(next_pointer, dict):
                next_pointer = {}
                pointer[key[i]] = next_pointer
            pointer = next_pointer

def parse_conf(path):
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
                    sys.exit(2)
                store_line(conf, sanitize_conf(line))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    return lambda name: conf.get(name)
    
def get_location(geoip_services):
    template = ("lat", "lon", "country_name", "country_code", "city")
    for i in geoip_services["url"]:
        response = requests.get(geoip_services["url"][i])
        if response.ok:
            json = response.json()
            fields = geoip_services["fields"][i]
            return dict(((key, json[field])
                         for key,field in zip(template,fields)))
        else:
            response.raise_for_status()
