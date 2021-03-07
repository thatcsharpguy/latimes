import logging
import re
from collections import defaultdict, namedtuple
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import click

from latimes.config import load_config

TIEMPO_REGEX = re.compile(
    r"^((?P<dia>[a-zA-Z]+)|(?P<fecha>\d{1,2})\sde\s(?P<mes>[a-zA-Z]+))\s(?P<hora>[0-9]{1,2})(?::(?P<minutes>[0-9]{1,2}))?\s(?P<ampm>(am|pm|AM|PM))$"
)

DIAS = {
    dia: valor
    for valor, dia in enumerate(
        ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    )
}

MESES = {
    mes: valor + 1
    for valor, mes in enumerate(
        [
            "enero",
            "febrero",
            "marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "setiembre",
            "octubre",
            "noviembre",
            "diciembre",
        ]
    )
}

DIA_DOMINGO = 6


@click.command()
@click.argument("time_string", nargs=-1, type=click.STRING)
@click.option("--config", default=None, type=click.Path(dir_okay=False, exists=True))
@click.option("-v", "--verbose", count=True)
def main(time_string: List[str], config: str, verbose: int):
    """
    TIME_STRING Este es tu tiempo en lenguaje natural
    """
    setup_logging(verbose)

    if config:
        config_file = Path(config)
    else:
        logging.info("Will try to use default configuration file config.yml")
        config_file = Path("config.yml")

    time_string = " ".join(time_string)

    try:
        configuration = load_config(config_file)
    except KeyError as keyError:
        missing_key = keyError.args[0]
        logging.error(f"Missing key {missing_key} in config file")
        raise click.Abort()

    result = process_date(time_string, configuration)

    print(result)


def process_date(cadena_tiempo: str, configuration: dict) -> str:
    try:
        tiempo_usuario = interpreta_cadena_tiempo(cadena_tiempo)
    except ValueError:
        logging.error(f'"{cadena_tiempo}" is not a valid time string')
        raise click.Abort()
    tiempos = transforma_zonas_horarias(tiempo_usuario, configuration)
    return format_results(tiempo_usuario, tiempos, configuration["output_formatting"])


def setup_logging(verbose):
    if verbose > 1:
        logging.basicConfig(level=logging.DEBUG)
    if verbose > 0:
        logging.basicConfig(level=logging.INFO)
    logging.debug("Set logging level to " + str(logging.root.level))


def interpreta_cadena_tiempo(cadena_tiempo: str) -> datetime:
    match = TIEMPO_REGEX.match(cadena_tiempo)
    today = datetime.today()

    logging.info(f"Today's date is {today.isoformat()}")

    if not match:
        raise ValueError(f'"{cadena_tiempo}" is not a valid time string')

    valores = match.groupdict()

    if valores["dia"] is not None:
        dia_usuario = DIAS[valores["dia"]]

        dia_actual = today.weekday()
        if dia_usuario > dia_actual:
            dias_faltantes = dia_usuario - dia_actual
            fecha_solicitada = today + timedelta(days=dias_faltantes)
        else:
            dias_para_domingo = DIA_DOMINGO - dia_actual + 1
            fecha_solicitada = today + timedelta(days=dias_para_domingo + dia_usuario)
    elif valores["fecha"] is not None and valores["mes"] is not None:
        mes_usuario = MESES[valores["mes"]]
        dia_usuario = int(valores["fecha"])

        fecha_solicitada = datetime(today.year, mes_usuario, dia_usuario)

    minutes = int(valores["minutes"] or 0)
    hora = int(valores["hora"]) + (0 if valores["ampm"] == "am" else 12)

    return datetime(
        fecha_solicitada.year,
        fecha_solicitada.month,
        fecha_solicitada.day,
        hora,
        minutes,
    )


def transforma_zonas_horarias(
    valor_final: datetime, configuration: dict
) -> List[Tuple[str, datetime]]:
    tiempos = []
    valor_localizado = configuration["starting_timezone"].localize(valor_final)
    for pais, zona_horaria in configuration["convert_to"].items():
        tiempos.append((pais, valor_localizado.astimezone(zona_horaria)))

    return tiempos


DateDiff = namedtuple("DateDiff", ["time", "day_difference"])


def format_results(
    anchor_datetime: datetime,
    results: List[Tuple[str, datetime]],
    output_formatting: dict,
) -> str:
    aggregates: Dict[DateDiff, List[str]] = defaultdict(list)

    for pais, time in results:
        restored_time = time.replace(tzinfo=None)
        difference = restored_time.date() - anchor_datetime.date()
        date_diff = DateDiff(restored_time, difference.days)
        aggregates[date_diff].append(pais)

    times = []
    for date_diff, time_zones in aggregates.items():
        time_formatted = date_diff.time.strftime(
            output_formatting["time_format_string"]
        )
        if date_diff.day_difference:
            time_formatted += "%+d" % date_diff.day_difference

        if output_formatting["aggregate"]:
            joint_timezones = output_formatting["aggregate_joiner"].join(time_zones)
            times.append(f"{time_formatted} {joint_timezones}")
        else:
            for time_zone in time_zones:
                times.append(f"{time_formatted} {time_zone}")

    return output_formatting["different_time_joiner"].join(times)


if __name__ == "__main__":
    main()
