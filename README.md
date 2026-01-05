## Overview

Fetch weather data and print it to stdout in various formats.

`Todo: add demo GIFs`

## Features

`Todo`

- City detection by IP address

## Requirements

- Python 3

## Installation

`To do`

## Usage

```
weather [options] [when] [city [country]]

    Positional arguments

    when       now | today | tomorrow | forecast (default: now)
    city       city name (default: configured city)
    country    in case there are multiple cities with the same name

    Options

    -F, --format=human|short|json (default: human)
    -f, --field=FIELD_NAME	  (prints only one field)
    -u, --units=metric|imperial|standard
    -h, --help
    -v, --version
```

## Examples

`To do`

## Configuration

`To do`

## Exit status codes

* `1`: filesystem error
* `2`: bad configuration

## Future Improvements

- Add colored output
- Show weather icon in terminals that support it

## Limitations

`To do`

## License

This project is licensed under the MIT License.