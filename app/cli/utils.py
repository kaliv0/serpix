import os
import sys
from dataclasses import dataclass

import click


@dataclass
class FileData:
    byte_count: int
    line_count: int
    word_count: int
    char_count: int
    file_name: str


def extract_file_data(file: str, is_empty_file_list: bool = False) -> FileData:
    data = FileData(0, 0, 0, 0, "")
    if file and file != "-":
        with open(file, "rb") as f:
            for line in f:
                update_file_data(line, data)
    else:
        for line in sys.stdin.buffer:
            update_file_data(line, data)

    if not is_empty_file_list:
        data.file_name = file
    return data


def update_file_data(line: bytes, data: FileData) -> None:
    data.byte_count += len(line)
    data.word_count += len(line.split())
    decoded_line = line.decode()
    data.char_count += len(decoded_line)
    if decoded_line.endswith("\n"):
        data.line_count += 1


@dataclass
class WCOptions:
    show_lines: bool
    show_words: bool
    show_chars: bool
    show_bytes: bool


def build_wc_options(
    show_lines: bool, show_words: bool, show_chars: bool, show_bytes: bool
) -> WCOptions | None:
    if not show_lines and not show_words and not show_chars and not show_bytes:
        return None
    return WCOptions(show_lines, show_words, show_chars, show_bytes)


def handle_file_list(file_list: tuple[str, ...], wc_opts: WCOptions | None) -> None:
    total_data = FileData(0, 0, 0, 0, "total")
    for file in file_list:
        if file != "-" and os.path.exists(file) is False:
            click.echo(f"wc: {file}: No such file or directory")
            continue

        data = extract_file_data(file)
        if wc_opts is None:
            update_total_data_no_opts(data, total_data)
            message = build_message_no_options(data)
        else:
            update_total_data(wc_opts, data, total_data)
            message = build_message_from_options(data, wc_opts)
        click.echo(message)

    total_message = build_total_message(total_data, wc_opts)
    click.echo(total_message)


def handle_single_file(file_list: tuple[str, ...], wc_opts: WCOptions | None) -> None:
    file, is_empty_file_list = get_file_name(file_list)
    if file != "-" and os.path.exists(file) is False:
        click.echo(f"wc: {file}: No such file or directory")
        return

    data = extract_file_data(file, is_empty_file_list)
    if wc_opts is None:
        message = build_default_message(data)
    else:
        message = build_message_from_options(data, wc_opts)
    click.echo(message)


def get_file_name(file_list: tuple[str, ...]) -> tuple[str, bool]:
    if len(file_list) == 1:
        return file_list[0], False
    return "-", True


def build_message_from_options(data: FileData, wc_opts: WCOptions) -> str:
    message = ""
    if wc_opts.show_lines:
        message += f"{data.line_count :>8} "
    if wc_opts.show_words:
        message += f"{data.word_count :>8} "
    if wc_opts.show_chars:
        message += f"{data.char_count :>8} "
    if wc_opts.show_bytes:
        message += f"{data.byte_count :>8} "
    if data.file_name:
        message += f"{data.file_name :<8}"
    return message


def build_message_no_options(data: FileData) -> str:
    message = f"{data.line_count :>8} {data.word_count :>8} {data.byte_count :>8} "
    if data.file_name:
        message += f"{data.file_name :<8}"
    return message


def build_default_message(data: FileData) -> str:
    message = f"{data.line_count :>8} {data.word_count :>8} {data.byte_count :>8} "
    if data.file_name:
        message += f"{data.file_name :<8}"
    return message


def build_total_message(total_data: FileData, wc_opts: WCOptions | None) -> str:
    if wc_opts is None:
        return f"{total_data.line_count :>8} {total_data.word_count :>8} {total_data.byte_count :>8} {'total' :<8}"
    return build_message_from_options(total_data, wc_opts)


def update_total_data(wc_opts: WCOptions, curr_data: FileData, total_data: FileData) -> None:
    if wc_opts.show_lines:
        total_data.line_count += curr_data.line_count
    if wc_opts.show_words:
        total_data.word_count += curr_data.word_count
    if wc_opts.show_chars:
        total_data.char_count += curr_data.char_count
    if wc_opts.show_bytes:
        total_data.byte_count += curr_data.byte_count


def update_total_data_no_opts(curr_data: FileData, total_data: FileData) -> None:
    total_data.line_count += curr_data.line_count
    total_data.word_count += curr_data.word_count
    total_data.byte_count += curr_data.byte_count
