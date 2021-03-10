import collections.abc
from pathlib import Path
from typing import Dict, List, Union

import yaml
from pytz import timezone


class LatimesOutputFormatting:
    def __init__(
        self,
        time_format_string: str,
        different_time_joiner: str,
        aggregate_joiner: str,
        aggregate: bool,
    ):
        self.aggregate = aggregate
        self.aggregate_joiner = aggregate_joiner
        self.time_format_string = time_format_string
        self.different_time_joiner = different_time_joiner

    def __eq__(self, other) -> bool:
        if not isinstance(other, LatimesOutputFormatting):
            return False
        return (
            other.time_format_string == self.time_format_string
            and other.different_time_joiner == self.different_time_joiner
            and other.aggregate == self.aggregate
            and other.aggregate_joiner == self.aggregate_joiner
        )

    @classmethod
    def from_dict(cls, dictionary: Dict):
        return cls(**dictionary)


class LatimesConfiguration:
    def __init__(
        self,
        starting_timezone: Union[str, timezone],
        convert_to: Union[Dict[str, timezone], List[str]],
        output_formatting: LatimesOutputFormatting,
    ):
        self.output_formatting = output_formatting
        if isinstance(convert_to, collections.abc.Sequence):
            self.convert_to = dict()
            for content in convert_to:
                label, _, tz = content.partition(":")
                self.convert_to[label] = timezone(tz)
        else:
            self.convert_to = convert_to

        if isinstance(starting_timezone, str):
            self.starting_timezone = timezone(starting_timezone)
        else:
            self.starting_timezone = starting_timezone

    def __eq__(self, other) -> bool:
        if not isinstance(other, LatimesConfiguration):
            return False

        return (
            other.convert_to == self.convert_to
            and other.output_formatting == self.output_formatting
            and other.starting_timezone == self.starting_timezone
        )

    @classmethod
    def from_dict(cls, dictionary: Dict):
        output_format = LatimesOutputFormatting.from_dict(
            dictionary["output_formatting"]
        )

        convert_to = dict()
        for content in dictionary["convert_to"]:
            label, _, tz = content.partition(":")
            convert_to[label] = timezone(tz)
        starting_timezone = timezone(dictionary["starting_timezone"])

        return cls(
            starting_timezone=starting_timezone,
            convert_to=convert_to,
            output_formatting=output_format,
        )


TIME_FORMAT_STRING = "%H:%M"
AGGREGATE_JOINER = ""
AGGREGATE = True
DIFFERENT_TIME_JOINER = ", "

DEFAULT_VALUES = {
    "starting_timezone": "America/Mexico_City",
    "convert_to": [
        "🇲🇽:America/Mexico_City",
        "🇨🇴:America/Bogota",
        "🇨🇱:America/Santiago",
        "🇪🇨:America/Guayaquil",
        "🇵🇪:America/Lima",
        "🇦🇷:America/Argentina/Buenos_Aires",
        "🇬🇶:Africa/Malabo",
        "🇨🇷:America/Costa_Rica",
    ],
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


def load_config(file: Path) -> LatimesConfiguration:
    if not file or not file.exists():
        return LatimesConfiguration.from_dict(DEFAULT_VALUES)

    with open(file) as readable:
        configuration = yaml.safe_load(readable)

    output_formatting = _update(
        configuration.get("output_formatting", dict()),
        DEFAULT_VALUES["output_formatting"],
    )
    configuration["output_formatting"] = output_formatting
    return LatimesConfiguration.from_dict(configuration)


def write_config(file: Path):
    with open(file, "w", encoding="utf8") as writable:
        writable.write("# The timezones must be expressed in TZ timezone\n")
        writable.write(
            "# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\n"
        )
        yaml.safe_dump(DEFAULT_VALUES, writable)
