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
    today = datetime.today() + timedelta(days=-4)

    if not match:
        return None

    valores = match.groupdict()
    dia_de_la_semana = DIAS[valores["dia"]]

    dias_para_domingo = 6 - today.weekday()
    dias_restantes = ((today.weekday() + dias_para_domingo + dia_de_la_semana) % 6) + 1
    fecha_usuario = today + timedelta(days=dias_restantes + dias_para_domingo)

    hora = int(valores["hora"]) + (0 if valores["ampm"] == "am" else 12)

    return datetime(
        fecha_usuario.year,
        fecha_usuario.month,
        fecha_usuario.day,
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
