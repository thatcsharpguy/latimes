from copy import deepcopy
from datetime import datetime

import pytest
from freezegun import freeze_time
from pytz import timezone

from latimes import interpreta_cadena_tiempo, transforma_zonas_horarias
from latimes.config import DEFAULT_VALUES, LatimesConfiguration


@freeze_time("2021-02-22")
@pytest.mark.parametrize(
    ["cadena_entrada", "valor_esperado"],
    [
        ("jueves 10 pm", datetime(2021, 2, 25, 22, 00)),
        ("viernes 10 am", datetime(2021, 2, 26, 10, 00)),
        ("Viernes 10 am", datetime(2021, 2, 26, 10, 00)),
        ("Sábado 10 am", datetime(2021, 2, 27, 10, 00)),
        ("domingo 8:30 am", datetime(2021, 2, 28, 8, 30)),
        ("DoMiNGo 8:30 am", datetime(2021, 2, 28, 8, 30)),
        ("27 de febrero 5 pm", datetime(2021, 2, 27, 17, 00)),
        ("2 de marzo 9:30 pm", datetime(2021, 3, 2, 21, 30)),
        ("2 de marzo 9:01 pm", datetime(2021, 3, 2, 21, 1)),
        ("2 marzo 9:01 pm", datetime(2021, 3, 2, 21, 1)),
    ],
)
def test_interpreta_cadena_tiempo(cadena_entrada, valor_esperado):

    valor_actual = interpreta_cadena_tiempo(cadena_entrada)

    assert valor_esperado == valor_actual


@freeze_time("1982-12-29")  # Wednesday
@pytest.mark.parametrize(
    ["cadena_entrada", "valor_esperado"],
    [
        ("viernes 10 pm", datetime(1982, 12, 31, 22, 00)),
        ("sábado 10 am", datetime(1983, 1, 1, 10, 00)),
        ("Domingo 10 am", datetime(1983, 1, 2, 10, 00)),
        ("1 de enero 10 am", datetime(1983, 1, 1, 10, 00)),
        ("31 de diciembre 10 am", datetime(1982, 12, 31, 10, 00)),
    ],
)
def test_interpreta_cadena_tiempo_end_of_year(cadena_entrada, valor_esperado):

    valor_actual = interpreta_cadena_tiempo(cadena_entrada)

    assert valor_esperado == valor_actual


@pytest.mark.parametrize(
    "cadena_entrada",
    [
        ("lunes10 pm"),
        ("xD pm"),
    ],
)
def test_interpreta_cadena_fails(cadena_entrada):

    with pytest.raises(ValueError):
        interpreta_cadena_tiempo(cadena_entrada)


def test_transforma_zonas_horarias():
    hora_entrada = datetime(2021, 2, 22, 10, 0)
    horas_esperadas = [
        (
            "🇲🇽",
            datetime(2021, 2, 22, 10, 0, tzinfo=timezone("America/Mexico_City")),
        ),
        ("🇨🇴", datetime(2021, 2, 22, 11, 0, tzinfo=timezone("America/Bogota"))),
        ("🇨🇱", datetime(2021, 2, 22, 13, 0, tzinfo=timezone("America/Santiago"))),
        ("🇪🇨", datetime(2021, 2, 22, 11, 0, tzinfo=timezone("America/Guayaquil"))),
        ("🇵🇪", datetime(2021, 2, 22, 11, 0, tzinfo=timezone("America/Lima"))),
        (
            "🇦🇷",
            datetime(
                2021, 2, 22, 13, 0, tzinfo=timezone("America/Argentina/Buenos_Aires")
            ),
        ),
        (
            "🇬🇶",
            datetime(2021, 2, 22, 17, 0, tzinfo=timezone("Africa/Malabo")),
        ),
        (
            "🇨🇷",
            datetime(2021, 2, 22, 10, 0, tzinfo=timezone("America/Costa_Rica")),
        ),
    ]
    configuration = LatimesConfiguration.from_dict(deepcopy(DEFAULT_VALUES))

    valor_retorno = transforma_zonas_horarias(hora_entrada, configuration)

    for (pais_esperado, fecha_esperada), (pais_retorno, fecha_retorno) in zip(
        horas_esperadas, valor_retorno
    ):
        assert pais_esperado == pais_retorno
        assert fecha_esperada.year == fecha_retorno.year
        assert fecha_esperada.month == fecha_retorno.month
        assert fecha_esperada.day == fecha_retorno.day
        assert fecha_esperada.hour == fecha_retorno.hour
        assert fecha_esperada.minute == fecha_retorno.minute


def test_transforma_zonas_horarias_no_default():
    hora_entrada = datetime(2021, 2, 22, 10, 0)
    horas_esperadas = [
        ("Mexico", datetime(2021, 2, 22, 9, 0, tzinfo=timezone("America/Mexico_City"))),
    ]
    configuration = LatimesConfiguration(
        timezone("America/Bogota"), {"Mexico": timezone("America/Mexico_City")}, None
    )

    valor_retorno = transforma_zonas_horarias(hora_entrada, configuration)

    for (pais_esperado, fecha_esperada), (pais_retorno, fecha_retorno) in zip(
        horas_esperadas, valor_retorno
    ):
        assert pais_esperado == pais_retorno
        assert fecha_esperada.year == fecha_retorno.year
        assert fecha_esperada.month == fecha_retorno.month
        assert fecha_esperada.day == fecha_retorno.day
        assert fecha_esperada.hour == fecha_retorno.hour
        assert fecha_esperada.minute == fecha_retorno.minute
