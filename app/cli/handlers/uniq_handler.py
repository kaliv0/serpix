import os

import click


class UniqHandler:
    def __init__(
        self,
        # multiple_files: bool,
        duplicates_count: bool,  # FIXME-> rename to show_dupl_count?
        show_repeated: bool,
        verbose: bool,
    ) -> None:
        # TODO: -ud returns nothing but could raise as well, -uc also (??)
        # if duplicates_count and all_duplicates
        # raise ValueError("uniq: printing all duplicated lines and repeat counts is meaningless")

        # setting uniq options
        self.duplicates_count = duplicates_count
        self.show_repeated = show_repeated
        self.verbose = verbose

    # ### files ###

    def handle_single_file(self, file: str) -> None:
        self._validate_file(file, raise_error=True)
        self._build_message(file)
        # message = self._build_message(file)
        # click.echo(message)

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

    def _build_message(self, file: str) -> None:  # FIXME: rename -> display_content
        if self.verbose:
            click.echo(f"==> {file} <==")

        counter = 1
        with open(file, "r") as f:
            curr_line = f.readline()
            while next_line := f.readline():
                if curr_line == next_line:
                    counter += 1
                else:
                    click.echo(f"{counter :>7} {curr_line}", nl=False)
                    counter = 1
                    curr_line = next_line
            click.echo(f"{counter :>7} {curr_line}", nl=False)

        # with open(file, "r") as f:
        #     lines = f.readlines()
        # # NB: originally uniq detects only adjacent duplicate files ->
        # # to achieve same behavior probably custom DSA instead of collections.Counter should be used?
        # cnt = collections.Counter(lines)  # FIXME rename

        # if self._opts_exist():
        #     # TODO: combine options
        #     file_content = self._build_message_from_options(cnt)
        # else:
        #     file_content = "".join(cnt)

        # if self.verbose:
        #     return f"==> {file} <==\n" + file_content.rstrip("\n")
        # # remove final new line to mimic original message
        # return file_content.rstrip("\n")

    # def _build_message_from_options(self, cnt: Counter) -> str:
    #     """
    #     -c, -u, -d, -D, -i
    #     -cu?, -cd, -ci, -cdi
    #     -ui, -di
    #     """

    #     if self.duplicates_count:
    #         return "".join([f"{v :>7} {k}" for k, v in cnt.items()])  # FIXME => :>8 as in wc?
    #     if self.show_repeated:
    #         return "".join([k for k, v in cnt.items() if v > 1])
    #     else:
    #         return ""  # TODO

    def _opts_exist(self) -> bool:
        return self.duplicates_count or self.show_repeated
