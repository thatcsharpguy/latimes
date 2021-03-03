from pathlib import Path
from typing import Optional

import yaml
from pytz import timezone

DEFAULT_VALUES = {
    "starting_timezone": timezone("America/Mexico_City"),
    "convert_to": {
        "Colombia": timezone("America/Bogota"),
        "Chile": timezone("America/Santiago"),
        "Ecuador": timezone("America/Guayaquil"),
        "Perú": timezone("America/Lima"),
        "Argentina": timezone("America/Argentina/Buenos_Aires"),
        "Guinea Ecuatorial": timezone("Africa/Malabo"),
        "Costa Rica": timezone("America/Costa_Rica"),
    },
}


def load_config(file: Optional[Path]) -> dict:
    if not file:
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

    return real_configuration
