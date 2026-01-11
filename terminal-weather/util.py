import re
import requests
import sys

CONF_SPEC = {
    "cumulative": ("geoip-url", "geoip-fields")
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
        sys.exit(2)

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
        sys.exit(2)

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
                    sys.exit(2)
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
