import os
import sys

import click


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
        self._validate_options(
            byte_count, char_count, field_count, delimiter, show_only_delimited_lines
        )
        # setting cut_options
        self.byte_count = self._read_range(byte_count) if byte_count else None
        self.char_count = self._read_range(char_count) if char_count else None
        self.field_count = self._read_range(field_count) if field_count else None

        self.delimiter = delimiter if delimiter else "\t"
        self.output_delimiter = output_delimiter if output_delimiter else self.delimiter
        self.show_only_delimited_lines = show_only_delimited_lines

    @staticmethod
    def _validate_options(
        byte_count, char_count, field_count, delimiter, show_only_delimited_lines
    ) -> None:
        if not (byte_count or char_count or field_count):
            raise ValueError("cut: you must specify a list of bytes, characters, or fields")
        if bool(byte_count) + bool(char_count) + bool(field_count) > 1:
            raise ValueError("cut: only one type of list may be specified")

        if delimiter:
            if len(delimiter) > 1:
                raise ValueError("cut: the delimiter must be a single character")
            if char_count or byte_count:
                raise ValueError(
                    "cut: an input delimiter may be specified only when operating on fields"
                )
        if show_only_delimited_lines and (char_count or byte_count):
            raise ValueError(
                "cut: suppressing non-delimited lines makes sense\n\tonly when operating on fields"
            )

    def _read_range(self, arg: str) -> slice:
        self._validate_range(arg)
        arg_list = arg.split("-")
        try:
            if len(arg_list) == 1:
                # NB-> original version starts from 1 and is inclusive range
                start = int(arg_list[0]) - 1
                stop = int(arg_list[0])
            else:
                start = int(arg_list[0]) - 1 if arg_list[0] else 0
                stop = int(arg_list[1]) if arg_list[1] else 10_000  # quasi Integer.MAX_VALUE
        except (ValueError, Exception):
            # raise error if 'start' or 'stop' are not valid integers
            raise ValueError(f"cut: invalid option value '{arg}'")
        return slice(start, stop)

    @staticmethod
    def _validate_range(arg: str) -> None:
        if arg == "-":
            raise ValueError(f"cut: invalid range with no endpoint: {arg}")
        elif arg.count("-") > 1:
            raise ValueError("cut: invalid range")

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
        curr_line = line.decode().rstrip()
        # check if non-delimited lines should be displayed
        if self.field_count is not None and self.delimiter not in curr_line:
            if not self.show_only_delimited_lines:
                click.echo(curr_line)
            return
        # cut selected part of text
        # NB: counts starts from zeroth index -> explicitly use 'is not None'
        if self.field_count is not None:
            curr_line = self.output_delimiter.join(
                curr_line.split(self.delimiter)[self.field_count]
            )
        elif self.char_count is not None:
            curr_line = curr_line[self.char_count]
        elif self.byte_count is not None:
            curr_line = line[self.byte_count].decode().rstrip()
        click.echo(curr_line)
