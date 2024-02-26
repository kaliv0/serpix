import os
import sys

import click


# @TODO: cut- and cat-handlers (others as well) share same methods
#   -> e.g. handle_file_list, get_file_name etc
#   refactor 'OOP style'
class CutHandler:
    def __init__(
        self,
        byte_count: str,
        char_count: str,
        field_count: str,
        delimiter: str,
        output_delimiter: str,
        show_only_delimited_lines: bool,
    ) -> None:
        if not (byte_count or char_count or field_count):
            raise ValueError("cut: you must specify a list of bytes, characters, or fields")

        # @ FIXME: check this bitwise :P
        # if (
        #     (byte_count and char_count)
        #     or (char_count and field_count)
        #     or (byte_count and field_count)
        # ):
        if bool(byte_count) + bool(char_count) + bool(field_count) > 1:
            raise ValueError("cut: only one type of list may be specified")

        if len(delimiter) != 1:
            raise ValueError("cut: the delimiter must be a single character")

        # setting cut_options
        self.byte_count = byte_count
        self.char_count = char_count
        self.field_count = field_count
        self.delimiter = delimiter
        self.show_only_delimited_lines = show_only_delimited_lines

        self.output_delimiter = output_delimiter if output_delimiter else delimiter  # @FIXME

    def handle_file_list(self, file_list: tuple[str, ...]) -> None:
        for file in file_list:
            if file == "-":
                for line in sys.stdin.buffer:
                    self._handle_file_line(line)
            else:
                if os.path.exists(file) is False:
                    click.echo(f"cut: {file}: No such file or directory", err=True)
                    continue
                with open(file, "rb") as f:
                    for line in f:
                        self._handle_file_line(line)

    def handle_single_file(self, file_list: tuple[str, ...]) -> None:
        file = self._get_file_name(file_list)
        if file == "-":
            for line in sys.stdin.buffer:
                self._handle_file_line(line)
        else:
            if os.path.exists(file) is False:
                raise ValueError(f"cut: {file}: No such file or directory")
            with open(file, "rb") as f:
                for line in f:
                    self._handle_file_line(line)

    @staticmethod
    def _get_file_name(file_list: tuple[str, ...]) -> str:
        if len(file_list) == 1:
            return file_list[0]
        return "-"

    def _handle_file_line(self, line: bytes) -> None:
        message = ""
        curr_line = line.decode().rstrip()

        if self.show_only_delimited_lines and self.delimiter not in curr_line:
            return
        curr_line = curr_line.split(self.delimiter)

        message = self.output_delimiter.join(curr_line)
        click.echo(message)
