import logging
from pathlib import Path
from typing import List

import click
import pyperclip

from latimes.config import load_config, write_config
from latimes.exceptions import InvalidTimeStringException
from latimes.latimes import convert_times


@click.command()
@click.argument("time_string", nargs=-1, type=click.STRING)
@click.option("--config", default=None, type=click.Path(dir_okay=False))
@click.option("--create-config/--no-create-config", default=False)
@click.option("--copy/--no-copy", "-c", default=False)
@click.option("-v", "--verbose", count=True)
def main(
    time_string: List[str], config: str, create_config: bool, copy: bool, verbose: int
):
    """
    TIME_STRING Este es tu tiempo en lenguaje natural
    """
    setup_logging(verbose)

    if config:
        config_file = Path(config)
    else:
        logging.info("Will try to use default configuration file config.yml")
        config_file = Path("config.yml")

    if create_config:
        write_config(config_file)
        click.echo(f"Config file generated at {str(config_file)}")
        return

    time_string = " ".join(time_string)

    try:
        configuration = load_config(config_file)
    except KeyError as keyError:
        missing_key = keyError.args[0]
        logging.error(f"Missing key {missing_key} in config file")
        raise click.Abort()

    try:
        result = convert_times(time_string, configuration)
    except InvalidTimeStringException:
        logging.error(f'"{time_string}" is not a valid time string')
        raise click.Abort()

    print(result)

    if copy:
        pyperclip.copy(result)
        print("Copied to the clipboard!")


def setup_logging(verbose):
    if verbose > 1:
        logging.basicConfig(level=logging.DEBUG)
    if verbose > 0:
        logging.basicConfig(level=logging.INFO)
    logging.debug("Set logging level to " + str(logging.root.level))


if __name__ == "__main__":
    main()
