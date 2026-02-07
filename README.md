## Overview

Get current weather and forecasts for upcoming days

`todo: add demo GIF`

## Notable Features

- Based on currently maintained OpenWeatherMap API features[^1]
- Current weather for any location on earth
- Support for both location name and geocoordinates
- City detection by IP address
- Weather forecasts for specific days or custom day-ranges
- 18 available fields related to temperature, pressure, wind and more
- Togglable raw json data output
- Settings persistence through configuration file

## Requirements

- Python 3.9+

## Installation

* `pip install git+https://github.com/helanabi/terminal-weather.git`

> Temporarily: you need to manually create a configuration file with
the content of `./conf` (until an automated procedure is implemented),
e.g. copy the content of `./conf` to `~/.terminal-weather`.

## Usage

```
usage: weather [-h] [-c CONF] [-d DAYS] [-D] [-f FIELDS] [-j] [-k KEY]
               [-u {metric,imperial,standard}] [-g GEOCOORDINATES |
               -l LOCATION] [-v]
               [{now,today,tomorrow,forecast}]

Get current weather and forecasts for upcoming days

positional arguments:
  {now,today,tomorrow,forecast}
                        show weather data for the specified time period
                        (default: now)

options:
  -h, --help            show this help message and exit
  -c, --conf CONF       configuration file
  -d, --days DAYS       show weather forecasts for the specified day or a
                        range of the form: [start],[end]
  -D, --debug           enable debugging messages
  -f, --fields FIELDS   specify a comma-separated list of fields to show
                        (default: city,desc,temp), or 'all' to show all
                        fields. Available fields are: city, desc, temp,
                        feels_like, temp_min, temp_max, pressure, humidity,
                        sea_level, grnd_level, visibility, wind_speed,
                        wind_deg, wind_gust, rain, clouds, sunrise, sunset
  -j, --json            show results in raw json format
  -k, --key KEY         OpenWeatherMap API key
  -u, --units {metric,imperial,standard}
                        (default: metric)
  -g, --geocoordinates GEOCOORDINATES
                        geocoordintes of the form: latitude,longitude
  -l, --location LOCATION
                        a location of the form: city[,country]
  -v, --version         show software version and copyright notice
```

## Examples

- `weather`  
Print current weather for preconfigured location, otherwise attempt  
to auto-detect it and prompt user to save it.

- `weather today`  
Show weather forecasts for today (this is an alias for `weather --days 0`).

- `weather --days 1,3 --fields rain,clouds --location rabat,MA`  
Show forecasted rain and clouds for three days starting tomorrow  
in Rabat (Morocco).

- `weather -f visibility,wind_speed --geocoordinates 33,-6 tomorrow`  
Show forecasted visibility and wind speed tomorrow in the location with  
geocoordinates: latitude=33 and longitude=-6.

- `weather --units imperial -f temp -l berkeley forecast`  
Show temperature for the next 5 days in Berkeley, using imperial units  
(e.i. temperature in Fahrenheit).

## Configuration

### Configuration file resolution order:

1. Command line option `-c`|`--conf`
2. Environment variable `TERMINAL_WEATHER_CF`
3. `$XDG_CONFIG_HOME/terminal-weather/conf`
4. `$HOME/.config/terminal-weather/conf`
5. `$HOME/.terminal-weather`

### Notes

- Command line arguments always take precendence over configuration
file settings.
- All command line options (excluding `help` and `version`)
can be set in a configuration file using the long option name,
e.g. `units=imperial`.
- Flags (zero-argument options) can be set by assigning an arbirary string
(excluding whitespace characters) to them. e.g. `json=yes` (`json=no` will have the same effect, the actual value is not interpreted).

## Exit status codes

* `1`: filesystem error
* `2`: bad usage
* `3`: bad configuration
* `9`: unknown error

## Future Improvements

- Add configuration entry: ljust-width
- Automated configuration file generation
- Better output format
- Custom time range in forecasts
- Custom output delimiters
- Custom field labels
- Weather icon in terminals that support it
- Hide field label when only one field is requested
- Add fields: pop, snow
- Country name-to-code conversion and vice-versa
- Custom units (symbol + formula)
- Custom time zone
- Add --no-prompt flag for non-interactive usage
- Caching functionality for offline usage

## Limitations

- Currently the program uses an OpenWeatherMap free tier API key, that has
a rate limit (60 calls/minute) and monthly quota (1M calls/month).
Thankfully this is plenty for a few users, but it isn't scalable.
However, anyone can get a free API key from OWM and pass it to the program
as a command line argument `(-k/--key)`, or even better permanently set it
in the configuration file.

## License

This project is licensed under the GNU General Public License v3.0 or later.  
See the COPYING file for details.

---

[^1]: Notably, it uses geocoding API for city/geocoordinates translation
rather than relying on **deprecated** automatic location resolution.
