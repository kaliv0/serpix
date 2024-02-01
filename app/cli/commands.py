import click

from app.cli.utils import head_utils, wc_utils

# ### wc ###


@click.command()
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
    """
    Print newline, word, and byte counts for each FILE, and a total line if
    more than one FILE is specified.  A word is a non-zero-length sequence of
    characters delimited by white space.

    With no FILE, or when FILE is -, read standard input.

    """
    wc_opts = wc_utils.build_wc_options(show_lines, show_words, show_chars, show_bytes)
    if len(file_list) > 1:
        wc_utils.handle_file_list(file_list, wc_opts)
    else:
        wc_utils.handle_single_file(file_list, wc_opts)


# ### head ###


@click.command()
@click.argument("file_list", metavar="file", type=click.Path(), nargs=-1)
@click.option(
    "-c",
    "--bytes",
    "byte_count",
    type=click.IntRange(0),
    help="""print the first NUM bytes of each file""",
)
@click.option(
    "-n",
    "--lines",
    "line_count",
    type=int,
    default=10,
    show_default=True,
    help="""print the first NUM lines instead of the first 10;
    with the leading '-', print all but the last NUM lines of each file""",
)
@click.option(
    "-q",
    "--quiet",
    "--silent",
    is_flag=True,
    help="never print headers giving file names",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="always print headers giving file names",
)
def head(
    file_list: tuple[str, ...],
    byte_count: int,
    line_count: int,
    quiet: bool,
    verbose: bool,
) -> None:
    """
    Print the first 10 lines of each FILE to standard output.
    With more than one FILE, precede each with a header giving the file name.

    With no FILE, or when FILE is -, read standard input.
    """

    #
    # -no file -> read 10 lines from sdtin
    # -list of files -> with/out opts
    #     -> display header of each file as "==> test2.txt <=="
    #     -> empty line between files
    #
    head_opts = head_utils.build_head_options(byte_count, line_count, quiet, verbose)
    if len(file_list) > 1:
        # head_utils.handle_file_list(file_list, head_opts)
        ...
    elif len(file_list) == 1:
        head_utils.handle_single_file(file_list[0], head_opts)
    else:
        # head_utils.read_from_sdtin(head_opts)
        ...


# ### cat ###

# ### tail ###

# ### grep ###

# ### sed ###

# ### tr ###

# ### cut ###

# ### sort ###

# ### uniq ###

###### ???????? ######

# ### diff -> without pager ###

# ### more ###

# ### less ###

# ### crontab ###
