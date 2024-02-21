import os
import sys

import click


class CatHandler:
    def __init__(
        self,
        show_all_line_numbers: bool,
        show_nonempty_line_numbers: bool,
        squeeze_blank: bool,
        show_ends: bool,
        show_tabs: bool,
        show_all: bool,
    ) -> None:
        # NB: in the original if -n and -b are passed simultaneously
        # option -b overrides -n
        if show_all_line_numbers and show_nonempty_line_numbers:
            raise ValueError("Contradicting flags passed: 'number' and 'number-nonblank'")

        # setting cat_options
        self.show_all_line_numbers = show_all_line_numbers
        self.show_nonempty_line_numbers = show_nonempty_line_numbers
        self.squeeze_blank = squeeze_blank
        if show_all:
            self.show_ends = True
            self.show_tabs = True
        else:
            self.show_ends = show_ends
            self.show_tabs = show_tabs

        # helper variables used with options
        self.line_number = 1
        self.previous_line = None

    def _opts_exist(self) -> bool:
        return (
            self.show_all_line_numbers
            or self.show_nonempty_line_numbers
            or self.squeeze_blank
            or self.show_ends
            or self.show_tabs
        )

    def handle_file_list(self, file_list: tuple[str, ...]) -> None:
        for file in file_list:
            if file == "-":
                for line in sys.stdin.buffer:
                    self._handle_file_line(line)
            else:
                if os.path.exists(file) is False:
                    click.echo(f"cat: {file}: No such file or directory", err=True)
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
                raise ValueError(f"cat: {file}: No such file or directory")
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
        message = curr_line
        if self._opts_exist():
            # @TODO: extract as separate method for handling empty lines
            # together with keeping track of current/previous line
            if self.squeeze_blank and curr_line == "" and self.previous_line == "":
                self.previous_line = curr_line
                return
            if (self.show_nonempty_line_numbers and message) or self.show_all_line_numbers:
                message = f"{self.line_number :>6} " + message
                self.line_number += 1
            if self.show_ends:
                message += "$"
            if self.show_tabs:
                message = message.replace("    ", "^")
        click.echo(message)
        self.previous_line = curr_line
