import os
import sys

import click


class FileData:
    def __init__(self, file_name="") -> None:
        self.byte_count = 0
        self.line_count = 0
        self.word_count = 0
        self.char_count = 0
        self.file_name = file_name

    def extract_from_file(self, file: str, is_empty_file_list: bool = False) -> None:
        if file != "-":
            with open(file, "rb") as f:
                for line in f:
                    self._update_file_data(line)
        else:
            for line in sys.stdin.buffer:
                self._update_file_data(line)

        if not is_empty_file_list:
            self.file_name = file

    def _update_file_data(self, line: bytes) -> None:
        self.byte_count += len(line)
        self.word_count += len(line.split())
        decoded_line = line.decode()
        self.char_count += len(decoded_line)
        if decoded_line.endswith("\n"):
            self.line_count += 1


class WCHandler:
    def __init__(
        self, show_lines: bool, show_words: bool, show_chars: bool, show_bytes: bool
    ) -> None:
        # setting wc_options
        self.show_lines = show_lines
        self.show_words = show_words
        self.show_chars = show_chars
        self.show_bytes = show_bytes

    def _opts_exist(self) -> bool:
        if (
            not self.show_lines
            and not self.show_words
            and not self.show_chars
            and not self.show_bytes
        ):
            return False
        return True

    # ### files ###

    def handle_file_list(self, file_list: tuple[str, ...]) -> None:
        total_data = FileData(file_name="total")
        for file in file_list:
            if file != "-" and os.path.exists(file) is False:
                click.echo(f"wc: {file}: No such file or directory", err=True)
                continue

            data = FileData()
            data.extract_from_file(file)
            if self._opts_exist() is False:
                self._update_total_data_no_opts(data, total_data)
                message = self._build_default_message(data)
            else:
                self._update_total_data(data, total_data)
                message = self._build_message_from_options(data)
            click.echo(message)

        total_message = self._build_total_message(total_data)
        click.echo(total_message)

    def handle_single_file(self, file_list: tuple[str, ...]) -> None:
        file, is_empty_file_list = self._get_file_name(file_list)
        if file != "-" and os.path.exists(file) is False:
            raise ValueError(f"wc: {file}: No such file or directory")

        data = FileData()
        data.extract_from_file(file, is_empty_file_list)
        if self._opts_exist() is False:
            message = self._build_default_message(data)
        else:
            message = self._build_message_from_options(data)
        click.echo(message)

    def _get_file_name(self, file_list: tuple[str, ...]) -> tuple[str, bool]:
        if len(file_list) == 1:
            return file_list[0], False
        return "-", True

    # ### result messages ###

    def _build_message_from_options(self, data: FileData) -> str:
        message = ""
        if self.show_lines:
            message += f"{data.line_count :>8} "
        if self.show_words:
            message += f"{data.word_count :>8} "
        if self.show_chars:
            message += f"{data.char_count :>8} "
        if self.show_bytes:
            message += f"{data.byte_count :>8} "
        if data.file_name:
            message += f"{data.file_name :<8}"
        return message

    def _build_default_message(self, data: FileData) -> str:
        message = f"{data.line_count :>8} {data.word_count :>8} {data.byte_count :>8} "
        if data.file_name:
            message += f"{data.file_name :<8}"
        return message

    def _build_total_message(self, total_data: FileData) -> str:
        if self._opts_exist() is False:
            return f"{total_data.line_count :>8} {total_data.word_count :>8} {total_data.byte_count :>8} {'total' :<8}"
        return self._build_message_from_options(total_data)

    # @FIXME: extract as separate function outside class?
    # ### total file_data ###

    def _update_total_data(self, curr_data: FileData, total_data: FileData) -> None:
        if self.show_lines:
            total_data.line_count += curr_data.line_count
        if self.show_words:
            total_data.word_count += curr_data.word_count
        if self.show_chars:
            total_data.char_count += curr_data.char_count
        if self.show_bytes:
            total_data.byte_count += curr_data.byte_count

    def _update_total_data_no_opts(self, curr_data: FileData, total_data: FileData) -> None:
        total_data.line_count += curr_data.line_count
        total_data.word_count += curr_data.word_count
        total_data.byte_count += curr_data.byte_count
