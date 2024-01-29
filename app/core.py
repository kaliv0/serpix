import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class FileData:
    byte_count: int
    line_count: int
    word_count: int
    char_count: int
    file_name: str


def extract_file_data(file: str) -> FileData:
    if "-" in file:
        file_name = "-"
    else:
        file_name = file[0]

    bytes_count = 0
    lines_count = 0
    words_count = 0
    chars_count = 0
    if file_name and not file_name == "-":
        with open(file_name, "rb") as f:
            for line in f:
                bytes_count += len(line)
                lines_count += 1
                words_count += len(line.split())
                # NB: If the current locale does not support multibyte characters this will match the bytes_count.
                chars_count += len(line.decode())
    else:
        for line in sys.stdin.buffer:
            bytes_count += len(line)
            lines_count += 1
            words_count += len(line.split())
            chars_count += len(line.decode())
    return FileData(bytes_count, lines_count, words_count, chars_count, file_name)
