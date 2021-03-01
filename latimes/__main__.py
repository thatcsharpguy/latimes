import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

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
@click.argument("cadena_tiempo", type=click.STRING)
@click.option("--config", default=None, type=click.Path(dir_okay=False, exists=True))
def main(cadena_tiempo: str, config: str):
    """
    CADENA_TIEMPO Este es tu tiempo en lenguaje natural
    """

    config_file = Path(config) if config else None

    configuration = load_config(config_file)

    tiempo_usuario = interpreta_cadena_tiempo(cadena_tiempo)

    if tiempo_usuario:

        tiempos = transforma_zonas_horarias(tiempo_usuario, configuration)

        for pais, tiempo in tiempos:
            print(pais + ": " + tiempo.strftime("%Y/%m/%d, %H:%M"))

    else:
        print("Cadena inválida")


def interpreta_cadena_tiempo(cadena_tiempo: str) -> datetime:
    match = TIEMPO_REGEX.match(cadena_tiempo)
    today = datetime.today()

    if not match:
        return None

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


if __name__ == "__main__":
    main()
