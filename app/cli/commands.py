import click

from app.cli.utils import head_utils, tail_utils, wc_utils

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
@click.option(
    "-c",
    "--bytes",
    "byte_count",
    type=click.IntRange(0),
    default=0,
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
def head(
    file_list: tuple[str, ...],
    quiet: bool,
    verbose: bool,
    byte_count: int = 0,
    line_count: int = 10,
) -> None:
    """
    Print the first 10 lines of each FILE to standard output.
    With more than one FILE, precede each with a header giving the file name.

    With no FILE, or when FILE is -, read standard input.
    """

    if len(file_list) > 1:
        head_opts = head_utils.build_head_options(
            quiet, verbose, byte_count, line_count, multiple_files=True
        )
        head_utils.handle_file_list(file_list, head_opts)
        ...
    elif len(file_list) == 1:
        head_opts = head_utils.build_head_options(quiet, verbose, byte_count, line_count)
        head_utils.handle_single_file(file_list[0], head_opts)
    else:
        head_opts = head_utils.build_head_options(quiet, verbose, byte_count, line_count)
        head_utils.read_from_sdtin(head_opts)


# ### tail ###


@click.command()
@click.argument("file_list", metavar="file", type=click.Path(), nargs=-1)
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
    help="always output headers giving file names",
)
@click.option(
    "-f",
    "--follow",
    is_flag=True,
    help="output appended data as the file grows",
)
@click.option(
    "-s",
    "--sleep-interval",
    type=click.IntRange(1),
    default=1,
    show_default=True,
    help="with -f, sleep for approximately N seconds between iterations",
)
@click.option(
    "-c",
    "--bytes",
    "byte_count",
    type=click.IntRange(0),
    default=0,
    help="output the last NUM bytes",
)
@click.option(
    "-n",
    "--lines",
    "line_count",
    type=int,
    default=10,
    show_default=True,
    help="""output the last NUM lines, instead of the last 10;
    or use -n +NUM to output starting with line NUM""",
)
def tail(
    file_list: tuple[str, ...],
    quiet: bool,
    verbose: bool,
    follow: bool,
    sleep_interval: int = 1,
    byte_count: int = 0,
    line_count: int = 10,
) -> None:
    """
    Print the last 10 lines of each FILE to standard output.
    With more than one FILE, precede each with a header giving the file name.

    With no FILE, or when FILE is -, read standard input.
    """

    # TODO:add --follow and --sleep-interval
    # raise exception if -f is used with list of files

    if len(file_list) > 1:
        tail_opts = tail_utils.build_tail_options(
            quiet, verbose, follow, sleep_interval, byte_count, line_count, multiple_files=True
        )
        tail_utils.handle_file_list(file_list, tail_opts)
        ...
    elif len(file_list) == 1:
        tail_opts = tail_utils.build_tail_options(
            quiet, verbose, follow, sleep_interval, byte_count, line_count
        )
        tail_utils.handle_single_file(file_list[0], tail_opts)
    else:
        tail_opts = tail_utils.build_tail_options(
            quiet, verbose, follow, sleep_interval, byte_count, line_count
        )
        tail_utils.read_from_sdtin(tail_opts)


# ### cat ###

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
