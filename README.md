## Overview

Get current weather and forecasts for upcoming days

`todo: add demo GIF`

## Features

- Support for location name and geocoordinates
- City detection by IP address
- Settings persistence through configuration file
- Ability to select from multiple weather metrics
- Togglable raw json data output

## Requirements

- Python 3.9+

## Installation

`pip install git+https://github.com/helanabi/terminal-weather.git`

## Usage

```
usage: weather [-h] [-c CONF] [-C {yes,no}] [-d] [-f FIELDS] [-j] [-k KEY]
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
  -C, --color {yes,no}  enable colored output (default: yes). This option is
                        ignored when -j/--json is used
  -d, --debug           enable debugging messages
  -f, --fields FIELDS   specify a comma-separated list of fields to show
                        (default: desc,temp), or 'all' to show all fields.
                        Available fields are: desc, temp, feels_like,
                        temp_min, temp_max, pressure, humidity, sea_level,
                        grnd_level, visibility, wind_speed, wind_deg,
                        wind_gust, rain, clouds, sunrise, sunset.
  -j, --json            show results in raw json format
  -k, --key KEY         OpenWeatherMap API key
  -u, --units {metric,imperial,standard}
                        (default: metric)
  -g, --geocoordinates GEOCOORDINATES
                        geocoordintes of the form: latitude,longitude
  -l, --location LOCATION
                        a location of the format: city[,country]
  -v, --version         show software version and copyright notice
```

## Examples

- `weather`
Print current weather for preconfigured location, otherwise attempt
to auto-detect it and prompt user to save it.

- `weather --fields visibility,wind_speed --location rabat,ma tomorrow`
Show forecasted visibility and wind speed in Rabat (Morocco) tomorrow 

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
* `4`: connection error
* `9`: unknown error

## Future Improvements

- Better output format
- Custom time range in forecasts
- Custom output delimiters
- Custom field labels
- User defined colors
- Weather icon in terminals that support it
- Caching functionality for offline usage

## License

This project is licensed under the GNU General Public License v3.0 or later.
See the COPYING file for details.
