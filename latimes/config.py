import collections.abc
from pathlib import Path

import yaml

from latimes.utils import DEFAULT_VALUES
from latimes.utils.latimes_configuration import LatimesConfiguration


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
