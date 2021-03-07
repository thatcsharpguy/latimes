from unittest.mock import patch

from click.testing import CliRunner
from freezegun import freeze_time

from latimes.__main__ import main


@freeze_time("2021-02-22")
def test_main():
    runner = CliRunner()
    result = runner.invoke(main, ["jueves", "10:00", "am"])

    assert result.exit_code == 0
    assert result.stdout == "10:00 🇲🇽🇨🇷, 11:00 🇨🇴🇪🇨🇵🇪, 13:00 🇨🇱🇦🇷, 17:00 🇬🇶\n"
