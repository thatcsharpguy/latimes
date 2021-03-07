import collections.abc
import logging
from pathlib import Path
from typing import Optional

import yaml
from pytz import timezone

TIME_FORMAT_STRING = "%H:%M"
AGGREGATE_JOINER = ""
AGGREGATE = True
DIFFERENT_TIME_JOINER = ", "

DEFAULT_VALUES = {
    "starting_timezone": timezone("America/Mexico_City"),
    "convert_to": {
        "🇲🇽": timezone("America/Mexico_City"),
        "🇨🇴": timezone("America/Bogota"),
        "🇨🇱": timezone("America/Santiago"),
        "🇪🇨": timezone("America/Guayaquil"),
        "🇵🇪": timezone("America/Lima"),
        "🇦🇷": timezone("America/Argentina/Buenos_Aires"),
        "🇬🇶": timezone("Africa/Malabo"),
        "🇨🇷": timezone("America/Costa_Rica"),
    },
    "output_formatting": {
        "time_format_string": TIME_FORMAT_STRING,
        "aggregate_joiner": AGGREGATE_JOINER,
        "aggregate": AGGREGATE,
        "different_time_joiner": DIFFERENT_TIME_JOINER,
    },
}


def _update(anchor, updated):
    for k, v in updated.items():
        if isinstance(v, collections.abc.Mapping):
            anchor[k] = _update(anchor.get(k, {}), v)
        elif k not in anchor:
            anchor[k] = v
    return anchor


def load_config(file: Path) -> dict:
    if not file or not file.exists():
        return DEFAULT_VALUES

    with open(file) as readable:
        configuration = yaml.safe_load(readable)

    real_configuration = dict()

    real_configuration["starting_timezone"] = timezone(
        configuration["starting_timezone"]
    )
    real_configuration["convert_to"] = {}
    for convert_to_value in configuration["convert_to"]:
        zone_name, _, zone_code = convert_to_value.partition(":")
        real_configuration["convert_to"][zone_name] = timezone(zone_code)

    output_formatting = _update(
        configuration.get("output_formatting", dict()),
        DEFAULT_VALUES["output_formatting"],
    )
    real_configuration["output_formatting"] = output_formatting
    return real_configuration


def write_config(file: Path):
    dumpable = dict()
    dumpable["starting_timezone"] = DEFAULT_VALUES["starting_timezone"].zone
    dumpable["convert_to"] = [
        f"{name}:{tz.zone}" for name, tz in DEFAULT_VALUES["convert_to"].items()
    ]
    dumpable["output_formatting"] = DEFAULT_VALUES["output_formatting"]
    with open(file, "w", encoding="utf8") as writable:
        writable.write("# The timezones must be expressed in TZ timezone\n")
        writable.write(
            "# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\n"
        )
        yaml.safe_dump(dumpable, writable)
