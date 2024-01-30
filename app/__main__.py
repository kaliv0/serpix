import click

from app.cli import commands



@click.group()
def cli() -> None:
    pass


cli.add_command(commands.wc)
