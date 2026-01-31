# SPDX-License-Identifier: GPL-3.0-or-later

"""Printing and formatting procedures"""

from datetime import datetime
from functools import partial
from . import owm

def print_ts(weather_dict,
             fields,
             sep,
             field_delim,
             end='\n',
             lookup=owm.grep_weather,
             context=None):
    """Extract and print specific fields from a weather dictionary."""

    print(field_delim.join(
        sep.join(
            (field, format_value(field, lookup(weather_dict, field), context))
        ) for field in fields
    ), end=end)

def format_value(field, value, context):
    """Make a printable string of a given field value."""

    # todo: add units

    if field == "dt":
        return format_time(value + context["timezone"], context["time-format"])
    return str(value)

def format_time(timestamp, fstr):
    """Make a representation time string for a unix timestamp."""
    return datetime.fromtimestamp(timestamp).strftime(fstr)

def print_forecast(forecast_dict,
                   fields,
                   sep,
                   field_delim,
                   ts_delim,
                   time_format):
    """Extract and print a list of weather timestamps for specific fields."""

    # Separate daylight fields
    daylight_fields = tuple(f for f in ("sunrise", "sunset") if f in fields)
    fields = tuple(f for f in ("dt",*fields) if f not in daylight_fields)

    print_data = partial(print_ts, sep=sep, field_delim=field_delim)

    if not forecast_dict.get("list"):
        return

    timestamps = forecast_dict["list"]
    for i, ts in enumerate(timestamps):
        print_data(ts, fields, end='', context={
            "timezone": owm.grep_forecast(forecast_dict, "timezone"),
            "time-format": time_format
        })
        if i < len(timestamps) - 1:
            print(ts_delim, end='')

    if daylight_fields:
        if timestamps:
            print(ts_delim, end='')
        daylight_data = dict(
            (f, owm.grep_forecast(forecast_dict, f)) for f in daylight_fields
        )
        print_data(daylight_data,
                 daylight_fields,
                 lookup=lambda d,k: d.get(k),
                 end='')
    print()
