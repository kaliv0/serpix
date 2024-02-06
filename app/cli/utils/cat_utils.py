import os
import sys
from dataclasses import dataclass

import click

# ### cat_options ###


@dataclass
class CatOptions:
    show_all_line_numbers: bool
    # @TODO: -b overrides -n
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

    # data = extract_file_data(file, is_empty_file_list)
    # if cat_opts is None:
    #     message = _build_default_message(data)
    # else:
    #     message = _build_message_from_options(data, cat_opts)
    # click.echo(message)

    if file and file != "-":
        with open(file, "rb") as f:
            for idx, line in enumerate(f, start=1):
                message = line.decode().rstrip()
                if cat_opts and cat_opts.show_all_line_numbers:
                    message = f"{idx :>6} " + message
                click.echo(message)
    else:
        for line in sys.stdin.buffer:
            # _update_file_data(line, data)
            ...


def _get_file_name(file_list: tuple[str, ...]) -> str:
    if len(file_list) == 1:
        return file_list[0]
    return "-"
