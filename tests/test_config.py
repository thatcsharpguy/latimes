from latimes.config import load_config, DEFAULT_VALUES
from copy import deepcopy
from pathlib import Path
from pytz import timezone


def test_load_config_gets_default_values():
    expected_values = deepcopy(DEFAULT_VALUES)
    actual_values = load_config(None)
    assert actual_values == expected_values


def config_file():
    configuration_file_path = Path("config.yml")
    with open(configuration_file_path, "w") as writable:
        writable.write("""
starting_timezone: America/Mexico_City
convert_to:
 - Colombia:America/Bogota
 - Chile:America/Santiago
 - Costa Rica:America/Costa_Rica
        """)
    return configuration_file_path

def test_load_config_from_file():
    expected_value = {
        "starting_timezone": timezone("America/Mexico_City"),
        "convert_to": {
            "Colombia": timezone("America/Bogota"),
            "Chile": timezone("America/Santiago"),
            "Costa Rica": timezone("America/Costa_Rica"),
        }
    }

    file = config_file()

    assert expected_value == load_config(file)


