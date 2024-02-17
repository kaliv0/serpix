import os
import subprocess
import sys
from dataclasses import dataclass

import click

# ### cat_options ###


@dataclass
class CatOptions:
    show_all_line_numbers: bool
    show_nonempty_line_numbers: bool


def build_cat_options(
    show_all_line_numbers: bool, show_nonempty_line_numbers: bool
) -> CatOptions | None:
    if not show_all_line_numbers and not show_nonempty_line_numbers:
        return None
    return CatOptions(show_all_line_numbers, show_nonempty_line_numbers)


def handle_file_list(file_list: tuple[str, ...], cat_opts: CatOptions | None) -> None:
    ...


def handle_single_file(file_list: tuple[str, ...], cat_opts: CatOptions | None) -> None:
    file = _get_file_name(file_list)
    if file != "-" and os.path.exists(file) is False:
        raise ValueError(f"cat: {file}: No such file or directory")

    # @FIXME: refactor using Cat class -> idx as attribute
    global idx
    idx = 1
    if file != "-":
        with open(file, "rb") as f:
            for line in f:
                _handle_file_line(line, cat_opts)
    else:
        for line in sys.stdin.buffer:
            _handle_file_line(line, cat_opts)


def _get_file_name(file_list: tuple[str, ...]) -> str:
    if len(file_list) == 1:
        return file_list[0]
    return "-"


def _handle_file_line(line: bytes, cat_opts: CatOptions | None) -> None:
    global idx
    message = line.decode().rstrip()
    if cat_opts:
        if cat_opts.show_nonempty_line_numbers and message:
            message = f"{idx :>6} " + message
            idx += 1
        elif cat_opts.show_all_line_numbers:
            message = f"{idx :>6} " + message
            idx += 1
    click.echo(message)


def seed_file_from_stdin(file: str) -> None:
    with subprocess.Popen("cat", stdout=subprocess.PIPE) as proc:
        if proc.stdout:
            with open("./res.txt", "w") as f:
                for line in proc.stdout.readlines():
                    f.write(line.decode())
