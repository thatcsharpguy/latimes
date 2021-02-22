import pytest
from datetime import datetime
from freezegun import freeze_time
from pytz import timezone
from latimes import interpreta_cadena_tiempo, transforma_zonas_horarias

@freeze_time("2021-02-22")
@pytest.mark.parametrize(
    ["cadena_entrada", "valor_esperado"],
    [
        ("jueves 10 pm", datetime(2021, 2, 25, 22, 00)),
        ("viernes 10 am", datetime(2021, 2, 26, 10, 00)),
        # ("domingo 8 am", datetime(2021, 2, 28, 8, 00)),
    ]
)
def test_interpreta_cadena_tiempo(cadena_entrada, valor_esperado):

    valor_actual = interpreta_cadena_tiempo(cadena_entrada)

    assert valor_esperado == valor_actual


def test_transforma_zonas_horarias():
    hora_entrada = datetime(2021, 2, 22, 10, 0)
    horas_esperadas = [
        ('Colombia', datetime(2021, 2, 22, 11, 0, tzinfo=timezone('America/Bogota'))),
        ('Chile', datetime(2021, 2, 22, 13, 0, tzinfo=timezone('America/Santiago'))),
        ('Ecuador', datetime(2021, 2, 22, 11, 0, tzinfo=timezone('America/Guayaquil'))),
        ('Perú', datetime(2021, 2, 22, 11, 0, tzinfo=timezone('America/Lima'))),
        ('Argentina', datetime(2021, 2, 22, 13, 0, tzinfo=timezone('America/Argentina/Buenos_Aires'))),
        ('Guinea Ecuatorial', datetime(2021, 2, 22, 17, 0, tzinfo=timezone('Africa/Malabo'))),
        ('Costa Rica', datetime(2021, 2, 22, 10, 0, tzinfo=timezone('America/Costa_Rica'))),
    ]

    valor_retorno = transforma_zonas_horarias(hora_entrada)

    for (pais_esperado, fecha_esperada), (pais_retorno, fecha_retorno) in zip(horas_esperadas, valor_retorno):
        assert pais_esperado == pais_retorno
        assert fecha_esperada.year == fecha_retorno.year
        assert fecha_esperada.month == fecha_retorno.month
        assert fecha_esperada.day == fecha_retorno.day
        assert fecha_esperada.hour == fecha_retorno.hour
        assert fecha_esperada.minute == fecha_retorno.minute