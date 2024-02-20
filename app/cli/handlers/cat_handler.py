import os
import sys

import click


class CatHandler:
    def __init__(self, show_all_line_numbers: bool, show_nonempty_line_numbers: bool) -> None:
        # NB: in the original if -n and -b are passed simultaneously
        # option -b overrides -n
        if show_all_line_numbers and show_nonempty_line_numbers:
            raise ValueError("Contradicting flags passed: 'number' and 'number-nonblank'")

        # setting cat_options
        self.show_all_line_numbers = show_all_line_numbers
        self.show_nonempty_line_numbers = show_nonempty_line_numbers
        self.line_number = 1

    def _opts_exist(self) -> bool:
        return self.show_all_line_numbers or self.show_nonempty_line_numbers

    def handle_file_list(self, file_list: tuple[str, ...]) -> None:
        ...

    def handle_single_file(self, file_list: tuple[str, ...]) -> None:
        file = self._get_file_name(file_list)
        # @FIXME: refactor using if file != "-" twice
        if file != "-" and os.path.exists(file) is False:
            raise ValueError(f"cat: {file}: No such file or directory")

        if file != "-":
            with open(file, "rb") as f:
                for line in f:
                    self._handle_file_line(line)
        else:
            for line in sys.stdin.buffer:
                self._handle_file_line(line)

    @staticmethod
    def _get_file_name(file_list: tuple[str, ...]) -> str:
        if len(file_list) == 1:
            return file_list[0]
        return "-"

    def _handle_file_line(self, line: bytes) -> None:
        message = line.decode().rstrip()
        if self._opts_exist():
            if (self.show_nonempty_line_numbers and message) or self.show_all_line_numbers:
                message = f"{self.line_number :>6} " + message
                self.line_number += 1
        click.echo(message)
