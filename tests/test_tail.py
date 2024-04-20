import subprocess

import pytest
from click.testing import CliRunner

from app.cli.commands import tail

LOG_FILE = "tests/resources/common/log.txt"
POEM_FILE = "tests/resources/common/poem.txt"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"
DIR_PATH = "test/resources/"


runner = CliRunner()


@pytest.mark.parametrize("file", [LOG_FILE, POEM_FILE])
def test_tail_no_options(file) -> None:
    assert runner.invoke(tail, [file]).output.rstrip("\n") == subprocess.run(
        ["tail", file], capture_output=True, text=True
    ).stdout.rstrip("\n")


@pytest.mark.parametrize(
    "tail_options, file",
    [
        ("-n3", LOG_FILE),
        ("-n-3", LOG_FILE),
        ("-c40", LOG_FILE),
    ],
)
def test_tail(tail_options, file) -> None:
    assert runner.invoke(tail, [tail_options, file]).output.rstrip("\n") == subprocess.run(
        ["tail", tail_options, file], capture_output=True, text=True
    ).stdout.rstrip("\n")


def test_tail_error_message() -> None:
    expected_value_error = "Contradicting flags passed: 'quiet' and 'verbose'"
    assert runner.invoke(tail, ["-qv", LOG_FILE]).exception.args[0] == expected_value_error  # type: ignore


def test_tail_file_list_no_options() -> None:
    expected_multiple_no_opts = """==> tests/resources/common/log.txt <==
Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

==> tests/resources/common/poem.txt <==

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert runner.invoke(tail, [LOG_FILE, POEM_FILE]).output == expected_multiple_no_opts


def test_tail_file_list() -> None:
    expected_multiple_n5 = """==> tests/resources/common/log.txt <==
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

==> tests/resources/common/poem.txt <==

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert runner.invoke(tail, ["-n 5", LOG_FILE, POEM_FILE]).output == expected_multiple_n5


def test_tail_file_list_combined_options() -> None:
    expected_multiple_q_n6 = """Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert runner.invoke(tail, ["-q", "-n 6", LOG_FILE, POEM_FILE]).output == expected_multiple_q_n6


def test_tail_file_list_non_existent_file() -> None:
    expected_multiple_non_existent = f"""tail: cannot open '{NON_EXISTENT_FILE}' for reading: No such file or directory

Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert (
        runner.invoke(tail, ["-q", "-n 6", NON_EXISTENT_FILE, POEM_FILE]).output
        == expected_multiple_non_existent
    )


def test_tail_file_list_path_is_directory() -> None:
    assert (
        runner.invoke(tail, [DIR_PATH, NON_EXISTENT_FILE, POEM_FILE]).output
        == f"""tail: cannot open '{DIR_PATH}' for reading: No such file or directory
tail: cannot open '{NON_EXISTENT_FILE}' for reading: No such file or directory

==> tests/resources/common/poem.txt <==

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    )


def test_tail_file_list_not_supported_option() -> None:
    expected_value_error = "tail: following multiple files is not supported"
    assert (
        runner.invoke(tail, ["-f", LOG_FILE, POEM_FILE]).exception.args[0] == expected_value_error  # type: ignore
    )
