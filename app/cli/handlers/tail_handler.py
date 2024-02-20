import io
import os
import sys
import time
from typing import NoReturn

import click


class TailHandler:
    def __init__(
        self,
        quiet: bool,
        verbose: bool,
        follow: bool,
        byte_count: int = 0,
        line_count: int = 10,
        multiple_files: bool = False,
    ) -> None:
        # NB: in the original if -v and -q are passed simultaneously
        # the second option overrides the first one
        if quiet and verbose:
            raise ValueError("Contradicting flags passed: 'quiet' and 'verbose'")
        # adjust header options if none are passed
        if not quiet and not verbose:
            if multiple_files:
                verbose = True
            else:
                quiet = True

        if multiple_files and follow:
            raise ValueError("tail: following multiple files is not supported")

        # setting tail_options
        self.quiet = quiet
        self.verbose = verbose
        self.follow = follow
        self.byte_count = byte_count
        self.line_count = line_count
        self.sleep_interval = 1  # @FIXME: extract as class const?

    # ### files ###

    def handle_single_file(self, file: str) -> None:
        self._validate_file(file, raise_error=True)
        if self.follow:
            self._follow_file(file)
        else:
            message = self._build_message(file)
            click.echo(message)

    def handle_file_list(self, file_list: tuple[str, ...]) -> None:
        for idx, file in enumerate(file_list):
            if self._validate_file(file) is False:
                continue
            # leave blank line before next file header
            if idx > 0:
                click.echo()
            message = self._build_message(file)
            click.echo(message)

    def read_from_stdin(self) -> None:
        if self.verbose:
            click.echo("==> standard input <==")
        # NB: originally if -n is negative 'tail' enters an infinite loop
        if self.line_count <= 0:
            click.echo("Seriously?!")
            return
        # other options (line_count) are discarded
        if self.byte_count:
            # @FIXME:
            message = sys.stdin.buffer.readline()[: self.byte_count].decode()
            click.echo(message)
            return

        for _ in range(self.line_count):
            message = sys.stdin.readline().rstrip("\n")
            click.echo(message)

    # ### validate path ###
    def _validate_file(self, file: str, raise_error: bool = False) -> bool:
        if os.path.exists(file) is False:
            message = f"tail: cannot open '{file}' for reading: No such file or directory"
            if raise_error:
                raise ValueError(message)
            click.echo(message, err=True)
            return False

        if os.path.isdir(file):
            if self.verbose:
                click.echo(f"==> {file} <==\n")
            message = f"tail: error reading '{file}': Is a directory"
            if raise_error:
                raise ValueError(message)
            click.echo(message, err=True)
            return False
        return True

    # ### result messages ###

    def _build_message(self, file: str) -> str:
        if self.byte_count:
            with open(file, "rb") as f:
                # calculate and find offset
                f.seek(os.path.getsize(file) - self.byte_count)
                file_content = f.read().decode().rstrip("\n")
        else:
            with open(file, "r") as f:
                lines = f.readlines()[-self.line_count :]
            # remove final new line to mimic original message
            lines[-1] = lines[-1].rstrip("\n")
            file_content = "".join(lines)

        if self.verbose:
            return f"==> {file} <==\n" + file_content
        return file_content

    def _follow_file(self, file: str) -> NoReturn:
        # NB: lines/bytes offset is supported in the original command but ignored here
        if self.verbose:
            click.echo(f"==> {file} <==")
        with open(file) as f:
            f.seek(0, io.SEEK_END)
            while True:
                curr_position = f.tell()
                line = f.readline()
                if not line:
                    f.seek(curr_position)
                    time.sleep(self.sleep_interval)
                else:
                    click.echo(line.rstrip())
