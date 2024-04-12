import os

import click


class UniqHandler:
    def __init__(
        self,
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
        # setting uniq options
        self.show_count = show_count
        self.show_unique = show_unique
        self.show_repeated = show_repeated
        self.show_all_repeated = show_all_repeated
        self.ignore_case = ignore_case
        self.check_chars = check_chars
        self.skip_chars = skip_chars

    # ### files ###

    def handle_file(self, file_list: tuple[str, ...]) -> None:
        file = self._get_file_name(file_list)
        self._validate_file(file)
        self._process_file(file)

    def _get_file_name(self, file_list: tuple[str, ...]) -> str:
        if not file_list:
            raise ValueError("uniq: reading INPUT from stdin is not supported")
        if len(file_list) > 1:
            raise ValueError("uniq: saving logs to OUTPUT destination is not supported")
        file = file_list[0]
        return file

    # ### validate path ###

    def _validate_file(self, file: str) -> bool:
        if os.path.exists(file) is False:
            raise ValueError(f"uniq: {file}: No such file or directory")
        if os.path.isdir(file):
            raise ValueError(f"uniq: error reading '{file}'")
        return True

    # ### result messages ###

    def _process_file(self, file: str) -> None:
        with open(file, "r") as f:
            counter = 1
            curr_line = f.readline()
            while next_line := f.readline():
                # count duplicates until different line is reached
                if self._compare_lines(curr_line, next_line):
                    counter += 1
                    if self.show_all_repeated:
                        click.echo(curr_line, nl=False)
                    continue
                # previous line is different compared to next_one
                # but 'uniq' only if not last in series of duplicates
                self._handle_message(counter, curr_line)
                counter = 1
                curr_line = next_line
            # handle last line in file
            self._handle_message(counter, curr_line)

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
            click.echo(message, nl=False)

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
