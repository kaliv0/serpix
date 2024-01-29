import click

from app.core import extract_file_data


@click.command(help="With no FILE, or when FILE is -, read standard input.")
@click.argument("file", type=click.STRING, nargs=-1)
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
    file: str, show_bytes: bool, show_chars: bool, show_lines: bool, show_words: bool
) -> None:
    print("Foooo ", file)

    data = extract_file_data(file)
    message = "  "
    if not show_lines and not show_words and not show_chars and not show_bytes:
        message += f"{data.line_count}\t{data.word_count}\t{data.byte_count}\t"
        if data.file_name:
            message += f"{data.file_name}"
        click.echo(message)
        return

    if show_lines:
        message += f"{data.line_count}\t"
    if show_words:
        message += f"{data.word_count}\t"
    if show_chars:
        message += f"{data.char_count}\t"
    if show_bytes:
        message += f"{data.byte_count}\t"
    if data.file_name:
        message += f"{data.file_name}"
    click.echo(message)
