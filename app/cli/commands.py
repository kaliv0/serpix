import click

from app.cli.utils import build_wc_options, handle_file_list, handle_single_file


@click.command(help="With no FILE, or when FILE is -, read standard input.")
@click.argument("file_list", metavar="file", type=click.Path(), nargs=-1)
@click.option(
    "-c",
    "--bytes",
    "show_bytes",
    is_flag=True,
    help="print the byte counts",
)
@click.option(
    "-m",
    "--chars",
    "show_chars",
    is_flag=True,
    help="print the character counts",
)
@click.option(
    "-l",
    "--lines",
    "show_lines",
    is_flag=True,
    help="print the newline counts",
)
@click.option(
    "-w",
    "--words",
    "show_words",
    is_flag=True,
    help="print the word counts",
)
def wc(
    file_list: tuple[str, ...],
    show_bytes: bool,
    show_chars: bool,
    show_lines: bool,
    show_words: bool,
) -> None:
    wc_opts = build_wc_options(show_lines, show_words, show_chars, show_bytes)
    if len(file_list) > 1:
        handle_file_list(file_list, wc_opts)
    else:
        handle_single_file(file_list, wc_opts)
