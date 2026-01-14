## Overview

Get current weather and forecasts for upcoming days

`Todo: add demo GIFs`

## Features

- City detection by IP address

## Requirements

- Python 3.9+

## Installation

`To do`

## Usage

```
usage: weather [-h] [-c CONF] [-C {yes,no}] [-f FIELDS] [-j] [-k KEY]
               [-l LOCATION] [-u {metric,imperial,standard}] [-v]
               [{now,today,tomorrow,forecast}]

positional arguments:
  {now,today,tomorrow,forecast}
                        show weather data for the specified time period
			(default: today)

options:
  -h, --help            show this help message and exit
  -c, --conf CONF       configuration file
  -C, --color {yes,no}  enable colored output (default: yes). This option is
                        ignored when -j/--json is used
  -f, --fields FIELDS   specify a comma-separated list of fields to show,
                        or 'all' to show all fields. Available fields are:
			feels_like, uvi, wind, humidity, pressure, daylight
  -j, --json            show results in raw json format
  -k, --key KEY         OpenWeatherMap API key
  -l, --location LOCATION
                        must be in the format: city[,country]
  -u, --units {metric,imperial,standard}
                        (default: metric)
  -v, --version         show software version and copyright notice
```

## Examples

`To do`

## Configuration

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

## Future Improvements

- Show weather icon in terminals that support it
- Add caching functionality for offline usage

## Limitations

`To do`

## Copyright

Copyright (C) 2026 Hassan El anabi
Terminal-weather comes with ABSOLUTELY NO WARRANTY.
You may redistribute copies of Terminal-weather
under the terms of the GNU General Public License.
For more information about these matters, see the file named COPYING.