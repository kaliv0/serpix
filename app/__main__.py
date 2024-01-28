import click

from app import commands


@click.group()
def cli() -> None:
    pass


cli.add_command(commands.wc)
