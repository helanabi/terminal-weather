# SPDX-License-Identifier: GPL-3.0-or-later

"""Printing and formatting procedures"""

from datetime import datetime
from functools import partial
from . import owm

def print_ts(weather_dict,
             fields, *,
             sep,
             field_delim,
             units,
             end='\n',
             lookup=owm.grep_weather,
             timezone=None,
             time_format=None):
    """Extract and print specific fields from a weather dictionary."""

    padding = max(map(len, fields))

    print(field_delim.join(
        sep.join(
            (field.ljust(padding), format_value(
                field,
                lookup(weather_dict, field),
                timezone=timezone or lookup(weather_dict, "timezone"),
                time_format=time_format,
                units=units))
        ) for field in fields
    ), end=end)

def format_value(field, value, timezone, time_format, units):
    """Make a string representation for a field value."""

    if field in ("dt", "sunrise", "sunset"):
        return format_time(
            value + (timezone or 0),
            time_format if field == "dt" else "%I:%M"
        )

    unit = owm.get_unit(field, units)
    if unit:
        return f"{value} {unit}"
    else:
        return str(value)

def format_time(timestamp, fstr):
    """Make a representation time string for a unix timestamp."""
    return datetime.fromtimestamp(timestamp).strftime(fstr)

def print_forecast(forecast_dict,
                   fields,
                   sep,
                   field_delim,
                   units,
                   ts_delim,
                   time_format):
    """Extract and print a list of weather timestamps for specific fields."""

    global_fields = ("city", "sunrise", "sunset")
    global_fields = tuple(filter(lambda f: f in global_fields, fields))
    fields = tuple(filter(lambda f: f not in global_fields, ("dt",*fields)))

    if not forecast_dict.get("list"):
        return

    print_data = partial(print_ts,
                         sep=sep,
                         field_delim=field_delim,
                         units=units,
                         timezone=owm.grep_forecast(forecast_dict, "timezone"),
                         time_format=time_format)

    timestamps = forecast_dict["list"]

    if global_fields:
        global_dict = dict(
            (f, owm.grep_forecast(forecast_dict, f)) for f in global_fields
        )
        print_data(global_dict,
                 global_fields,
                 lookup=lambda d,k: d.get(k),
                 end='')
        if timestamps:
            print(ts_delim, end='')

    for i, ts in enumerate(timestamps):
        print_data(ts, fields, end='')
        if i < len(timestamps) - 1:
            print(ts_delim, end='')
    print()
