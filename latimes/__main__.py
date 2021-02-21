import click
import re
from datetime import datetime,timedelta

TIEMPO_REGEX = re.compile("^(?P<dia>[a-zA-Z]+)\s(?P<hora>[0-9]{1,2})\s(?P<ampm>(am|pm|AM|PM))$")
TODAY = datetime.today() + timedelta(days=-4)

DIAS = {
    dia: valor for valor, dia  in
    enumerate(["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"])
}

@click.command()
@click.argument("cadena_tiempo",  type=click.STRING)
def main(cadena_tiempo: str):
    """
    CADENA_TIEMPO Este es tu tiempo en lenguaje natural
    """
    match = TIEMPO_REGEX.match(cadena_tiempo)
    if match:
        valores = match.groupdict()
        dia_de_la_semana = DIAS[valores["dia"]]

        dias_para_domingo = 6 - TODAY.weekday()
        dias_restantes = ((TODAY.weekday() + dias_para_domingo + dia_de_la_semana) % 6) + 1
        fecha_usuario = TODAY + timedelta(days=dias_restantes + dias_para_domingo)

        hora = int(valores["hora"]) + (0 if valores["ampm"] == "am" else 12)

        valor_final = datetime(fecha_usuario.year, fecha_usuario.month, fecha_usuario.day, hora, 0)

        print(valor_final)
    else:
        print("Cadena inválida")


if __name__ == "__main__":
    main()