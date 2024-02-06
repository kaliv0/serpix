import click

from app.cli import commands


class ExceptionHandler(click.Group):
    def __call__(self, *args, **kwargs) -> None:
        try:
            return self.main(*args, **kwargs)
        except (ValueError, Exception) as e:
            # NB: ValueError is raised instead of click.BadParameter e.g.
            # in order to display same messages as in the original implementation
            click.echo(e, err=True)


# @FIXME
# @click.group(cls=ExceptionHandler)
@click.group()
def cli() -> None:
    pass


cli.add_command(commands.wc)
cli.add_command(commands.head)
cli.add_command(commands.tail)
cli.add_command(commands.cat)
