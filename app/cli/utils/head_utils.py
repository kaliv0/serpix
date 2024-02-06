import os
import sys
from dataclasses import dataclass

import click


# ### head_options ###


@dataclass
class HeadOptions:
    quiet: bool
    verbose: bool
    byte_count: int = 0
    line_count: int = 10


def build_head_options(
    quiet: bool, verbose: bool, byte_count: int, line_count: int, multiple_files: bool = False
) -> HeadOptions:
    # NB: in the original if -v and -q are passed simultaneously
    # the second option overrides the first one
    if quiet and verbose:
        raise ValueError("Contradicting flags passed: 'quiet' and 'verbose'")
    # adjust header options if none are passed
    if not quiet and not verbose:
        if multiple_files:
            verbose = True
        else:
            quiet = True
    return HeadOptions(quiet, verbose, byte_count, line_count)


# ### files ###


def handle_single_file(file: str, head_opts: HeadOptions) -> None:
    _validate_file(file, head_opts, raise_error=True)
    message = _build_message(file, head_opts)
    click.echo(message)


def handle_file_list(file_list: tuple[str, ...], head_opts: HeadOptions) -> None:
    for idx, file in enumerate(file_list):
        if _validate_file(file, head_opts) is False:
            continue
        # leave blank line before next file header
        if idx > 0:
            click.echo()
        message = _build_message(file, head_opts)
        click.echo(message)


def read_from_sdtin(head_opts: HeadOptions) -> None:
    if head_opts.verbose:
        click.echo("==> standard input <==")
    # NB: originally if -n is negative 'head' enters an infinite loop
    if head_opts.line_count <= 0:
        click.echo("Serriously?!")
        return
    # other options (line_count) are discarded
    if head_opts.byte_count:
        message = sys.stdin.buffer.readline()[: head_opts.byte_count].decode()
        click.echo(message)
        return

    for _ in range(head_opts.line_count):
        message = sys.stdin.readline().rstrip("\n")
        click.echo(message)


# ### validate path ###


def _validate_file(file: str, head_opts: HeadOptions, raise_error: bool = False) -> bool:
    if os.path.exists(file) is False:
        message = f"head: cannot open '{file}' for reading: No such file or directory"
        if raise_error:
            raise ValueError(message)
        click.echo(message, err=True)
        return False

    if os.path.isdir(file):
        if head_opts.verbose:
            click.echo(f"==> {file} <==\n")
        message = f"head: error reading '{file}': Is a directory"
        if raise_error:
            raise ValueError(message)
        click.echo(message, err=True)
        return False
    return True


# ### result messages ###


def _build_message(file: str, head_opts: HeadOptions) -> str:
    if head_opts.byte_count:
        with open(file, "rb") as f:
            file_content = f.read(head_opts.byte_count).decode().rstrip("\n")
    else:
        with open(file, "r") as f:
            lines = f.readlines()[: head_opts.line_count]
        # remove final new line to mimic original message
        lines[-1] = lines[-1].rstrip("\n")
        file_content = "".join(lines)

    if head_opts.verbose:
        return f"==> {file} <==\n" + file_content
    return file_content
