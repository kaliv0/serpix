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


def build_head_options(
    byte_count: int, line_count: int, quiet: bool, verbose: bool, multiple_files: bool = False
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

    return HeadOptions(byte_count, line_count, quiet, verbose)


# ### files ###


def handle_single_file(file: str, head_opts: HeadOptions) -> None:
    if os.path.exists(file) is False:
        raise ValueError(f"head: cannot open '{file}' for reading: No such file or directory")
    message = _build_message(file, head_opts)
    click.echo(message)


def handle_file_list(file_list: tuple[str, ...], head_opts: HeadOptions) -> None:
    for idx, file in enumerate(file_list):
        if os.path.exists(file) is False:
            click.echo(
                f"head: cannot open '{file}' for reading: No such file or directory", err=True
            )
            continue
        message = _build_message(file, head_opts)
        click.echo(message)
        # leave blank line before next file header @FIXME
        if idx < len(file_list) - 1:
            click.echo()


# ### result messages ###


def _build_message(file: str, head_opts: HeadOptions) -> str:
    # @FIXME string list manipulation -> split + join?!
    if head_opts.byte_count:
        with open(file, "rb") as f:
            file_content = f.read(head_opts.byte_count).decode().rstrip("\n")
    else:
        with open(file, "r") as f:
            lines = f.readlines()[: head_opts.line_count]
        # remove final new line to mimic original message
        lines[-1] = lines[-1].rstrip("\n")
        file_content = "".join(lines)
    message = ""
    if head_opts.verbose:
        message += f"==> {file} <==\n"
    return message + file_content
