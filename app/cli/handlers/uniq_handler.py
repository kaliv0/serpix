import os
from typing import TextIO

import click


class UniqHandler:
    def __init__(
        self,
        file_list: tuple[str, ...],
        show_count: bool,
        show_unique: bool,
        show_repeated: bool,
        show_all_repeated: bool,
        ignore_case: bool,
        check_chars: int,
        skip_chars: int,
    ) -> None:
        self._validate_opts(
            show_count, show_unique, show_repeated, show_all_repeated, check_chars, skip_chars
        )
        # setting input|output files
        file_path, output_path = self._get_io_paths(file_list)
        self.file_path = file_path
        self.output_path = output_path
        # setting uniq options
        self.show_count = show_count
        self.show_unique = show_unique
        self.show_repeated = show_repeated
        self.show_all_repeated = show_all_repeated
        self.ignore_case = ignore_case
        self.check_chars = check_chars
        self.skip_chars = skip_chars

    # ### files ###

    def _get_io_paths(self, file_list: tuple[str, ...]) -> tuple[str, TextIO | None]:
        file, output_path = self._get_file_names(file_list)
        self._validate_file(file)

        output = None
        if self._validate_output_path(output_path):
            output = self._get_output_file(output_path)
        return file, output

    def _get_file_names(self, file_list: tuple[str, ...]) -> tuple[str, str | None]:
        if not file_list or file_list[0] == "-":
            raise ValueError("uniq: reading INPUT from stdin is not supported")
        if len(file_list) > 2:
            raise ValueError(f"uniq: extra operand ‘{file_list[2]}’")
        if len(file_list) == 2:
            return file_list[0], file_list[1]
        return file_list[0], None

    @staticmethod
    def _get_output_file(path: str) -> TextIO:
        output = open(path, "a+")
        # erase output content if exists
        output.truncate(0)
        return output

    # ### validate path ###

    def _validate_file(self, file: str) -> None:
        if os.path.exists(file) is False:
            raise ValueError(f"uniq: {file}: No such file or directory")
        if os.path.isdir(file):
            raise ValueError(f"uniq: error reading '{file}'")

    def _validate_output_path(self, path: str | None) -> bool:
        if path is None or path == "-":
            return False
        if os.path.isdir(path):
            raise ValueError(f"uniq: {path}: Is a directory")
        return True

    # ### result messages ###

    def process_file(self) -> None:
        file = open(self.file_path, "r")
        counter = 1
        curr_line = file.readline()
        while next_line := file.readline():
            # count duplicates until different line is reached
            if self._compare_lines(curr_line, next_line):
                counter += 1
                if self.show_all_repeated:
                    self._handle_message(counter, curr_line)
                    curr_line = next_line
                continue
            # previous line is different compared to next_one
            # but 'uniq' only if not last in series of duplicates
            self._handle_message(counter, curr_line)
            counter = 1
            curr_line = next_line
        # handle last line in file
        self._handle_message(counter, curr_line)
        file.close()
        if self.output_path:
            self.output_path.close()

    def _compare_lines(self, current: str, next: str) -> bool:
        if self.check_chars:
            current = current[0 : self.check_chars]
            next = next[0 : self.check_chars]
        if self.skip_chars:
            current = current[self.skip_chars :]
            next = next[self.skip_chars :]
        if self.ignore_case:
            return current.upper() == next.upper()
        return current == next

    def _handle_message(self, counter: int, curr_line: str) -> None:
        message = f"{curr_line}"
        if self.show_count:
            message = f"{counter :>7} " + message
        if self._should_print_message(counter):
            click.echo(message, nl=False, file=self.output_path)

    def _should_print_message(self, counter: int) -> bool:
        if self.show_unique:
            return counter == 1
        if self.show_repeated or self.show_all_repeated:
            return counter > 1
        # default behavior
        if not (self.show_unique or self.show_repeated or self.show_all_repeated):
            return True
        return False

    # ### validate options ###

    def _validate_opts(
        self,
        show_count: bool,
        show_unique: bool,
        show_repeated: bool,
        show_all_repeated: bool,
        check_chars: int,
        skip_chars: int,
    ) -> None:
        if show_count and (show_unique or show_all_repeated):
            raise ValueError("uniq: printing all lines and repeat counts is meaningless")
        if show_unique and (show_repeated or show_all_repeated):
            raise ValueError("uniq: meaningless flag combination")
        if check_chars and skip_chars:
            raise ValueError("uniq: unsupported flag combination")
