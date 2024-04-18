import click

from app.cli.handlers import CatHandler, CutHandler, HeadHandler, TailHandler, WCHandler
from app.cli.handlers.uniq_handler import UniqHandler

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

    wc_handler = WCHandler(show_lines, show_words, show_chars, show_bytes)
    if len(file_list) > 1:
        wc_handler.handle_file_list(file_list)
    else:
        wc_handler.handle_single_file(file_list)


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

    multiple_files = True if len(file_list) > 1 else False
    head_handler = HeadHandler(quiet, verbose, multiple_files, byte_count, line_count)
    if len(file_list) > 1:
        head_handler.handle_file_list(file_list)
    elif len(file_list) == 1:
        head_handler.handle_single_file(file_list[0])
    else:
        head_handler.read_from_stdin()


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
    byte_count: int = 0,
    line_count: int = 10,
) -> None:
    """
    Print the last 10 lines of each FILE to standard output.
    With more than one FILE, precede each with a header giving the file name.

    With no FILE, or when FILE is -, read standard input.
    """

    multiple_files = True if len(file_list) > 1 else False
    tail_handler = TailHandler(quiet, verbose, follow, multiple_files, byte_count, line_count)
    if len(file_list) > 1:
        tail_handler.handle_file_list(file_list)
    elif len(file_list) == 1:
        tail_handler.handle_single_file(file_list[0])
    else:
        tail_handler.read_from_stdin()


# ### cat ###


@click.command()
@click.argument("file_list", metavar="file", type=click.Path(), nargs=-1)
@click.option(
    "-n",
    "--number",
    "show_all_line_numbers",
    is_flag=True,
    help="number all output lines",
)
@click.option(
    "-b",
    "--number-nonblank",
    "show_nonempty_line_numbers",
    is_flag=True,
    help="number nonempty output lines",
)
@click.option(
    "-s",
    "--squeeze-blank",
    is_flag=True,
    help="suppress repeated empty output lines",
)
@click.option(
    "-E",
    "--show-ends",
    is_flag=True,
    help="display $ at end of each line",
)
@click.option(
    "-T",
    "--show-tabs",
    is_flag=True,
    help="display TAB characters as ^I",
)
@click.option(
    "-A",
    "--show-all",
    is_flag=True,
    help="equivalent to -ET",
)
def cat(
    file_list: tuple[str, ...],
    show_all_line_numbers: bool,
    show_nonempty_line_numbers: bool,
    squeeze_blank: bool,
    show_ends: bool,
    show_tabs: bool,
    show_all: bool,
) -> None:
    """
    Concatenate FILE(s) to standard output.

    With no FILE, or when FILE is -, read standard input.
    """

    cat_handler = CatHandler(
        show_all_line_numbers,
        show_nonempty_line_numbers,
        squeeze_blank,
        show_ends,
        show_tabs,
        show_all,
    )
    if len(file_list) > 1:
        cat_handler.handle_file_list(file_list)
    else:
        cat_handler.handle_single_file(file_list)


# ### cut ###


@click.command()
@click.argument("file_list", metavar="file", type=click.Path(), nargs=-1)
@click.option(
    "-b",
    "--bytes",
    "byte_count",
    type=click.STRING,
    help="select only these bytes",
)
@click.option(
    "-c",
    "--characters",
    "char_count",
    type=click.STRING,
    help="select only these characters",
)
@click.option(
    "-f",
    "--fields",
    "field_count",
    type=click.STRING,
    help="""select only these fields;  
also print any line that contains no delimiter character""",
)
@click.option(
    "-d",
    "--delimiter",
    type=click.STRING,
    help="use DELIM instead of TAB for field delimiter",
)
@click.option(
    "--output-delimiter",
    type=click.STRING,
    help="""use STRING as the output delimiter
the default is to use the input delimiter""",
)
@click.option(
    "-s",
    "--only-delimited",
    "show_only_delimited_lines",
    is_flag=True,
    help="""use STRING as the output delimiter
the default is to use the input delimiter""",
)
def cut(
    file_list: tuple[str, ...],
    byte_count: str,
    char_count: str,
    field_count: str,
    delimiter: str,
    output_delimiter: str,
    show_only_delimited_lines: bool,
) -> None:
    """
    Print selected parts of lines from each FILE to standard output.

    With no FILE, or when FILE is -, read standard input.
    """
    cut_handler = CutHandler(
        byte_count, char_count, field_count, delimiter, output_delimiter, show_only_delimited_lines
    )
    if len(file_list) > 1:
        cut_handler.handle_file_list(file_list)
    else:
        cut_handler.handle_single_file(file_list)


# ### uniq ###


@click.command()
@click.argument("file_list", metavar="file", type=click.Path(), nargs=-1)
@click.option(
    "-c",
    "--count",
    "show_count",
    is_flag=True,
    help="prefix lines by the number of occurrences",
)
@click.option(
    "-u",
    "--unique",
    "show_unique",
    is_flag=True,
    help="only print unique lines",
)
@click.option(
    "-d",
    "--repeated",
    "show_repeated",
    is_flag=True,
    help="only print duplicate lines, one for each group",
)
@click.option(
    "-D",
    "--all-repeated",
    "show_all_repeated",
    is_flag=True,
    help="print all duplicate lines",
)
@click.option(
    "-i",
    "--ignore-case",
    "ignore_case",
    is_flag=True,
    help="ignore differences in case when comparing",
)
@click.option(
    "-w",
    "--check-chars",
    type=click.IntRange(0),
    default=0,
    help="ignore differences in case when comparing",
)
@click.option(
    "-s",
    "--skip-chars",
    type=click.IntRange(0),
    default=0,
    help="avoid comparing the first N characters",
)
def uniq(
    file_list: tuple[str, ...],
    show_count: bool,
    show_unique: bool,
    show_repeated: bool,
    show_all_repeated: bool,
    ignore_case: bool,
    check_chars: int,
    skip_chars: int,
) -> None:
    """
    Filter adjacent matching lines from INPUT (or standard input),
    writing to OUTPUT (or standard output).

    With no options, matching lines are merged to the first occurrence.

    Note: 'uniq' does not detect repeated lines unless they are adjacent.
    You may want to sort the input first, or use 'sort -u' without 'uniq'.
    """
    uniq_handler = UniqHandler(
        file_list,
        show_count,
        show_unique,
        show_repeated,
        show_all_repeated,
        ignore_case,
        check_chars,
        skip_chars,
    )
    uniq_handler.process_input()


# ### sort ###
"""
-o, --output-file
-r, reverse,
-n, sort numerically,
-k, sort based on column number,
-c, check if sorted,
-u, sort and remove duplicate lines,
-M -> sort my months name ???
"""

# ### grep ###

# ### sed ###

# ### tr ###

# ### find ###

###### ???????? ######

# ### diff -> wrapper around built-in python's implementation?? ###

# ### comm ###

# ### more ###

# ### less -> use cat with click's pager?? ###

# ### crontab ###
