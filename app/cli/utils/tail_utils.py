import os
import sys
from dataclasses import dataclass

import click

# ### tail_options ###


@dataclass
class TailOptions:
    quiet: bool
    verbose: bool
    follow: bool
    byte_count: int = 0
    line_count: int = 10


def build_tail_options(
    quiet: bool,
    verbose: bool,
    follow: bool,
    byte_count: int,
    line_count: int,
    multiple_files: bool = False,
) -> TailOptions:
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

    # @TODO: raise exception here if -f is passed with list of files?
    return TailOptions(quiet, verbose, follow, byte_count, line_count)


# ### files ###


def handle_single_file(file: str, tail_opts: TailOptions) -> None:
    if os.path.exists(file) is False:
        raise ValueError(f"tail: cannot open '{file}' for reading: No such file or directory")
    if os.path.isdir(file):
        if tail_opts.verbose:
            click.echo(f"==> {file} <==\n")
        raise ValueError(f"tail: error reading '{file}': Is a directory")

    if tail_opts.follow:
        return _follow_file(file, tail_opts)
    message = _build_message(file, tail_opts)
    click.echo(message)


def handle_file_list(file_list: tuple[str, ...], tail_opts: TailOptions) -> None:
    if tail_opts.follow:
        click.echo("following multiple files is not supported", err=True)

    for idx, file in enumerate(file_list):
        # @TODO: extract validation and use here and in handle_single_file
        if os.path.exists(file) is False:
            click.echo(
                f"tail: cannot open '{file}' for reading: No such file or directory", err=True
            )
            continue
        if os.path.isdir(file):
            if tail_opts.verbose:
                click.echo(f"==> {file} <==\n")
            click.echo(f"tail: error reading '{file}': Is a directory", err=True)
            continue

        # leave blank line before next file header
        if idx > 0:
            click.echo()
        message = _build_message(file, tail_opts)
        click.echo(message)


def read_from_sdtin(tail_opts: TailOptions) -> None:
    if tail_opts.verbose:
        click.echo("==> standard input <==")
    # NB: originally if -n is negative 'tail' enters an infinite loop
    if tail_opts.line_count <= 0:
        click.echo("Serriously?!")
        return
    # other options (line_count) are discarded
    if tail_opts.byte_count:
        # @FIXME:
        message = sys.stdin.buffer.readline()[: tail_opts.byte_count].decode()
        click.echo(message)
        return

    for _ in range(tail_opts.line_count):
        message = sys.stdin.readline().rstrip("\n")
        click.echo(message)


# ### result messages ###


def _build_message(file: str, tail_opts: TailOptions) -> str:
    if tail_opts.byte_count:
        with open(file, "rb") as f:
            # calculate and find offset
            f.seek(os.path.getsize(file) - tail_opts.byte_count)
            file_content = f.read().decode().rstrip("\n")
    else:
        with open(file, "r") as f:
            lines = f.readlines()[-tail_opts.line_count :]
        # remove final new line to mimic original message
        lines[-1] = lines[-1].rstrip("\n")
        file_content = "".join(lines)

    if tail_opts.verbose:
        return f"==> {file} <==\n" + file_content
    return file_content


def _follow_file(file: str, tail_opts: TailOptions):
    ...
