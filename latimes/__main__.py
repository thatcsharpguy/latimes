import re
from datetime import datetime, timedelta
from typing import List, Tuple

import click
from pytz import timezone

TIEMPO_REGEX = re.compile(
    "^(?P<dia>[a-zA-Z]+)\s(?P<hora>[0-9]{1,2})\s(?P<ampm>(am|pm|AM|PM))$"
)
MEXICO = timezone("America/Mexico_City")

TIMEZONES = {
    "Colombia": timezone("America/Bogota"),
    "Chile": timezone("America/Santiago"),
    "Ecuador": timezone("America/Guayaquil"),
    "Perú": timezone("America/Lima"),
    "Argentina": timezone("America/Argentina/Buenos_Aires"),
    "Guinea Ecuatorial": timezone("Africa/Malabo"),
    "Costa Rica": timezone("America/Costa_Rica"),
}

DIAS = {
    dia: valor
    for valor, dia in enumerate(
        ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    )
}

DIA_DOMINGO = 6


@click.command()
@click.argument("cadena_tiempo", type=click.STRING)
def main(cadena_tiempo: str):
    """
    CADENA_TIEMPO Este es tu tiempo en lenguaje natural
    """

    tiempo_usuario = interpreta_cadena_tiempo(cadena_tiempo)

    if tiempo_usuario:

        tiempos = transforma_zonas_horarias(tiempo_usuario)

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
    dia_usuario = DIAS[valores["dia"]]

    dia_actual = today.weekday()
    if dia_usuario > dia_actual:
        dias_faltantes = dia_usuario - dia_actual
        fecha_solicitada = today + timedelta(days=dias_faltantes)
    else:
        dias_para_domingo = DIA_DOMINGO - dia_actual + 1
        fecha_solicitada = today + timedelta(days=dias_para_domingo + dia_usuario)

    hora = int(valores["hora"]) + (0 if valores["ampm"] == "am" else 12)

    return datetime(
        fecha_solicitada.year,
        fecha_solicitada.month,
        fecha_solicitada.day,
        hora,
        0,
    )


def transforma_zonas_horarias(valor_final: datetime) -> List[Tuple[str, datetime]]:
    tiempos = []
    valor_localizado = MEXICO.localize(valor_final)
    for pais, zona_horaria in TIMEZONES.items():
        tiempos.append((pais, valor_localizado.astimezone(zona_horaria)))

    return tiempos


if __name__ == "__main__":
    main()
