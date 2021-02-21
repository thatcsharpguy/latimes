import click

@click.command()
@click.argument("cadena_tiempo",  type=click.STRING)
def main(cadena_tiempo: str):
    """
    CADENA_TIEMPO Este es tu tiempo en lenguaje natural
    """
    print("Hola mundo " + cadena_tiempo)

if __name__ == "__main__":
    main()