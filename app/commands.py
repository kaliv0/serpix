import os

import click


@click.command()
@click.argument("file", type=click.STRING)
@click.option(
    "-c",
    "--bytes",
    type=click.STRING,
    help="print the byte counts",
)
def wc(file: str) -> None:
    bytes_count = os.stat(file).st_size
    click.echo(bytes_count)
