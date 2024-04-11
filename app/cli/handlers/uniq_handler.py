import os
from io import TextIOWrapper

import click


class UniqHandler:
    def __init__(
        self,
        show_count: bool,
        show_unique: bool,
        show_repeated: bool,
        show_all_repeated: bool,
        ignore_case: bool,
        verbose: bool,
    ) -> None:
        self._validate_opts(show_count, show_unique, show_repeated, show_all_repeated)
        # setting uniq options
        self.show_count = show_count
        self.show_unique = show_unique
        self.show_repeated = show_repeated
        self.show_all_repeated = show_all_repeated
        self.ignore_case = ignore_case
        self.verbose = verbose

    # ### files ###

    def handle_single_file(self, file: str) -> None:
        self._validate_file(file, raise_error=True)
        self._process_file(file)

    # ### validate path ###

    def _validate_file(self, file: str, raise_error: bool = False) -> bool:
        if os.path.exists(file) is False:
            message = f"uniq: {file}: No such file or directory"
            if raise_error:
                raise ValueError(message)
            click.echo(message, err=True)
            return False

        if os.path.isdir(file):
            if self.verbose:
                click.echo(f"==> {file} <==\n")
            message = f"head: error reading '{file}'"
            if raise_error:
                raise ValueError(message)
            click.echo(message, err=True)
            return False
        return True

    # ### result messages ###

    def _process_file(self, file: str) -> None:
        if self.verbose:
            click.echo(f"==> {file} <==")  # add \n?

        with open(file, "r") as f:
            return self._display_lines(f)

    def _display_lines(self, file: TextIOWrapper) -> None:  # TODO: works only for -u and -d
        counter = 1
        curr_line = file.readline()
        while next_line := file.readline():
            # count duplicates until different line is reached
            if self.compare_lines(curr_line, next_line):
                counter += 1
                curr_line = next_line
                continue
            # previous line is different compared to next_one
            # but 'uniq' only if not last in series of duplicates
            message = f"{curr_line}"  # TODO: extract handle message -> nest adding count inside if_should_print
            if self.show_count:
                message = f"{counter :>7} " + message
            if self.should_print_message(counter):
                click.echo(message, nl=False)
            counter = 1
            curr_line = next_line
        # handle last line in file
        message = f"{curr_line}"
        if self.show_count:
            message = f"{counter :>7} " + message
        if self.should_print_message(counter):
            click.echo(message, nl=False)

    def compare_lines(self, current: str, next: str) -> bool:
        if self.ignore_case:
            return current.upper() == next.upper()
        return current == next

    def should_print_message(self, counter: int) -> bool:
        if self.show_unique:
            return counter == 1
        if self.show_repeated:
            return counter > 1
        return False

    # ### validate options ###

    def _validate_opts(self, show_count, show_unique, show_repeated, show_all_repeated) -> None:
        if show_count:
            if show_all_repeated:
                raise ValueError(
                    "uniq: printing all duplicated lines and repeat counts is meaningless"
                )
            elif show_unique:
                raise ValueError("uniq: printing all uniq lines and repeat counts is meaningless")
        if show_unique and (show_repeated or show_all_repeated):
            raise ValueError("uniq: meaningless flag combination")

    def _opts_exist(self) -> bool:
        return self.show_count or self.show_repeated
