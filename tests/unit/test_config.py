from copy import deepcopy
from pathlib import Path

import pytest

from latimes.config import DEFAULT_VALUES, LatimesConfiguration, load_config


@pytest.mark.parametrize("path", (None, Path("i-dont-exist.yml")))
def test_load_config_gets_default_values(path):
    expected_values = LatimesConfiguration.from_dict(deepcopy(DEFAULT_VALUES))
    actual_values = load_config(path)
    assert actual_values == expected_values


@pytest.fixture
def config_file():
    configuration_file_path = Path("config.yml")
    with open(configuration_file_path, "w") as writable:
        writable.write(
            """
starting_timezone: America/Mexico_City
convert_to:
 - Colombia:America/Bogota
 - Chile:America/Santiago
 - Costa Rica:America/Costa_Rica
        """
        )
    yield configuration_file_path
    configuration_file_path.unlink()


def test_load_config_from_file(config_file):
    expected_value = LatimesConfiguration.from_dict(
        {
            "starting_timezone": "America/Mexico_City",
            "convert_to": [
                "Colombia:America/Bogota",
                "Chile:America/Santiago",
                "Costa Rica:America/Costa_Rica",
            ],
            "output_formatting": {
                "time_format_string": "%H:%M",
                "aggregate_joiner": "",
                "aggregate": True,
                "different_time_joiner": ", ",
            },
        }
    )

    assert expected_value == load_config(config_file)


@pytest.fixture
def config_file_partial_output():
    configuration_file_path = Path("config.yml")
    with open(configuration_file_path, "w") as writable:
        writable.write(
            """
starting_timezone: America/Mexico_City
convert_to:
 - Colombia:America/Bogota
 - Chile:America/Santiago
 - Costa Rica:America/Costa_Rica
output_formatting:
    aggregate_joiner: " $$$ "
    aggregate: false
        """
        )
    yield configuration_file_path
    configuration_file_path.unlink()


def test_load_config_from_file_partial(config_file_partial_output):
    expected_value = LatimesConfiguration.from_dict(
        {
            "starting_timezone": "America/Mexico_City",
            "convert_to": [
                "Colombia:America/Bogota",
                "Chile:America/Santiago",
                "Costa Rica:America/Costa_Rica",
            ],
            "output_formatting": {
                "time_format_string": "%H:%M",
                "aggregate_joiner": " $$$ ",
                "aggregate": False,
                "different_time_joiner": ", ",
            },
        }
    )

    assert expected_value == load_config(config_file_partial_output)


@pytest.fixture
def broken_config_file():
    configuration_file_path = Path("config.yml")
    with open(configuration_file_path, "w") as writable:
        writable.write(
            """
convert_to:
 - Colombia:America/Bogota
 - Chile:America/Santiago
 - Costa Rica:America/Costa_Rica
        """
        )
    yield configuration_file_path
    configuration_file_path.unlink()


def test_load_config_from_file_fails_missing_key(broken_config_file):
    with pytest.raises(KeyError):
        load_config(broken_config_file)
