import click

from app.cli import commands


class ExceptionHandler(click.Group):
    def __call__(self, *args, **kwargs) -> None:
        try:
            return self.main(*args, **kwargs)
        except Exception as e:
            click.echo(e, err=True)


@click.group(cls=ExceptionHandler)
def cli() -> None:
    pass


cli.add_command(commands.wc)
cli.add_command(commands.head)
