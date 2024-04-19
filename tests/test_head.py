import subprocess

import pytest
from click.testing import CliRunner

from app.cli.commands import head

LOG_FILE = "tests/resources/log.txt"
POEM_FILE = "tests/resources/poem.txt"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"
DIR_PATH = "test/resources/"

runner = CliRunner()


@pytest.mark.parametrize("file", [LOG_FILE, POEM_FILE])
def test_head_no_options(file: str) -> None:
    assert runner.invoke(head, [file]).output.rstrip("\n") == subprocess.run(
        ["head", file], capture_output=True, text=True
    ).stdout.rstrip("\n")


@pytest.mark.parametrize(
    "head_options, file",
    [("-n 3", LOG_FILE), ("-n 3", POEM_FILE), ("-c 40", LOG_FILE), ("-q", LOG_FILE)],
)
def test_head(head_options: str, file: str) -> None:
    assert runner.invoke(head, [head_options, file]).output.rstrip("\n") == subprocess.run(
        ["head", head_options, file], capture_output=True, text=True
    ).stdout.rstrip("\n")


def test_head_error_message() -> None:
    expected_value_error = "Contradicting flags passed: 'quiet' and 'verbose'"
    assert runner.invoke(head, ["-qv", LOG_FILE]).exception.args[0] == expected_value_error


# NB: serpix head puts additional empty lines between different files in the output for better readabilty
def test_wc_file_list_no_options() -> None:
    expected_multiple_no_opts = """==> tests/resources/log.txt <==
Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

==> tests/resources/poem.txt <==
Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

"""
    assert runner.invoke(head, [LOG_FILE, POEM_FILE]).output == expected_multiple_no_opts


def test_wc_file_list() -> None:
    expected_multiple_n5 = """==> tests/resources/log.txt <==
Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur

==> tests/resources/poem.txt <==
Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

"""
    assert runner.invoke(head, ["-n 5", LOG_FILE, POEM_FILE]).output == expected_multiple_n5


def test_wc_file_list_combined_options() -> None:
    expected_multiple_q_n6 = """Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
"""
    assert runner.invoke(head, ["-q", "-n 6", LOG_FILE, POEM_FILE]).output == expected_multiple_q_n6


def test_wc_file_list_non_existent_file() -> None:
    expected_multiple_non_existent = f"""head: cannot open '{NON_EXISTENT_FILE}' for reading: No such file or directory

Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
"""
    assert (
        runner.invoke(head, ["-q", "-n 6", NON_EXISTENT_FILE, POEM_FILE]).output
        == expected_multiple_non_existent
    )


def test_wc_file_list_invalid_file_path() -> None:
    assert (
        runner.invoke(head, [DIR_PATH, NON_EXISTENT_FILE, POEM_FILE]).output
        == f"""head: cannot open '{DIR_PATH}' for reading: No such file or directory
head: cannot open '{NON_EXISTENT_FILE}' for reading: No such file or directory

==> tests/resources/poem.txt <==
Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

"""
    )
