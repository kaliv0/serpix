import os
from dataclasses import dataclass

import click

# ### head_options ###


@dataclass
class HeadOptions:
    byte_count: int
    line_count: int
    quiet: bool
    verbose: bool


def build_head_options(byte_count: int, line_count: int, quiet: bool, verbose: bool) -> HeadOptions:
    # NB: in the original if -v and -q are passed simultaneously
    # the second option overrides the first one
    if quiet and verbose:
        raise ValueError("Contradicting flags passed: 'quiet' and 'verbose'")

    if not quiet and not verbose:
        quiet = True
    return HeadOptions(byte_count, line_count, quiet, verbose)


# ### files ###


def handle_single_file(file: str, head_opts: HeadOptions) -> None:
    if os.path.exists(file) is False:
        raise ValueError(f"head: cannot open '{file}' for reading: No such file or directory")

    message = _build_message(file, head_opts)
    click.echo(message)


# ### result messages ###


def _build_message(file: str, head_opts: HeadOptions) -> str:
    with open(file, "r") as f:
        lines = f.readlines()[: head_opts.line_count]
        # remove final new line to mimic original message
        lines[-1] = lines[-1].rstrip("\n")

        message = ""
        if head_opts.verbose:
            message += f"==> {file} <==\n"
        return message + "".join(lines)  # @FIXME
