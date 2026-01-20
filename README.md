## Overview

Get current weather and forecasts for upcoming days

`Todo: add demo GIFs`

## Features

- City detection by IP address

`todo`

## Requirements

- Python 3.9+

## Installation

`To do`

## Usage

```
usage: weather [-h] [-c CONF] [-C {yes,no}] [-f FIELDS] [-j] [-k KEY]
               [-u {metric,imperial,standard}] [-v] [-g GEOCOORDINATES |
               -l LOCATION]
               [{now,forecast}]

Get current weather and forecasts for upcoming days

positional arguments:
  {now,forecast}        show weather data for the specified time period
                        (default: forecast)

options:
  -h, --help            show this help message and exit
  -c, --conf CONF       configuration file
  -C, --color {yes,no}  enable colored output (default: yes). This option is
                        ignored when -j/--json is used
  -f, --fields FIELDS   specify a comma-separated list of fields to show, or
                        'all' to show all fields. Available fields are: desc,
                        temp, feels_like, temp_min, temp_max, pressure,
                        humidity, sea_level, grnd_level, visibility,
                        wind_speed, wind_deg, wind_gust, rain, clouds,
                        sunrise, sunset.
  -j, --json            show results in raw json format
  -k, --key KEY         OpenWeatherMap API key
  -u, --units {metric,imperial,standard}
                        (default: metric)
  -v, --version         show software version and copyright notice
  -g, --geocoordinates GEOCOORDINATES
                        geocoordintes of the form: latitude,longitude
  -l, --location LOCATION
                        a location of the format: city[,country]
```

## Examples

`To do`

## Configuration

> Note: Command line arguments always take precendence over configuration
file settings.

Configuration file resolution order:

1. Command line option `-c`|`--conf`
2. Environment variable `TERMINAL_WEATHER_CF`
3. `$XDG_CONFIG_HOME/terminal-weather/conf`
4. `$HOME/.config/terminal-weather/conf`
5. `$HOME/.terminal-weather`

## Exit status codes

* `1`: filesystem error
* `2`: bad usage
* `3`: bad configuration
* `9`: unknown error

## Future Improvements

- Custom output delimiter and separator
- Custom field labels
- User defined colors
- Weather icon in terminals that support it
- Caching functionality for offline usage

## Limitations

`To do`

## License

This project is licensed under the GNU General Public License v3.0 or later.
See the COPYING file for details.
