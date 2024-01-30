import sys
from dataclasses import dataclass


@dataclass
class FileData:
    byte_count: int
    line_count: int
    word_count: int
    char_count: int
    file_name: str


def extract_file_data(file: str, is_empty_file_list: bool = False) -> FileData:
    data = FileData(0, 0, 0, 0, "")
    if file and file != "-":
        with open(file, "rb") as f:
            for line in f:
                update_file_data(line, data)
    else:
        for line in sys.stdin.buffer:
            update_file_data(line, data)

    if not is_empty_file_list:
        data.file_name = file
    return data


def update_file_data(line: bytes, data: FileData) -> None:
    data.byte_count += len(line)
    data.word_count += len(line.split())
    decoded_line = line.decode()
    data.char_count += len(decoded_line)
    if decoded_line.endswith("\n"):
        data.line_count += 1
