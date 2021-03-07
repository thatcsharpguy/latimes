from unittest.mock import patch

from click.testing import CliRunner
from freezegun import freeze_time

from latimes.__main__ import main


@freeze_time("2021-02-22")
def test_main():
    runner = CliRunner()
    result = runner.invoke(main, ["jueves", "10:00", "am"])

    assert result.exit_code == 0
    assert result.stdout == (
        "10:00 México, Costa Rica; "
        + "11:00 Colombia, Ecuador, Perú; "
        + "13:00 Chile, Argentina; "
        + "17:00 Guinea Ecuatorial"
        + "\n"
    )
