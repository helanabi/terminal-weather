# SPDX-License-Identifier: GPL-3.0-or-later

"""Printing and formatting procedures"""

from datetime import datetime, timezone, timedelta
from functools import partial
from . import owm
from . import util

def print_ts(weather_dict,
             fields, *,
             sep,
             field_delim,
             units,
             end='\n',
             lookup=owm.grep_weather,
             time_shift=None,
             time_format=None):
    """Extract and print specific fields from a weather dictionary."""

    padding = max(map(len, fields))

    print(field_delim.join(
        sep.join(
            (field.ljust(padding), format_value(
                field,
                lookup(weather_dict, field),
                tzinfo=timezone(timedelta(
                    seconds=time_shift or lookup(weather_dict, "timezone")
                )),
                time_format=time_format,
                units=units))
        ) for field in fields
    ), end=end)

def format_value(field, value, tzinfo, time_format, units):
    """Make a string representation for a field value."""

    if field in ("dt", "sunrise", "sunset"):
        utc_time = datetime.fromtimestamp(value, tz=timezone.utc)
        return utc_time.astimezone(tz=tzinfo).strftime(
            time_format if field == "dt" else "%I:%M"
        )

    unit = owm.get_unit(field, units)
    if unit:
        return f"{value} {unit}"
    else:
        return str(value)

def print_forecast(forecast_dict,
                   fields,
                   sep,
                   field_delim,
                   units,
                   ts_delim,
                   time_format,
                   start_day,
                   end_day):
    """Extract and print a list of weather timestamps for specific fields."""

    global_fields = ("city", "sunrise", "sunset")
    global_fields = tuple(filter(lambda f: f in global_fields, fields))
    fields = tuple(filter(lambda f: f not in global_fields, ("dt",*fields)))

    if not forecast_dict.get("list"):
        return

    shift = owm.grep_forecast(forecast_dict, "timezone")
    tzinfo = timezone(timedelta(seconds=shift))
    print_data = partial(print_ts,
                         sep=sep,
                         field_delim=field_delim,
                         units=units,
                         time_shift=shift,
                         time_format=time_format)

    now = datetime.now(tz=tzinfo)
    midnight = datetime(year=now.year,
                        month=now.month,
                        day=now.day,
                        tzinfo=tzinfo)

    start_time = midnight + timedelta(days=start_day)
    end_time = midnight + timedelta(days=end_day+1)
        
    def in_range(weather_dict):
        utc_time = datetime.fromtimestamp(
            owm.grep_weather(weather_dict, "dt"),
            tz=timezone.utc
        )

        return utc_time >= start_time and utc_time < end_time
    
    timestamps = tuple(filter(in_range, forecast_dict["list"]))

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
