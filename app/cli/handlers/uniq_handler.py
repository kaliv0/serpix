import collections
import os

import click


class UniqHandler:
    def __init__(
        self,
        # multiple_files: bool,
        duplicates_count: bool,  # FIXME-> rename to show_dupl_count?
        show_repeated: bool,
    ) -> None:
        # setting uniq options
        self.duplicates_count = duplicates_count
        self.show_repeated = show_repeated

    # ### files ###

    def handle_single_file(self, file: str) -> None:
        self._validate_file(file, raise_error=True)
        message = self._build_message(file)
        click.echo(message)

    # ### validate path ###

    def _validate_file(self, file: str, raise_error: bool = False) -> bool:
        if os.path.exists(file) is False:
            message = f"uniq: {file}: No such file or directory"
            if raise_error:
                raise ValueError(message)
            click.echo(message, err=True)
            return False

        if os.path.isdir(file):
            # if self.verbose:
            # click.echo(f"==> {file} <==\n")
            message = f"head: error reading '{file}'"
            if raise_error:
                raise ValueError(message)
            click.echo(message, err=True)
            return False
        return True

    # ### result messages ###

    def _build_message(self, file: str) -> str:
        with open(file, "r") as f:
            lines = f.readlines()
        cnt = collections.Counter(lines)  # FIXME rename
        # TODO: combine options
        if self.duplicates_count:
            file_content = "".join(
                [f"{v :>7} {k}" for k, v in cnt.items()]
            )  # FIXME => :>8 as in wc?
        elif self.show_repeated:
            file_content = "".join([k for k, v in cnt.items() if v > 1])
        else:
            file_content = "".join(cnt)

        # if self.verbose:
        # return f"==> {file} <==\n" + file_content
        # remove final new line to mimic original message
        return file_content.rstrip("\n")
